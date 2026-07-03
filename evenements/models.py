from django.db import models


class Visiteur(models.Model):
    """Modèle Visiteur — §4.4 du Cahier des Charges."""

    class TypeAppareil(models.TextChoices):
        MOBILE = "mobile", "Mobile"
        DESKTOP = "desktop", "Desktop"
        TABLETTE = "tablette", "Tablette"

    class SourceTrafic(models.TextChoices):
        RECHERCHE = "recherche", "Recherche organique"
        DIRECT = "direct", "Direct"
        RESEAUX_SOCIAUX = "reseaux_sociaux", "Réseaux sociaux"
        AUTRES = "autres", "Autres"

    id = models.BigAutoField(primary_key=True)
    adresse_ip = models.CharField(max_length=45)
    type_appareil = models.CharField(max_length=50, choices=TypeAppareil.choices)
    os = models.CharField(max_length=50, null=True, blank=True)
    navigateur = models.CharField(max_length=100, null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)

    # ⚠️ AJOUT par rapport au §4.4 strict du CdC.
    # Nécessaire pour calculer G2 "Sources de trafic" (§6.1) — le CdC le
    # mentionne lui-même comme conditionnel : "si disponible en base" (§6.1).
    # Sans ce champ, G2 est impossible à calculer. À confirmer en équipe.
    source_trafic = models.CharField(
        max_length=30, choices=SourceTrafic.choices, null=True, blank=True
    )

    class Meta:
        db_table = "evenements_visiteur"
        verbose_name = "Visiteur"
        verbose_name_plural = "Visiteurs"

    def __str__(self):
        return f"Visiteur #{self.id} ({self.adresse_ip})"


class Evenement(models.Model):
    """Modèle Evenement — §4.5 du Cahier des Charges."""

    class TypeEvenement(models.TextChoices):
        CLIC = "clic", "Clic"
        SCROLL = "scroll", "Scroll"
        LECTURE = "lecture", "Lecture (audio)"
        VISIONNAGE = "visionnage", "Visionnage (vidéo)"

    id = models.BigAutoField(primary_key=True)
    type_even = models.CharField(max_length=50, choices=TypeEvenement.choices)
    date_heure = models.DateTimeField()
    duree_ecoute = models.IntegerField(null=True, blank=True, help_text="Secondes")
    profondeur_scroll = models.IntegerField(null=True, blank=True, help_text="0 à 100 (%)")

    visiteur = models.ForeignKey(
        Visiteur, on_delete=models.CASCADE, related_name="evenements", db_column="visiteur_id"
    )
    page = models.ForeignKey(
        "pages.PageWeb", on_delete=models.CASCADE, related_name="evenements", db_column="page_id"
    )

    class Meta:
        db_table = "evenements_evenement"
        ordering = ["-date_heure"]
        verbose_name = "Événement"
        verbose_name_plural = "Événements"
        indexes = [
            models.Index(fields=["date_heure"]),
            models.Index(fields=["type_even"]),
            models.Index(fields=["page", "date_heure"]),
        ]

    def __str__(self):
        return f"{self.type_even} — page #{self.page_id} — {self.date_heure}"
