from rest_framework import serializers

from users.models import User

from .models import Media


class MediaSerializer(serializers.ModelSerializer):
    """Forme commune utilisée en lecture (liste, détail, et après écriture)."""

    gestionnaire_id = serializers.IntegerField(source="gestionnaire.id", read_only=True, allow_null=True)
    gestionnaire_nom = serializers.CharField(source="gestionnaire.nom", read_only=True, allow_null=True)

    class Meta:
        model = Media
        fields = [
            "id", "nom", "url", "type_media", "statut",
            "gestionnaire_id", "gestionnaire_nom", "date_creation",
        ]


class MediaCreateSerializer(serializers.ModelSerializer):
    """
    POST /api/medias/ (Admin).
    ⚠️ Volontairement SANS gestionnaire_id — le CdC §8.3 est explicite :
    "Crée un nouveau média (sans gestionnaire_id)". L'affectation est
    une action distincte, réservée au Contrôleur (PATCH /medias/:id/).
    """

    class Meta:
        model = Media
        fields = ["nom", "url", "type_media"]


class MediaUpdateMetierSerializer(serializers.ModelSerializer):
    """PATCH /api/medias/:id/ — Admin : informations métier uniquement."""

    class Meta:
        model = Media
        fields = ["nom", "url", "type_media", "statut"]
        extra_kwargs = {field: {"required": False} for field in fields}


class MediaUpdateGestionnaireSerializer(serializers.Serializer):
    """PATCH /api/medias/:id/ — Contrôleur : affectation du gestionnaire uniquement."""

    gestionnaire_id = serializers.IntegerField(allow_null=True)

    def validate_gestionnaire_id(self, value):
        if value is None:
            return value
        try:
            user = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Utilisateur introuvable.")
        if user.role != User.Role.GESTIONNAIRE:
            raise serializers.ValidationError(
                "Seul un compte de rôle 'gestionnaire' peut être affecté à un média."
            )
        return value

    def save(self):
        media = self.instance
        gestionnaire_id = self.validated_data["gestionnaire_id"]

        if gestionnaire_id is None:
            media.gestionnaire = None
        else:
            # Un gestionnaire n'est responsable que d'UN SEUL média (§3.3 du CdC :
            # "Responsable d'un seul média"). On le retire donc de tout autre
            # média avant de l'affecter ici (= "réaffectation").
            Media.objects.filter(gestionnaire_id=gestionnaire_id).exclude(id=media.id).update(
                gestionnaire=None
            )
            media.gestionnaire_id = gestionnaire_id

        media.save()
        return media
