from django.urls import path

from .views import LoginView, LogoutView, MeView, UserDetailView, UserListCreateView

# Authentification — montée sous /api/token/ et /api/auth/ dans le urls.py racine
auth_urlpatterns = [
    path("token/", LoginView.as_view(), name="token_obtain_pair"),
    path("auth/logout/", LogoutView.as_view(), name="auth_logout"),
    path("auth/me/", MeView.as_view(), name="auth_me"),
]

# Gestion des utilisateurs (Admin) — montée sous /api/users/
users_urlpatterns = [
    path("", UserListCreateView.as_view(), name="user_list_create"),
    path("<int:pk>/", UserDetailView.as_view(), name="user_detail"),
]
