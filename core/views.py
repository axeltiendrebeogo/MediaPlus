from rest_framework.response import Response
from rest_framework.views import APIView

from core.permissions import IsAdmin
from medias.models import Media
from rapports.models import Rapport
from users.models import User


class AdminDashboardView(APIView):
    """
    GET /api/admin/dashboard/ — Admin uniquement.

    ⚠️ Endpoint AJOUTÉ au-delà du contrat API strict, suite à la décision
    explicite : le dashboard Admin du front affichait des statistiques
    d'audience (visiteurs_total, trafic_7j...), ce qui contredit le CdC
    (§3.1/§9.2 : "L'admin n'a aucun accès aux données analytiques").
    Cet endpoint ne renvoie QUE des compteurs de gestion (aucune donnée
    d'audience/visiteur), pour que le dashboard Admin reste utile sans
    violer cette règle.
    """

    permission_classes = [IsAdmin]

    def get(self, request):
        return Response({
            "medias_actifs": Media.objects.filter(statut=Media.Statut.ACTIF).count(),
            "medias_total": Media.objects.exclude(statut=Media.Statut.SUPPRIME).count(),
            "utilisateurs_total": User.objects.filter(is_active=True).count(),
            "gestionnaires_total": User.objects.filter(role="gestionnaire", is_active=True).count(),
            "medias_sans_gestionnaire": Media.objects.exclude(statut=Media.Statut.SUPPRIME)
                .filter(gestionnaire__isnull=True).count(),
            "rapports_generes_total": Rapport.objects.filter(statut="pret").count(),
        })
