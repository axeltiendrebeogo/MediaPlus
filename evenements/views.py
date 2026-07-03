from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core.permissions import IsControleur, IsGestionnaireOrControleur
from medias.models import Media
from . import services


def _get_period(request):
    period = request.query_params.get("period", "30")
    try:
        period = int(period)
    except ValueError:
        raise ValidationError({"period": ["Doit être un entier (7, 30, 90 ou 365)."]})
    if period not in services.PERIODES_VALIDES:
        raise ValidationError({"period": ["Valeurs autorisées : 7, 30, 90, 365."]})
    return period


def _resolve_media_single(request):
    """
    Résout LE média concerné pour les endpoints à portée "un média à la fois"
    (dashboard, audio-video) : Gestionnaire -> son média (paramètre ignoré),
    Contrôleur -> ?media= obligatoire.
    """
    user = request.user
    if user.role == "gestionnaire":
        media = user.get_media()
        if not media:
            raise NotFound("Aucun média affecté à ce compte gestionnaire.")
        return media

    if user.role == "controleur":
        media_id = request.query_params.get("media")
        if not media_id:
            raise ValidationError({"media": ["Paramètre requis pour le Contrôleur."]})
        try:
            return Media.objects.get(id=media_id)
        except Media.DoesNotExist:
            raise NotFound("Média introuvable.")

    raise PermissionDenied("L'administrateur n'a pas accès aux statistiques.")


# ------------------------------------------------------------------
# 6.1 — GET /api/stats/dashboard/ — Stats agrégées (KPI + G1, G2, G3)
# ------------------------------------------------------------------
class DashboardView(APIView):
    permission_classes = [IsGestionnaireOrControleur]

    def get(self, request):
        media = _resolve_media_single(request)
        period = _get_period(request)
        return Response(services.compute_dashboard(media, period))


# ------------------------------------------------------------------
# 6.2 — GET /api/stats/global/ — Stats globales (Contrôleur)
# ------------------------------------------------------------------
class GlobalStatsView(APIView):
    permission_classes = [IsControleur]

    def get(self, request):
        period = _get_period(request)
        return Response(services.compute_global(period))


# ------------------------------------------------------------------
# 6.3 — GET /api/stats/audio-video/ — Statistiques audio / vidéo (G6)
# ------------------------------------------------------------------
class AudioVideoStatsView(APIView):
    permission_classes = [IsGestionnaireOrControleur]

    def get(self, request):
        media = _resolve_media_single(request)
        period = _get_period(request)
        return Response(services.compute_audio_video(media.id, period))


# ------------------------------------------------------------------
# 6.4 — GET /api/stats/comparaison/ — Comparaison multi-médias (G7, G8)
# ------------------------------------------------------------------
class ComparaisonStatsView(APIView):
    permission_classes = [IsControleur]

    def get(self, request):
        medias_param = request.query_params.get("medias")
        if not medias_param:
            raise ValidationError({"medias": ["Paramètre requis (ex: ?medias=1,2,4)."]})

        try:
            media_ids = [int(x) for x in medias_param.split(",") if x.strip()]
        except ValueError:
            raise ValidationError({"medias": ["Format attendu : IDs séparés par des virgules."]})

        if not (2 <= len(media_ids) <= 6):
            raise ValidationError({"medias": ["Sélectionner entre 2 et 6 médias."]})

        existants = set(Media.objects.filter(id__in=media_ids).values_list("id", flat=True))
        manquants = set(media_ids) - existants
        if manquants:
            raise NotFound(f"Média(s) introuvable(s) : {sorted(manquants)}")

        period = _get_period(request)
        kpi = request.query_params.get("kpi", "visiteurs")
        if kpi not in ("visiteurs", "pages_vues", "duree_moyenne", "scroll_moyen"):
            raise ValidationError({"kpi": ["Valeurs autorisées : visiteurs, pages_vues, duree_moyenne, scroll_moyen."]})

        return Response(services.compute_comparaison(media_ids, period, kpi))
