from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from core.permissions import IsAdmin, IsAdminOrControleur
from .models import User
from .serializers import (
    MediaPulseTokenObtainPairSerializer,
    UserCreateSerializer,
    UserSerializer,
    UserUpdateSerializer,
)


# ------------------------------------------------------------------
# 2.1 — POST /api/token/ — Connexion
# ------------------------------------------------------------------
class LoginView(TokenObtainPairView):
    serializer_class = MediaPulseTokenObtainPairSerializer


# Le refresh (2.2 — POST /api/token/refresh/) n'a besoin d'aucune
# surcharge : le TokenRefreshView de simplejwt correspond déjà exactement
# au contrat ({"refresh": "..."} -> {"access": "..."}).
# Voir mediapulse_backend/urls.py pour le branchement direct.


# ------------------------------------------------------------------
# 2.3 — POST /api/auth/logout/ — Déconnexion (blackliste le refresh token)
# ------------------------------------------------------------------
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh = request.data.get("refresh")
        if not refresh:
            raise ValidationError({"refresh": ["Ce champ est requis."]})
        try:
            RefreshToken(refresh).blacklist()
        except TokenError:
            raise ValidationError({"refresh": ["Token de rafraîchissement invalide."]})
        return Response(status=status.HTTP_204_NO_CONTENT)


# ------------------------------------------------------------------
# 2.4 — GET /api/auth/me/ — Profil connecté
# ------------------------------------------------------------------
class MeView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


# ------------------------------------------------------------------
# 3. Utilisateurs (Admin uniquement)
# ------------------------------------------------------------------
class UserListCreateView(generics.ListCreateAPIView):
    """
    3.1 — GET  /api/users/  — Liste (filtres ?role= ?is_active= ?ordering=)
    3.2 — POST /api/users/  — Créer un compte (gestionnaire ou contrôleur)
    """

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdmin()]
        return [IsAdminOrControleur()]

    def get_queryset(self):
        qs = User.objects.all()

        role = self.request.query_params.get("role")
        if role:
            qs = qs.filter(role=role)

        is_active = self.request.query_params.get("is_active")
        if is_active is not None:
            qs = qs.filter(is_active=is_active.lower() == "true")

        ordering = self.request.query_params.get("ordering")
        allowed_orderings = {"nom", "-nom", "date_creation", "-date_creation"}
        if ordering in allowed_orderings:
            qs = qs.order_by(ordering)

        return qs

    def get_serializer_class(self):
        return UserCreateSerializer if self.request.method == "POST" else UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # La réponse 201 suit la forme complète documentée (id, media_id, media_nom...)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    3.3 — GET    /api/users/:id/ — Détail
    3.4 — PATCH  /api/users/:id/ — Modifier (nom, email, is_active uniquement)
    3.5 — DELETE /api/users/:id/ — Supprimer (média -> gestionnaire_id=null automatique)
    """

    permission_classes = [IsAdmin]
    queryset = User.objects.all()

    def get_serializer_class(self):
        return UserUpdateSerializer if self.request.method == "PATCH" else UserSerializer

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserUpdateSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserSerializer(instance).data)
