import logging

from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError, Throttled, AuthenticationFailed
from rest_framework_simplejwt.exceptions import InvalidToken

logger = logging.getLogger(__name__)

# Messages par défaut alignés sur le contrat API (§10.2 du CdC)
DEFAULT_MESSAGES = {
    400: "Données invalides",
    401: "Token invalide ou expiré",
    403: "Vous n'avez pas les droits nécessaires",
    404: "Ressource non trouvée",
    429: "Limite de requêtes atteinte",
    500: "Erreur interne — contactez l'administrateur",
}


def mediapulse_exception_handler(exc, context):
    """
    Reformate TOUTES les erreurs DRF selon le format documenté dans le contrat API :

      Erreur simple (401, 403, 404, 429, 500) :
        { "detail": "Message d'erreur explicite" }

      Erreur de validation (400) :
        { "detail": "Données invalides", "errors": { "champ": ["message"] } }

      Quota dépassé (429) :
        { "detail": "...", "retry_after": <secondes> }
    """
    response = drf_exception_handler(exc, context)

    # Cas non couvert par DRF (exception Python brute) -> 500 JSON propre
    if response is None:
        logger.exception("Erreur serveur non gérée : %s", exc)
        return Response(
            {"detail": DEFAULT_MESSAGES[500]},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    status_code = response.status_code

    # 400 — Erreur de validation : DRF renvoie directement {champ: [erreurs]}
    # On l'enveloppe dans la forme attendue par le contrat.
    if isinstance(exc, ValidationError) and status_code == 400:
        errors = response.data
        # Cas où le serializer renvoie déjà {"detail": "...", "errors": {...}}
        # (levé manuellement dans une vue) -> on ne touche à rien.
        if isinstance(errors, dict) and "detail" in errors and "errors" in errors:
            return response
        response.data = {"detail": DEFAULT_MESSAGES[400], "errors": errors}
        return response

    # 429 — Quota dépassé (Throttled standard DRF, si jamais utilisé)
    if isinstance(exc, Throttled):
        response.data = {
            "detail": DEFAULT_MESSAGES[429],
            "retry_after": int(exc.wait) if exc.wait is not None else None,
        }
        return response

    # Token JWT absent / invalide / expiré sur un endpoint protégé.
    # NB : InvalidToken hérite de AuthenticationFailed dans simplejwt — il
    # faut donc le tester AVANT le cas générique ci-dessous.
    if isinstance(exc, InvalidToken):
        response.data = {"detail": DEFAULT_MESSAGES[401]}
        return response

    # Échec de connexion (POST /api/token/) — email/mot de passe incorrects,
    # ou compte désactivé (is_active=False).
    if isinstance(exc, AuthenticationFailed):
        response.data = {"detail": "Email ou mot de passe incorrect."}
        return response

    # Cas où la vue a levé une APIException "maison" avec déjà
    # le bon format (ex: notre RapportQuotaDepasse) -> ne rien réécrire.
    if isinstance(response.data, dict) and "detail" in response.data:
        return response

    # Filet de sécurité générique pour tout le reste (401, 403, 404, ...)
    message = DEFAULT_MESSAGES.get(status_code, "Erreur")
    response.data = {"detail": message}
    return response
