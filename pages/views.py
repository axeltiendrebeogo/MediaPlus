import datetime as dt

from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.permissions import IsGestionnaireOrControleur
from .models import PageWeb
from .serializers import PageDetailSerializer, PageListSerializer
from .services import compute_page_stats

ALLOWED_ORDERINGS = {"-vues", "-visiteurs", "-duree_moyenne", "date_publication"}


def _annotated_queryset():
    return PageWeb.objects.select_related("media").annotate(
        vues=Count("evenements", filter=Q(evenements__type_even__in=["clic", "scroll"])),
        visiteurs_uniques=Count("evenements__visiteur", distinct=True),
        duree_moyenne=Avg("evenements__duree_ecoute"),
        scroll_moyen=Avg("evenements__profondeur_scroll"),
    )


def _scope_queryset_to_user(qs, request):
    """
    Applique la portée d'accès par rôle (§5.1 du contrat) :
    - Gestionnaire : uniquement les pages de SON média (filtré automatiquement)
    - Contrôleur   : ?media= obligatoire
    - Admin        : aucun accès (§9.2 du CdC)
    """
    user = request.user
    if user.role == "gestionnaire":
        media = user.get_media()
        return qs.filter(media=media) if media else qs.none()

    if user.role == "controleur":
        media_id = request.query_params.get("media")
        if not media_id:
            raise ValidationError({"media": ["Paramètre requis pour le Contrôleur."]})
        return qs.filter(media_id=media_id)

    raise PermissionDenied("L'administrateur n'a pas accès aux données des pages.")


def _check_object_access(user, page):
    if user.role == "controleur":
        return
    if user.role == "gestionnaire" and page.media_id == (user.get_media() and user.get_media().id):
        return
    raise PermissionDenied("Vous n'avez pas accès à cette page.")


# ------------------------------------------------------------------
# 5.1 — GET /api/pages/ — Liste des pages
# ------------------------------------------------------------------
class PageListView(ListAPIView):
    permission_classes = [IsGestionnaireOrControleur]
    serializer_class = PageListSerializer

    def get_queryset(self):
        qs = _scope_queryset_to_user(_annotated_queryset(), self.request)

        date_debut = self.request.query_params.get("date_debut")
        if date_debut:
            qs = qs.filter(date_publication__gte=date_debut)

        date_fin = self.request.query_params.get("date_fin")
        if date_fin:
            qs = qs.filter(date_publication__lte=date_fin)

        ordering = self.request.query_params.get("ordering")
        if ordering in ALLOWED_ORDERINGS:
            qs = qs.order_by(ordering)
        else:
            qs = qs.order_by("-date_publication")

        return qs


# ------------------------------------------------------------------
# GET /api/pages/:id/ — Détail d'une page
# ------------------------------------------------------------------
class PageDetailView(RetrieveAPIView):
    permission_classes = [IsGestionnaireOrControleur]
    serializer_class = PageDetailSerializer
    queryset = _annotated_queryset()

    def get_object(self):
        page = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        _check_object_access(self.request.user, page)
        return page


# ------------------------------------------------------------------
# 5.2 — GET /api/pages/:id/stats/ — Statistiques détaillées (G2-G5)
# ------------------------------------------------------------------
class PageStatsView(APIView):
    permission_classes = [IsGestionnaireOrControleur]

    def get(self, request, pk):
        page = get_object_or_404(PageWeb, pk=pk)
        _check_object_access(request.user, page)

        date_fin = request.query_params.get("date_fin")
        date_fin = dt.date.fromisoformat(date_fin) if date_fin else dt.date.today()

        date_debut = request.query_params.get("date_debut")
        date_debut = dt.date.fromisoformat(date_debut) if date_debut else date_fin - dt.timedelta(days=30)

        stats = compute_page_stats(page, date_debut, date_fin)

        return Response({
            "page_id": page.id,
            "nom": page.nom,
            "periode": {"debut": date_debut.isoformat(), "fin": date_fin.isoformat()},
            **stats,
        })
