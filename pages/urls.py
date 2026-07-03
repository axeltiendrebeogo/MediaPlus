from django.urls import path

from .views import PageDetailView, PageListView, PageStatsView

urlpatterns = [
    path("", PageListView.as_view(), name="page_list"),
    path("<int:pk>/", PageDetailView.as_view(), name="page_detail"),
    path("<int:pk>/stats/", PageStatsView.as_view(), name="page_stats"),
]
