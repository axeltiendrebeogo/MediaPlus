"""
Calculs statistiques pour une page web — GET /api/pages/:id/stats/
Formules suivies à la lettre du §5.4 (stats par page) et §6.2 (graphiques G4/G5)
du Cahier des Charges. Les graphiques G2 (sources) et G3 (appareils) sont
réutilisés ici à l'échelle de la page, comme documenté dans la réponse
exemple du contrat API (§5.2).
"""

from django.db.models import Avg, Count, Q

from evenements.models import Evenement, Visiteur

HEURES = [f"{h:02d}:00" for h in range(24)]
SOURCES = [
    (Visiteur.SourceTrafic.RECHERCHE, "Recherche"),
    (Visiteur.SourceTrafic.DIRECT, "Direct"),
    (Visiteur.SourceTrafic.RESEAUX_SOCIAUX, "Réseaux sociaux"),
    (Visiteur.SourceTrafic.AUTRES, "Autres"),
]
SCROLL_SEUILS = [(25, "0-25%"), (50, "25-50%"), (75, "50-75%"), (100, "75-100%")]


def _events_periode(page, date_debut, date_fin):
    return Evenement.objects.filter(
        page=page, date_heure__date__gte=date_debut, date_heure__date__lte=date_fin
    )


def _kpi(events):
    vues = events.filter(type_even__in=["clic", "scroll"]).count()
    visiteurs_uniques = events.values("visiteur_id").distinct().count()
    duree_moyenne = events.filter(duree_ecoute__isnull=False).aggregate(a=Avg("duree_ecoute"))["a"] or 0
    scroll_moyen = events.filter(profondeur_scroll__isnull=False).aggregate(a=Avg("profondeur_scroll"))["a"] or 0

    # Taux de rebond : parmi les visiteurs de cette page, % n'ayant
    # consulté AUCUNE autre page sur toute la plateforme (§5.2 du CdC).
    visiteur_ids = list(events.values_list("visiteur_id", flat=True).distinct())
    taux_rebond = 0
    if visiteur_ids:
        par_visiteur = (
            Evenement.objects.filter(visiteur_id__in=visiteur_ids)
            .values("visiteur_id")
            .annotate(nb_pages=Count("page_id", distinct=True))
        )
        mono_page = sum(1 for v in par_visiteur if v["nb_pages"] == 1)
        taux_rebond = round(mono_page / len(visiteur_ids) * 100)

    return {
        "vues": vues,
        "visiteurs_uniques": visiteurs_uniques,
        "duree_moyenne": round(duree_moyenne),
        "scroll_moyen": round(scroll_moyen),
        "taux_rebond": taux_rebond,
    }


def _par_heure(events):
    """G4 — visiteurs uniques par heure de la journée (0h à 23h, §6.2)."""
    from django.db.models.functions import ExtractHour

    rows = (
        events.annotate(h=ExtractHour("date_heure"))
        .values("h")
        .annotate(visiteurs=Count("visiteur_id", distinct=True))
    )
    par_heure = {row["h"]: row["visiteurs"] for row in rows}
    return [{"heure": HEURES[h], "visiteurs": par_heure.get(h, 0)} for h in range(24)]


def _scroll_sections(events):
    """G5 — % de visiteurs ayant atteint chaque palier de scroll (§6.2)."""
    scrolls = events.filter(profondeur_scroll__isnull=False)
    visiteurs_scroll = scrolls.values("visiteur_id").distinct()
    total = visiteurs_scroll.count()
    if total == 0:
        return [{"section": label, "pct_visiteurs": 0} for _, label in SCROLL_SEUILS]

    resultats = []
    for seuil, label in SCROLL_SEUILS:
        nb = (
            scrolls.filter(profondeur_scroll__gte=seuil)
            .values("visiteur_id")
            .distinct()
            .count()
        )
        resultats.append({"section": label, "pct_visiteurs": round(nb / total * 100)})
    return resultats


def _appareils(events):
    """G3 — répartition par type d'appareil (visiteurs distincts de la page)."""
    visiteur_ids = events.values_list("visiteur_id", flat=True).distinct()
    qs = (
        Visiteur.objects.filter(id__in=visiteur_ids)
        .values("type_appareil")
        .annotate(n=Count("id"))
    )
    total = sum(row["n"] for row in qs)
    if total == 0:
        return [{"type": t, "pct": 0} for t, _ in Visiteur.TypeAppareil.choices]
    return [
        {"type": row["type_appareil"], "pct": round(row["n"] / total * 100)}
        for row in qs
    ]


def _sources(events):
    """G2 — répartition par source de trafic (visiteurs distincts de la page)."""
    visiteur_ids = events.values_list("visiteur_id", flat=True).distinct()
    qs = (
        Visiteur.objects.filter(id__in=visiteur_ids, source_trafic__isnull=False)
        .values("source_trafic")
        .annotate(n=Count("id"))
    )
    par_code = {row["source_trafic"]: row["n"] for row in qs}
    total = sum(par_code.values())
    if total == 0:
        return [{"source": label, "pct": 0} for _, label in SOURCES]
    return [
        {"source": label, "pct": round(par_code.get(code, 0) / total * 100)}
        for code, label in SOURCES
    ]


def compute_page_stats(page, date_debut, date_fin):
    events = _events_periode(page, date_debut, date_fin)
    data = _kpi(events)
    data["par_heure"] = _par_heure(events)
    data["scroll_sections"] = _scroll_sections(events)
    data["appareils"] = _appareils(events)
    data["sources"] = _sources(events)
    return data
