from django.urls import path

from .views import MediaDetailView, MediaListCreateView

urlpatterns = [
    path("", MediaListCreateView.as_view(), name="media_list_create"),
    path("<int:pk>/", MediaDetailView.as_view(), name="media_detail"),
]
