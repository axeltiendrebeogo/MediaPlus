import datetime as dt

from django.utils import timezone
from rest_framework import serializers

from medias.models import Media
from users.models import User

from .models import Rapport


class RapportListSerializer(serializers.ModelSerializer):
    titre = serializers.CharField(read_only=True)
    media_id = serializers.IntegerField(source="media.id", read_only=True, allow_null=True)
    media_nom = serializers.CharField(source="media.nom", read_only=True, allow_null=True, default=None)
    genere_par_nom = serializers.CharField(source="genere_par.nom", read_only=True)

    class Meta:
        model = Rapport
        fields = [
            "id", "titre", "type_rapport", "media_id", "media_nom",
            "periode_debut", "periode_fin", "statut", "date_generation",
            "genere_par_nom", "inclure_graphiques", "inclure_stats",
        ]


class RapportGenererSerializer(serializers.Serializer):
    """
    POST /api/rapports/generer/ — §7.3 du CdC.
    La portée autorisée dépend du rôle de l'utilisateur (appliqué dans .validate()) :
    - Gestionnaire : type_rapport="media" uniquement, toujours sur SON média.
    - Contrôleur   : "media" (n'importe quel média) ou "global" (medias_ids).
    """

    type_rapport = serializers.ChoiceField(choices=Rapport.TypeRapport.choices)
    media_id = serializers.IntegerField(required=False, allow_null=True)
    medias_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    periode_debut = serializers.DateField()
    periode_fin = serializers.DateField()
    inclure_stats = serializers.BooleanField(default=True)
    inclure_graphiques = serializers.BooleanField(default=True)

    def validate(self, attrs):
        user = self.context["request"].user
        type_rapport = attrs["type_rapport"]

        if attrs["periode_fin"] < attrs["periode_debut"]:
            raise serializers.ValidationError({"periode_fin": ["Doit être postérieure à periode_debut."]})
        if attrs["periode_fin"] > timezone.now().date():
            raise serializers.ValidationError({"periode_fin": ["Ne peut pas être dans le futur."]})

        if user.role == "gestionnaire":
            if type_rapport != Rapport.TypeRapport.MEDIA:
                raise serializers.ValidationError(
                    {"type_rapport": ["Un gestionnaire ne peut générer que des rapports de type 'media'."]}
                )
            media = user.get_media()
            if not media:
                raise serializers.ValidationError("Aucun média affecté à ce compte.")
            attrs["media"] = media

        elif user.role == "controleur":
            if type_rapport == Rapport.TypeRapport.MEDIA:
                media_id = attrs.get("media_id")
                if not media_id:
                    raise serializers.ValidationError({"media_id": ["Requis pour un rapport de type 'media'."]})
                media = Media.objects.filter(id=media_id).first()
                if not media:
                    raise serializers.ValidationError({"media_id": ["Média introuvable."]})
                attrs["media"] = media
            else:  # global
                medias_ids = attrs.get("medias_ids")
                if not medias_ids:
                    raise serializers.ValidationError({"medias_ids": ["Requis pour un rapport de type 'global'."]})
                existants = set(Media.objects.filter(id__in=medias_ids).values_list("id", flat=True))
                manquants = set(medias_ids) - existants
                if manquants:
                    raise serializers.ValidationError({"medias_ids": [f"Média(s) introuvable(s) : {sorted(manquants)}"]})
                attrs["media"] = None

        else:
            raise serializers.ValidationError("Rôle non autorisé à générer des rapports.")

        return attrs
