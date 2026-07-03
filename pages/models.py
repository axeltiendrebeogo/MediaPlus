from django.db import models


class PageWeb(models.Model):
    """Modèle Page_web — §4.3 du Cahier des Charges."""

    id = models.BigAutoField(primary_key=True)
    nom = models.CharField(max_length=300)
    url = models.CharField(max_length=500)
    date_publication = models.DateField()
    auteur = models.CharField(max_length=150, null=True, blank=True)

    # ⚠️ AJOUT par rapport au §4.3 strict du CdC.
    # Nécessaire pour calculer le taux de complétion audio/vidéo (§5.5 :
    # "Taux de complétion = AVG(duree_ecoute / duree_contenu) × 100,
    # source : Evenement + Page_web") — ce champ est requis pour que ce
    # calcul soit possible, mais absent du modèle Page_web documenté.
    # NULL pour les pages purement texte (articles, où la notion ne s'applique pas).
    duree_contenu = models.IntegerField(
        null=True, blank=True, help_text="Durée du contenu en secondes (audio/vidéo uniquement)"
    )

    media = models.ForeignKey(
        "medias.Media",
        on_delete=models.CASCADE,
        related_name="pages",
        db_column="media_id",
    )

    class Meta:
        db_table = "pages_page_web"
        ordering = ["-date_publication"]
        verbose_name = "Page web"
        verbose_name_plural = "Pages web"

    def __str__(self):
        return self.nom
