"""
Génération des rapports — §7 du Cahier des Charges.

Choix d'implémentation : pas de broker Celery/Redis disponible dans cet
environnement académique. La génération tourne dans un thread Python en
arrière-plan (module `threading`), ce qui permet quand même un vrai flux
asynchrone (POST renvoie immédiatement "en_cours", le front fait du
polling sur /statut/). Le corps de `generate_rapport()` est volontairement
isolé de la vue HTTP : pour passer à Celery en production, il suffit de
décorer cette fonction avec @shared_task et de l'appeler via .delay()
au lieu de Thread(...).start() — aucune autre modification nécessaire.
"""

import datetime as dt
import threading

from django.conf import settings
from django.utils import timezone

from evenements import services as stats_services
from medias.models import Media
from pages.models import PageWeb

from .exceptions import RapportQuotaDepasse
from .models import Rapport


# ------------------------------------------------------------------
# Quota — §7.5 : 3 rapports / 4h glissantes par utilisateur
# ------------------------------------------------------------------
def verifier_quota(user):
    fenetre = timezone.now() - dt.timedelta(hours=settings.RAPPORTS_QUOTA_FENETRE_HEURES)
    rapports_recents = list(
        Rapport.objects.filter(genere_par=user, date_generation__gte=fenetre)
        .order_by("date_generation")
        .values_list("date_generation", flat=True)
    )
    if len(rapports_recents) >= settings.RAPPORTS_QUOTA_MAX:
        plus_ancien = rapports_recents[0]
        expire_a = plus_ancien + dt.timedelta(hours=settings.RAPPORTS_QUOTA_FENETRE_HEURES)
        retry_after = max(int((expire_a - timezone.now()).total_seconds()), 1)
        raise RapportQuotaDepasse(
            retry_after, settings.RAPPORTS_QUOTA_MAX, settings.RAPPORTS_QUOTA_FENETRE_HEURES
        )


# ------------------------------------------------------------------
# Calcul des statistiques d'un rapport (Section 2 et 4 du PDF — §7.4)
# ------------------------------------------------------------------
def _stats_un_media(media_id, debut, fin):
    k = stats_services._kpi_media(media_id, debut, fin)
    debut_prec = debut - (fin - debut) - dt.timedelta(days=1)
    fin_prec = debut - dt.timedelta(days=1)
    k_prec = stats_services._kpi_media(media_id, debut_prec, fin_prec)

    kpi = {
        "visiteurs_uniques": k["visiteurs_uniques"],
        "pages_vues": k["pages_vues"],
        "duree_moyenne": k["duree_moyenne"],
        "scroll_moyen": k["scroll_moyen"],
        "taux_rebond": k["taux_rebond"],
        "delta_visiteurs": stats_services._delta_pct(k["visiteurs_uniques"], k_prec["visiteurs_uniques"]),
        "delta_pages_vues": stats_services._delta_pct(k["pages_vues"], k_prec["pages_vues"]),
    }

    graphiques = {
        "trafic_journalier": stats_services._trafic_journalier(media_id, debut, fin),
        "sources": stats_services._sources(media_id, debut, fin),
        "appareils": stats_services._appareils(media_id, debut, fin),
    }
    # G6 — uniquement si le média a du contenu audio/vidéo
    av = stats_services.compute_audio_video(media_id, (fin - debut).days + 1, date_fin=fin)
    if av["contenus"]:
        graphiques["completion_audio_video"] = av["contenus"][:10]

    stats_detaillees = {
        "top_pages": stats_services._top_pages(media_id, debut, fin, debut_prec, fin_prec, limite=10),
        "repartition_appareils": stats_services.repartition_visiteurs(media_id, debut, fin, "type_appareil"),
        "repartition_navigateurs": stats_services.repartition_visiteurs(media_id, debut, fin, "navigateur"),
        "repartition_os": stats_services.repartition_visiteurs(media_id, debut, fin, "os"),
        "trafic_horaire": stats_services.trafic_horaire_media(media_id, debut, fin),
    }

    return kpi, graphiques, stats_detaillees


