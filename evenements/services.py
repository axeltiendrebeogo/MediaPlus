"""
Calculs statistiques agrégés — endpoints /api/stats/* (§6 du CdC).

Choix d'implémentation : les statistiques sont calculées EN DIRECT à
chaque requête (lecture seule sur PostgreSQL) plutôt que pré-calculées
par une tâche planifiée toutes les heures (§5.1 / §2.2 du CdC prévoient
Celery/cron). Pour le volume de données de ce projet académique, un calcul
à la demande est toujours exact et évite la complexité d'infrastructure
de Celery. `derniere_maj` reflète donc l'heure de la requête elle-même.
Si la volumétrie réelle l'exigeait, ces fonctions sont le point d'entrée
naturel à brancher sur une tâche planifiée + cache, sans changer les vues.
"""

import datetime as dt

from django.db.models import Avg, Count, Q, Sum
from django.utils import timezone

from evenements.models import Evenement, Visiteur
from medias.models import Media
from pages.models import PageWeb

COULEURS_SOURCES = {
    Visiteur.SourceTrafic.RECHERCHE: "#3B82F6",
    Visiteur.SourceTrafic.DIRECT: "#10B981",
    Visiteur.SourceTrafic.RESEAUX_SOCIAUX: "#8B5CF6",
    Visiteur.SourceTrafic.AUTRES: "#F59E0B",
}
LABELS_SOURCES = {
    Visiteur.SourceTrafic.RECHERCHE: "Recherche",
    Visiteur.SourceTrafic.DIRECT: "Direct",
    Visiteur.SourceTrafic.RESEAUX_SOCIAUX: "Réseaux sociaux",
    Visiteur.SourceTrafic.AUTRES: "Autres",
}
PALETTE_MEDIAS = ["#3B82F6", "#10B981", "#8B5CF6", "#F59E0B", "#EF4444", "#06B6D4"]

PERIODES_VALIDES = (7, 30, 90, 365)


def periode_bounds(period_jours, date_fin=None):
    """Retourne (debut, fin) pour la période demandée + la période précédente de même longueur."""
    fin = date_fin or timezone.now().date()
    debut = fin - dt.timedelta(days=period_jours - 1)
    fin_precedente = debut - dt.timedelta(days=1)
    debut_precedente = fin_precedente - dt.timedelta(days=period_jours - 1)
    return debut, fin, debut_precedente, fin_precedente


def _events_media_periode(media_id, debut, fin):
    return Evenement.objects.filter(
        page__media_id=media_id, date_heure__date__gte=debut, date_heure__date__lte=fin
    )


def _delta_pct(actuel, precedent):
    if not precedent:
        return 0.0 if not actuel else 100.0
    return round((actuel - precedent) / precedent * 100, 1)


def _kpi_media(media_id, debut, fin):
    events = _events_media_periode(media_id, debut, fin)
    visiteurs_uniques = events.values("visiteur_id").distinct().count()
    pages_vues = events.filter(type_even__in=["clic", "scroll"]).count()
    duree_moyenne = events.filter(duree_ecoute__isnull=False).aggregate(a=Avg("duree_ecoute"))["a"] or 0
    scroll_moyen = events.filter(profondeur_scroll__isnull=False).aggregate(a=Avg("profondeur_scroll"))["a"] or 0

    visiteur_ids = list(events.values_list("visiteur_id", flat=True).distinct())
    taux_rebond = 0
    if visiteur_ids:
        par_visiteur = (
            Evenement.objects.filter(visiteur_id__in=visiteur_ids, page__media_id=media_id)
            .values("visiteur_id")
            .annotate(nb_pages=Count("page_id", distinct=True))
        )
        mono_page = sum(1 for v in par_visiteur if v["nb_pages"] == 1)
        taux_rebond = round(mono_page / len(visiteur_ids) * 100)

    return {
        "visiteurs_uniques": visiteurs_uniques,
        "pages_vues": pages_vues,
        "duree_moyenne": round(duree_moyenne),
        "scroll_moyen": round(scroll_moyen),
        "taux_rebond": taux_rebond,
    }


def _trafic_journalier(media_id, debut, fin):
    from django.db.models.functions import TruncDate

    events = _events_media_periode(media_id, debut, fin)
    rows = (
        events.annotate(jour=TruncDate("date_heure"))
        .values("jour")
        .annotate(
            vues=Count("id", filter=Q(type_even__in=["clic", "scroll"])),
            visiteurs=Count("visiteur_id", distinct=True),
        )
    )
    par_jour = {row["jour"]: row for row in rows}

    resultat = []
    jour = debut
    while jour <= fin:
        row = par_jour.get(jour)
        resultat.append({
            "date": jour.isoformat(),
            "vues": row["vues"] if row else 0,
            "visiteurs": row["visiteurs"] if row else 0,
        })
        jour += dt.timedelta(days=1)
    return resultat


