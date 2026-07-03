from django.conf import settings
from django.db import models


class Media(models.Model):
    """Modèle Media — §4.2 du Cahier des Charges."""

    class TypeMedia(models.TextChoices):
        PRESSE = "presse", "Presse"
        TELEVISION = "television", "Télévision"
        RADIO = "radio", "Radio"
        WEB = "web", "Web"

    class Statut(models.TextChoices):
        ACTIF = "actif", "Actif"
        INACTIF = "inactif", "Inactif"
        SUPPRIME = "supprime", "Supprimé"

    id = models.BigAutoField(primary_key=True)
    nom = models.CharField(max_length=200)
    url = models.CharField(max_length=200, unique=True)
    type_media = models.CharField(max_length=50, choices=TypeMedia.choices)
    statut = models.CharField(max_length=20, choices=Statut.choices, default=Statut.ACTIF)

    # SET_NULL : si l'admin supprime le compte du gestionnaire, le média
    # repasse automatiquement à gestionnaire_id = null (règle du §4.2 / §3.5 du CdC).
    # Seul le Contrôleur peut écrire ce champ (appliqué au niveau permissions, pas BDD).
    gestionnaire = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="medias_geres",
        db_column="gestionnaire_id",
        limit_choices_to={"role": "gestionnaire"},
    )

    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "medias_media"
        ordering = ["nom"]
        verbose_name = "Média"
        verbose_name_plural = "Médias"

    def __str__(self):
        return self.nom
