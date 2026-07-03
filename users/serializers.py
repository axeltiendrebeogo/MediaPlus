from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


# ------------------------------------------------------------------
# Authentification
# ------------------------------------------------------------------
class UserBriefSerializer(serializers.ModelSerializer):
    """Objet "user" imbriqué dans la réponse de connexion (§2.1 du contrat API)."""

    media_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "nom", "email", "role", "media_id"]

    def get_media_id(self, obj):
        media = obj.get_media()
        return media.id if media else None


class MediaPulseTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Login — POST /api/token/.
    Surcharge le serializer simplejwt pour :
    - rejeter les comptes désactivés avec un message clair (is_active=False)
    - inclure l'objet "user" complet dans la réponse, comme documenté.
    """

    default_error_messages = {"no_active_account": "Email ou mot de passe incorrect."}

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = UserBriefSerializer(self.user).data
        return data


# ------------------------------------------------------------------
# Profil connecté — GET /api/auth/me/
# Réutilisé aussi pour les vues admin (liste/détail utilisateurs),
# car le contrat documente exactement la même forme dans les deux cas.
# ------------------------------------------------------------------
class UserSerializer(serializers.ModelSerializer):
    media_id = serializers.SerializerMethodField()
    media_nom = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id", "nom", "email", "role",
            "media_id", "media_nom",
            "date_creation", "is_active",
        ]

    def get_media_id(self, obj):
        media = obj.get_media()
        return media.id if media else None

    def get_media_nom(self, obj):
        media = obj.get_media()
        return media.nom if media else None


# ------------------------------------------------------------------
# Création d'un compte — POST /api/users/ (Admin uniquement)
# ------------------------------------------------------------------
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ["nom", "email", "password", "role"]

    def validate_role(self, value):
        # "L'admin ne peut pas créer un autre admin via cet endpoint" (§3.2 du contrat API)
        if value == User.Role.ADMIN:
            raise serializers.ValidationError(
                "Impossible de créer un compte administrateur via cet endpoint."
            )
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


# ------------------------------------------------------------------
# Modification d'un compte — PATCH /api/users/:id/ (Admin uniquement)
# ------------------------------------------------------------------
class UserUpdateSerializer(serializers.ModelSerializer):
    """
    ⚠️ Conformément au CdC (§3.1 / §9.2), l'admin ne peut PAS affecter ou
    réaffecter un gestionnaire à un média — c'est la responsabilité exclusive
    du Contrôleur (PATCH /api/medias/:id/). Le champ media_id n'est donc PAS
    modifiable ici, contrairement à l'exemple du contrat API (incohérence
    résolue en faveur du CdC, le document de référence).
    """

    class Meta:
        model = User
        fields = ["nom", "email", "is_active"]
        extra_kwargs = {field: {"required": False} for field in fields}