def _sources(media_id, debut, fin):
    events = _events_media_periode(media_id, debut, fin)
    visiteur_ids = events.values_list("visiteur_id", flat=True).distinct()
    qs = (
        Visiteur.objects.filter(id__in=visiteur_ids, source_trafic__isnull=False)
        .values("source_trafic")
        .annotate(n=Count("id"))
    )
    par_code = {row["source_trafic"]: row["n"] for row in qs}
    total = sum(par_code.values())
    resultat = []
    for code, label in LABELS_SOURCES.items():
        n = par_code.get(code, 0)
        resultat.append({
            "source": label,
            "pct": round(n / total * 100) if total else 0,
            "couleur": COULEURS_SOURCES[code],
        })
    return resultat


def _appareils(media_id, debut, fin):
    events = _events_media_periode(media_id, debut, fin)
    visiteur_ids = events.values_list("visiteur_id", flat=True).distinct()
    qs = Visiteur.objects.filter(id__in=visiteur_ids).values("type_appareil").annotate(n=Count("id"))
    total = sum(row["n"] for row in qs)
    par_code = {row["type_appareil"]: row["n"] for row in qs}
    return [
        {"type": code, "pct": round(par_code.get(code, 0) / total * 100) if total else 0}
        for code, _ in Visiteur.TypeAppareil.choices
    ]


def repartition_visiteurs(media_id, debut, fin, champ):
    """
    Répartition générique des visiteurs d'un média sur une période, par
    champ (type_appareil | os | navigateur) — réutilisé par le rapport PDF
    pour repartition_appareils / repartition_navigateurs / repartition_os (§7.4).
    """
    events = _events_media_periode(media_id, debut, fin)
    visiteur_ids = events.values_list("visiteur_id", flat=True).distinct()
    qs = (
        Visiteur.objects.filter(id__in=visiteur_ids)
        .exclude(**{f"{champ}__isnull": True})
        .values(champ)
        .annotate(n=Count("id"))
        .order_by("-n")
    )
    total = sum(row["n"] for row in qs)
    return [
        {"label": row[champ], "pct": round(row["n"] / total * 100) if total else 0, "n": row["n"]}
        for row in qs
    ]


def trafic_horaire_media(media_id, debut, fin):
    """Volume de visiteurs par heure de la journée (0h-23h), agrégé sur toute la période."""
    from django.db.models.functions import ExtractHour

    events = _events_media_periode(media_id, debut, fin)
    rows = (
        events.annotate(h=ExtractHour("date_heure"))
        .values("h")
        .annotate(visiteurs=Count("visiteur_id", distinct=True))
    )
    par_heure = {row["h"]: row["visiteurs"] for row in rows}
    return [{"heure": f"{h:02d}:00", "visiteurs": par_heure.get(h, 0)} for h in range(24)]


def _top_pages(media_id, debut, fin, debut_prec, fin_prec, limite=5):
    events = _events_media_periode(media_id, debut, fin)
    pages_stats = (
        events.filter(type_even__in=["clic", "scroll"])
        .values("page_id", "page__nom")
        .annotate(
            vues=Count("id"),
            duree_moyenne=Avg("duree_ecoute"),
            scroll_moyen=Avg("profondeur_scroll"),
        )
        .order_by("-vues")[:limite]
    )

    resultat = []
    for row in pages_stats:
        vues_precedent = _events_media_periode(media_id, debut_prec, fin_prec).filter(
            page_id=row["page_id"], type_even__in=["clic", "scroll"]
        ).count()
        resultat.append({
            "id": row["page_id"],
            "nom": row["page__nom"],
            "vues": row["vues"],
            "duree_moyenne": round(row["duree_moyenne"] or 0),
            "scroll_moyen": round(row["scroll_moyen"] or 0),
            "tendance": "up" if row["vues"] >= vues_precedent else "down",
        })
    return resultat


def compute_dashboard(media, period_jours):
    debut, fin, debut_prec, fin_prec = periode_bounds(period_jours)
    kpi_actuel = _kpi_media(media.id, debut, fin)
    kpi_precedent = _kpi_media(media.id, debut_prec, fin_prec)

    kpi = {
        cle: {"valeur": kpi_actuel[cle], "delta_pct": _delta_pct(kpi_actuel[cle], kpi_precedent[cle])}
        for cle in kpi_actuel
    }

    return {
        "media_id": media.id,
        "media_nom": media.nom,
        "periode": {"jours": period_jours, "debut": debut.isoformat(), "fin": fin.isoformat()},
        "derniere_maj": timezone.now().isoformat(),
        "kpi": kpi,
        "trafic_journalier": _trafic_journalier(media.id, debut, fin),
        "sources": _sources(media.id, debut, fin),
        "appareils": _appareils(media.id, debut, fin),
        "top_pages": _top_pages(media.id, debut, fin, debut_prec, fin_prec, limite=5),
    }


