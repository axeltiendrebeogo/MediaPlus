from django.urls import path

from .views import (
    GenererRapportView,
    RapportDetailView,
    RapportExportView,
    RapportListView,
    RapportStatutView,
)

urlpatterns = [
    path("", RapportListView.as_view(), name="rapport_list"),
    path("generer/", GenererRapportView.as_view(), name="rapport_generer"),
    path("<int:pk>/", RapportDetailView.as_view(), name="rapport_detail"),
    path("<int:pk>/statut/", RapportStatutView.as_view(), name="rapport_statut"),
    path("<int:pk>/export/", RapportExportView.as_view(), name="rapport_export"),
]