def compute_rapport_stats(rapport):
    debut, fin = rapport.periode_debut, rapport.periode_fin
    resultat = {}

    if rapport.type_rapport == Rapport.TypeRapport.MEDIA:
        kpi, graphiques, stats_detaillees = _stats_un_media(rapport.media_id, debut, fin)
        resultat["kpi"] = kpi
        if rapport.inclure_graphiques:
            resultat["graphiques"] = graphiques
        if rapport.inclure_stats:
            resultat["stats_detaillees"] = stats_detaillees

    else:  # GLOBAL — une section par média, JAMAIS agrégées (§7.4 règle explicite)
        medias_ids = rapport.stats.get("medias_ids") or list(
            Media.objects.filter(statut=Media.Statut.ACTIF).values_list("id", flat=True)
        )
        sections = []
        for media_id in medias_ids:
            media = Media.objects.filter(id=media_id).first()
            if not media:
                continue
            kpi, graphiques, stats_detaillees = _stats_un_media(media_id, debut, fin)
            section = {"media_id": media_id, "media_nom": media.nom, "kpi": kpi}
            if rapport.inclure_graphiques:
                section["graphiques"] = graphiques
            if rapport.inclure_stats:
                section["stats_detaillees"] = stats_detaillees
            sections.append(section)
        resultat["sections_par_media"] = sections
        resultat["medias_ids"] = medias_ids

        # G7 + G8 — comparaison multi-médias (si >= 2 médias)
        if rapport.inclure_graphiques and len(medias_ids) >= 2:
            comp = stats_services.compute_comparaison(medias_ids[:6], (fin - debut).days + 1, "visiteurs")
            resultat["comparaison"] = {"evolution": comp["evolution"], "comparaison_kpi": comp["comparaison_kpi"]}

    return resultat


# ------------------------------------------------------------------
# Orchestration — POST /api/rapports/generer/
# ------------------------------------------------------------------
def lancer_generation(rapport_id):
    """Démarre la génération en arrière-plan (thread) et retourne immédiatement."""
    thread = threading.Thread(target=generate_rapport, args=(rapport_id,), daemon=True)
    thread.start()


def generate_rapport(rapport_id):
    """
    Corps de la génération — conçu pour être appelable tel quel depuis un
    thread (actuel) ou une tâche Celery (futur, voir docstring du module).
    """
    from django.db import close_old_connections

    close_old_connections()  # nécessaire car on tourne hors du cycle requête/réponse Django

    try:
        rapport = Rapport.objects.get(id=rapport_id)
    except Rapport.DoesNotExist:
        return

    debut_generation = timezone.now()
    try:
        stats_existantes = rapport.stats or {}
        stats = compute_rapport_stats(rapport)
        stats_existantes.update(stats)
        rapport.stats = stats_existantes

        # Vérification du timeout (§7.5 : 120s max)
        ecoule = (timezone.now() - debut_generation).total_seconds()
        if ecoule > rapport.timeout_secondes:
            rapport.statut = Rapport.Statut.ERREUR
            rapport.message_erreur = (
                f"La génération a dépassé le délai maximum de {rapport.timeout_secondes} secondes."
            )
            rapport.save()
            return

        # Génération du PDF (WeasyPrint, §7.1)
        from .pdf import generer_pdf_rapport

        generer_pdf_rapport(rapport)

        rapport.statut = Rapport.Statut.PRET
        rapport.save()

    except Exception as exc:
        import traceback
        print("=== ERREUR GÉNÉRATION RAPPORT ===")
        traceback.print_exc()
        print("=================================")
        rapport.statut = Rapport.Statut.ERREUR
        rapport.message_erreur = f"Erreur : {str(exc)[:200]}"
        rapport.save()
        
    finally:
        close_old_connections()
