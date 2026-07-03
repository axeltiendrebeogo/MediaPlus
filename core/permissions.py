"""
Permissions par rôle — la vérification de rôle se fait TOUJOURS côté back-end
(jamais côté front uniquement), conformément au §9.2 du Cahier des Charges.

Rappel des rôles (§3 du CdC) :
- admin        : gestion des comptes et des médias. AUCUN accès aux données
                 analytiques (/stats/, /rapports/, /pages/).
- gestionnaire : accès en lecture/écriture limité à SON média uniquement.
- controleur   : accès à tous les médias, seul habilité à affecter un
                 gestionnaire à un média.
"""

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    message = "Réservé à l'administrateur."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "admin"
        )


class IsGestionnaire(BasePermission):
    message = "Réservé aux gestionnaires de média."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "gestionnaire"
        )


class IsControleur(BasePermission):
    message = "Réservé au contrôleur média."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "controleur"
        )


class IsGestionnaireOrControleur(BasePermission):
    """Accès aux données d'audience : Gestionnaire (son média) ou Contrôleur (tous)."""

    message = "Réservé aux gestionnaires et contrôleurs."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in ("gestionnaire", "controleur")
        )


class IsAdminOrControleur(BasePermission):
    """GET /api/medias/ : Admin (gestion) et Contrôleur (vue d'ensemble) — §8.3."""

    message = "Réservé à l'administrateur et au contrôleur."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in ("admin", "controleur")
        )


class IsOwnMediaGestionnaireOrControleur(BasePermission):
    """
    Permission au niveau objet pour les ressources liées à un média
    (pages, stats, rapports). Le gestionnaire ne peut accéder qu'aux
    objets de son propre média ; le contrôleur accède à tout.
    """

    message = "Vous n'avez pas accès aux données de ce média."

    def has_object_permission(self, request, view, obj):
        if request.user.role == "controleur":
            return True
        if request.user.role == "gestionnaire":
            media_id = getattr(obj, "media_id", None)
            return media_id == request.user.media_id
        return False
