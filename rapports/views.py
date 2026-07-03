import datetime as dt

from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from core.permissions import IsGestionnaireOrControleur
from . import services
from .models import Rapport
from .serializers import RapportGenererSerializer, RapportListSerializer

ALLOWED_ORDERINGS = {"-date_generation", "date_generation"}


def _scope_queryset(qs, user):
    if user.role == "gestionnaire":
        media = user.get_media()
        return qs.filter(media=media) if media else qs.none()
    if user.role == "controleur":
        return qs
    raise PermissionDenied("L'administrateur n'a pas accès aux rapports.")


def _check_object_access(user, rapport):
    if user.role == "controleur":
        return
    if user.role == "gestionnaire":
        media = user.get_media()
        if media and rapport.media_id == media.id:
            return
    raise PermissionDenied("Vous n'avez pas accès à ce rapport.")


# ------------------------------------------------------------------
# 7.1 — GET /api/rapports/ — Liste des rapports
# ------------------------------------------------------------------
class RapportListView(generics.ListAPIView):
    permission_classes = [IsGestionnaireOrControleur]
    serializer_class = RapportListSerializer

    def get_queryset(self):
        qs = _scope_queryset(Rapport.objects.select_related("media", "genere_par"), self.request.user)

        media = self.request.query_params.get("media")
        if media:
            qs = qs.filter(media_id=media)

        type_rapport = self.request.query_params.get("type_rapport")
        if type_rapport:
            qs = qs.filter(type_rapport=type_rapport)

        statut = self.request.query_params.get("statut")
        if statut:
            qs = qs.filter(statut=statut)

        ordering = self.request.query_params.get("ordering", "-date_generation")
        if ordering not in ALLOWED_ORDERINGS:
            ordering = "-date_generation"
        return qs.order_by(ordering)


# ------------------------------------------------------------------
# 7.2 — POST /api/rapports/generer/ — Déclenche la génération (async)
# ------------------------------------------------------------------
class GenererRapportView(APIView):
    permission_classes = [IsGestionnaireOrControleur]

    def post(self, request):
        services.verifier_quota(request.user)  # lève RapportQuotaDepasse (429) si dépassé

        serializer = RapportGenererSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        stats_initiales = {}
        if data["type_rapport"] == Rapport.TypeRapport.GLOBAL:
            stats_initiales["medias_ids"] = data["medias_ids"]

        rapport = Rapport.objects.create(
            type_rapport=data["type_rapport"],
            periode_debut=data["periode_debut"],
            periode_fin=data["periode_fin"],
            inclure_stats=data["inclure_stats"],
            inclure_graphiques=data["inclure_graphiques"],
            media=data.get("media"),
            genere_par=request.user,
            stats=stats_initiales,
        )

        services.lancer_generation(rapport.id)

        return Response(
            {
                "id": rapport.id,
                "statut": rapport.statut,
                "message": f"Génération démarrée. Utilisez /api/rapports/{rapport.id}/statut/ pour suivre la progression.",
                "timeout_secondes": rapport.timeout_secondes,
            },
            status=status.HTTP_201_CREATED,
        )


# ------------------------------------------------------------------
# 7.3 — GET /api/rapports/:id/statut/ — Polling (toutes les 5s côté front)
# ------------------------------------------------------------------
class RapportStatutView(APIView):
    permission_classes = [IsGestionnaireOrControleur]

    def get(self, request, pk):
        rapport = get_object_or_404(Rapport, pk=pk)
        _check_object_access(request.user, rapport)

        # Vérification paresseuse du timeout (pas de watchdog séparé — voir
        # rapports/services.py pour le détail de ce choix d'implémentation).
        if rapport.statut == Rapport.Statut.EN_COURS:
            ecoule = (timezone.now() - rapport.date_generation).total_seconds()
            if ecoule > rapport.timeout_secondes:
                rapport.statut = Rapport.Statut.ERREUR
                rapport.message_erreur = (
                    f"La génération a dépassé le délai maximum de {rapport.timeout_secondes} secondes."
                )
                rapport.save()

        if rapport.statut == Rapport.Statut.PRET:
            return Response({
                "id": rapport.id,
                "statut": rapport.statut,
                "progression": 100,
                "date_generation": rapport.date_generation.isoformat(),
            })

        if rapport.statut == Rapport.Statut.ERREUR:
            return Response({
                "id": rapport.id,
                "statut": rapport.statut,
                "message": rapport.message_erreur or "Erreur lors de la génération.",
            })

        ecoule = (timezone.now() - rapport.date_generation).total_seconds()
        progression = min(95, round(ecoule / rapport.timeout_secondes * 100))
        return Response({"id": rapport.id, "statut": rapport.statut, "progression": progression})


# ------------------------------------------------------------------
# 7.4 — GET /api/rapports/:id/ — Détail complet
# ------------------------------------------------------------------
class RapportDetailView(APIView):
    permission_classes = [IsGestionnaireOrControleur]

    def get(self, request, pk):
        rapport = get_object_or_404(Rapport.objects.select_related("media", "genere_par"), pk=pk)
        _check_object_access(request.user, rapport)

        base = {
            "id": rapport.id,
            "titre": rapport.titre,
            "type_rapport": rapport.type_rapport,
            "media_id": rapport.media_id,
            "media_nom": rapport.media.nom if rapport.media_id else None,
            "periode_debut": rapport.periode_debut.isoformat(),
            "periode_fin": rapport.periode_fin.isoformat(),
            "date_generation": rapport.date_generation.isoformat(),
            "genere_par_nom": rapport.genere_par.nom,
            "inclure_graphiques": rapport.inclure_graphiques,
            "inclure_stats": rapport.inclure_stats,
            "statut": rapport.statut,
        }
        base.update(rapport.stats or {})
        return Response(base)


# ------------------------------------------------------------------
# 7.5 — GET /api/rapports/:id/export/ — Téléchargement du PDF
# ------------------------------------------------------------------
class RapportExportView(APIView):
    permission_classes = [IsGestionnaireOrControleur]

    def get(self, request, pk):
        rapport = get_object_or_404(Rapport, pk=pk)
        _check_object_access(request.user, rapport)

        if rapport.statut != Rapport.Statut.PRET or not rapport.fichier_pdf:
            raise NotFound("Le PDF de ce rapport n'est pas encore disponible.")

        nom_fichier = f"{rapport.titre.lower().replace(' ', '-').replace('—', '-')}.pdf"
        try:
            return FileResponse(
                rapport.fichier_pdf.open("rb"),
                as_attachment=True,
                filename=nom_fichier,
                content_type="application/pdf",
            )
        except FileNotFoundError:
            raise Http404("Fichier PDF introuvable sur le serveur.")
