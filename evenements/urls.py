from django.urls import path

from .views import AudioVideoStatsView, ComparaisonStatsView, DashboardView, GlobalStatsView

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="stats_dashboard"),
    path("global/", GlobalStatsView.as_view(), name="stats_global"),
    path("audio-video/", AudioVideoStatsView.as_view(), name="stats_audio_video"),
    path("comparaison/", ComparaisonStatsView.as_view(), name="stats_comparaison"),
]
