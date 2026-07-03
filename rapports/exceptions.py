from rest_framework.exceptions import APIException
from rest_framework import status


class RapportQuotaDepasse(APIException):
    """
    429 — Limite de génération de rapports atteinte (§7.5 du CdC).
    Le detail est défini comme un dict pour que DRF retourne EXACTEMENT
    la forme documentée : {"detail": "...", "retry_after": <secondes>}
    """

    status_code = status.HTTP_429_TOO_MANY_REQUESTS

    def __init__(self, retry_after_secondes, max_rapports, fenetre_heures):
        self.detail = {
            "detail": f"Limite de {max_rapports} rapports par tranche de {fenetre_heures} heures atteinte.",
            "retry_after": retry_after_secondes,
        }