def compute_global(period_jours):
    from rapports.models import Rapport

    debut, fin, _, _ = periode_bounds(period_jours)
    medias_actifs = Media.objects.filter(statut=Media.Statut.ACTIF)

    events_periode = Evenement.objects.filter(
        page__media__in=medias_actifs, date_heure__date__gte=debut, date_heure__date__lte=fin
    )
    visiteurs_total = events_periode.values("visiteur_id").distinct().count()
    pages_vues_total = events_periode.filter(type_even__in=["clic", "scroll"]).count()
    rapports_generes = Rapport.objects.filter(
        date_generation__date__gte=debut, date_generation__date__lte=fin
    ).count()

    par_media = []
    for media in medias_actifs:
        k = _kpi_media(media.id, debut, fin)
        par_media.append({
            "media_id": media.id,
            "media_nom": media.nom,
            "type_media": media.type_media,
            "visiteurs": k["visiteurs_uniques"],
            "pages_vues": k["pages_vues"],
            "duree_moyenne": k["duree_moyenne"],
            "scroll_moyen": k["scroll_moyen"],
        })

    return {
        "periode": {"jours": period_jours, "debut": debut.isoformat(), "fin": fin.isoformat()},
        "derniere_maj": timezone.now().isoformat(),
        "totaux": {
            "medias_actifs": medias_actifs.count(),
            "visiteurs_total": visiteurs_total,
            "pages_vues_total": pages_vues_total,
            "rapports_generes": rapports_generes,
        },
        "par_media": par_media,
    }


def compute_audio_video(media_id, period_jours, date_fin=None):
    debut, fin, _, _ = periode_bounds(period_jours, date_fin)
    events = _events_media_periode(media_id, debut, fin).filter(type_even__in=["lecture", "visionnage"])

    total_lectures = events.count()
    duree_moy_ecoute = events.aggregate(a=Avg("duree_ecoute"))["a"] or 0

    contenus_qs = (
        events.values("page_id", "page__nom", "page__duree_contenu", "type_even")
        .annotate(nb_lectures=Count("id"), duree_moy_ecoute=Avg("duree_ecoute"))
        .order_by("-nb_lectures")
    )

    contenus = []
    completions = []
    for row in contenus_qs:
        duree_contenu = row["page__duree_contenu"]
        taux_completion = 0
        if duree_contenu:
            taux_completion = round((row["duree_moy_ecoute"] or 0) / duree_contenu * 100)
            completions.append(taux_completion)
        contenus.append({
            "page_id": row["page_id"],
            "titre": row["page__nom"],
            "type": "video" if row["type_even"] == "visionnage" else "audio",
            "duree_contenu": duree_contenu,
            "nb_lectures": row["nb_lectures"],
            "duree_moy_ecoute": round(row["duree_moy_ecoute"] or 0),
            "taux_completion": taux_completion,
        })

    return {
        "media_id": media_id,
        "kpi": {
            "total_contenus": len(contenus),
            "total_lectures": total_lectures,
            "duree_moy_ecoute": round(duree_moy_ecoute),
            "completion_moy": round(sum(completions) / len(completions)) if completions else 0,
        },
        "contenus": contenus,
    }


def compute_comparaison(media_ids, period_jours, kpi_choisi):
    debut, fin, _, _ = periode_bounds(period_jours)
    medias = list(Media.objects.filter(id__in=media_ids))
    couleurs = {str(m.id): PALETTE_MEDIAS[i % len(PALETTE_MEDIAS)] for i, m in enumerate(medias)}

    # G7 — évolution journalière des visiteurs, une série par média
    from django.db.models.functions import TruncDate

    par_jour = {}
    jour = debut
    while jour <= fin:
        par_jour[jour] = {"date": jour.isoformat()}
        jour += dt.timedelta(days=1)

    for media in medias:
        events = _events_media_periode(media.id, debut, fin)
        rows = (
            events.annotate(jour=TruncDate("date_heure"))
            .values("jour")
            .annotate(visiteurs=Count("visiteur_id", distinct=True))
        )
        par_media_jour = {row["jour"]: row["visiteurs"] for row in rows}
        for d in par_jour:
            par_jour[d][media.nom] = par_media_jour.get(d, 0)

    evolution = [par_jour[d] for d in sorted(par_jour)]

    # G8 — comparaison sur le KPI choisi
    champ_par_kpi = {
        "visiteurs": "visiteurs_uniques",
        "pages_vues": "pages_vues",
        "duree_moyenne": "duree_moyenne",
        "scroll_moyen": "scroll_moyen",
    }
    champ = champ_par_kpi.get(kpi_choisi, "visiteurs_uniques")
    comparaison_kpi = []
    for media in medias:
        k = _kpi_media(media.id, debut, fin)
        comparaison_kpi.append({"media_id": media.id, "media_nom": media.nom, "valeur": k[champ]})

    return {
        "periode": {"jours": period_jours, "debut": debut.isoformat(), "fin": fin.isoformat()},
        "evolution": evolution,
        "comparaison_kpi": comparaison_kpi,
        "couleurs": couleurs,
    }
