from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.permissions import IsAdmin, IsAdminOrControleur
from .models import Media
from .serializers import (
    MediaCreateSerializer,
    MediaSerializer,
    MediaUpdateGestionnaireSerializer,
    MediaUpdateMetierSerializer,
)

ALLOWED_ORDERINGS = {"nom", "-nom", "date_creation", "-date_creation"}


# ------------------------------------------------------------------
# 4.1 / 4.2 — GET (liste) / POST (création) /api/medias/
# ------------------------------------------------------------------
class MediaListCreateView(generics.ListCreateAPIView):
    serializer_class = MediaSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdmin()]
        return [IsAdminOrControleur()]

    def get_queryset(self):
        qs = Media.objects.select_related("gestionnaire")

        statut = self.request.query_params.get("statut")
        if statut:
            qs = qs.filter(statut=statut)
        else:
            # Un média "soft delete" n'est plus accessible via l'API (§9.3 du
            # CdC) -> exclu des listes par défaut, sauf filtre explicite.
            qs = qs.exclude(statut=Media.Statut.SUPPRIME)

        type_media = self.request.query_params.get("type_media")
        if type_media:
            qs = qs.filter(type_media=type_media)

        sans_gestionnaire = self.request.query_params.get("sans_gestionnaire")
        if sans_gestionnaire is not None:
            if sans_gestionnaire.lower() == "true":
                qs = qs.filter(gestionnaire__isnull=True)
            elif sans_gestionnaire.lower() == "false":
                qs = qs.filter(gestionnaire__isnull=False)

        ordering = self.request.query_params.get("ordering")
        if ordering == "-visiteurs":
            qs = qs.annotate(
                visiteurs_count=Count("pages__evenements__visiteur", distinct=True)
            ).order_by("-visiteurs_count")
        elif ordering in ALLOWED_ORDERINGS:
            qs = qs.order_by(ordering)

        return qs

    def get_serializer_class(self):
        return MediaCreateSerializer if self.request.method == "POST" else MediaSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        media = serializer.save()  # statut="actif" et gestionnaire=None par défaut
        return Response(MediaSerializer(media).data, status=status.HTTP_201_CREATED)


# ------------------------------------------------------------------
# GET détail / 4.3 + 4.4 PATCH (double comportement) / DELETE
# ------------------------------------------------------------------
class MediaDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Media, pk=pk)

    def get(self, request, pk):
        if request.user.role not in ("admin", "controleur"):
            raise PermissionDenied("Vous n'avez pas accès au détail des médias.")
        media = self.get_object(pk)
        return Response(MediaSerializer(media).data)

    def patch(self, request, pk):
        media = self.get_object(pk)
        role = request.user.role

        if role == "admin":
            if "gestionnaire_id" in request.data:
                raise PermissionDenied(
                    "Vous n'avez pas les droits pour modifier l'affectation du gestionnaire."
                )
            serializer = MediaUpdateMetierSerializer(media, data=request.data, partial=True)

        elif role == "controleur":
            champs_interdits = set(request.data.keys()) - {"gestionnaire_id"}
            if champs_interdits:
                raise PermissionDenied(
                    "Vous n'avez pas les droits pour modifier les informations métier du média."
                )
            serializer = MediaUpdateGestionnaireSerializer(media, data=request.data, partial=True)

        else:
            raise PermissionDenied("Vous n'avez pas les droits pour modifier un média.")

        serializer.is_valid(raise_exception=True)
        serializer.save()
        media.refresh_from_db()
        return Response(MediaSerializer(media).data)

    def delete(self, request, pk):
        if request.user.role != "admin":
            raise PermissionDenied("Réservé à l'administrateur.")

        media = self.get_object(pk)
        mode = request.query_params.get("mode")
        if mode not in ("hard", "soft"):
            raise ValidationError({"mode": ["Paramètre requis : 'hard' ou 'soft'."]})

        if mode == "soft":
            media.statut = Media.Statut.SUPPRIME
            media.save(update_fields=["statut"])
        else:
            # Hard delete : le média, ses pages et événements sont supprimés
            # en cascade (FK on_delete=CASCADE). Les rapports liés aussi.
            # Les Visiteur ne sont retirés que s'ils n'ont AUCUN autre
            # événement restant ailleurs sur la plateforme (§9.3 du CdC).
            from evenements.models import Evenement, Visiteur

            visiteur_ids = list(
                Evenement.objects.filter(page__media=media)
                .values_list("visiteur_id", flat=True)
                .distinct()
            )
            media.delete()
            Visiteur.objects.filter(id__in=visiteur_ids).exclude(
                id__in=Evenement.objects.values_list("visiteur_id", flat=True)
            ).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
