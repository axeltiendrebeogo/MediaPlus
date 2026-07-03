from django.conf import settings
from django.db import models


class Rapport(models.Model):
    """
    Modèle Rapport — §4.6 du Cahier des Charges.

    NB : pour un rapport global multi-médias, la liste des médias inclus
    (medias_ids du formulaire — §7.3) est conservée DANS le champ JSONB
    `stats` (clé "medias_ids"), au même endroit que "sections_par_media".
    Le CdC ne prévoit pas de colonne dédiée pour cette liste ; le champ
    `stats` étant explicitement prévu comme blob flexible (§4.6 : "voir §7"),
    c'est l'endroit le plus cohérent pour la stocker sans dupliquer le schéma.
    """

    class TypeRapport(models.TextChoices):
        MEDIA = "media", "Par média"
        GLOBAL = "global", "Global (multi-médias)"

    class Statut(models.TextChoices):
        EN_COURS = "en_cours", "En cours"
        PRET = "pret", "Prêt"
        ERREUR = "erreur", "Erreur"

    id = models.BigAutoField(primary_key=True)
    type_rapport = models.CharField(max_length=20, choices=TypeRapport.choices)
    periode_debut = models.DateField()
    periode_fin = models.DateField()
    inclure_graphiques = models.BooleanField(default=True)
    inclure_stats = models.BooleanField(default=True)

    # Statistiques calculées par Django (voir rapports/services.py) + métadonnées
    # (medias_ids pour un rapport global — voir docstring ci-dessus).
    stats = models.JSONField(default=dict, blank=True)

    statut = models.CharField(max_length=20, choices=Statut.choices, default=Statut.EN_COURS)
    date_generation = models.DateTimeField(auto_now_add=True)
    timeout_secondes = models.IntegerField(default=120)

    # NULL si rapport global (couvre potentiellement plusieurs médias)
    media = models.ForeignKey(
        "medias.Media",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="rapports",
        db_column="media_id",
    )
    genere_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="rapports_generes",
        db_column="genere_par_id",
    )

    # Message d'erreur si statut = "erreur" (ex: timeout) — pratique pour le polling.
    message_erreur = models.CharField(max_length=255, null=True, blank=True)
    # Chemin du PDF une fois généré (PDF_STORAGE_PATH — §2.3 du CdC)
    fichier_pdf = models.FileField(upload_to="rapports/", null=True, blank=True)

    class Meta:
        db_table = "rapports_rapport"
        ordering = ["-date_generation"]
        verbose_name = "Rapport"
        verbose_name_plural = "Rapports"

    def __str__(self):
        return f"Rapport #{self.id} ({self.type_rapport}, {self.statut})"

    @property
    def titre(self):
        """Titre lisible affiché côté front — calculé, non stocké en base."""
        mois_fr = [
            "", "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
            "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre",
        ]
        periode = f"{mois_fr[self.periode_fin.month]} {self.periode_fin.year}"
        if self.type_rapport == self.TypeRapport.GLOBAL:
            return f"Rapport Global {periode}"
        media_nom = self.media.nom if self.media_id else "Média supprimé"
        return f"Rapport {periode} — {media_nom}"
