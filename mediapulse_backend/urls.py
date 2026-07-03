from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from users.urls import auth_urlpatterns, users_urlpatterns
from core.views import AdminDashboardView

urlpatterns = [
    path("admin/", admin.site.urls),

    # --- 2. Authentification ---
    path("api/", include(auth_urlpatterns)),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # --- 3. Utilisateurs (Admin) ---
    path("api/users/", include(users_urlpatterns)),

    # --- Dashboard Admin (compteurs de gestion uniquement, voir core/views.py) ---
    path("api/admin/dashboard/", AdminDashboardView.as_view(), name="admin_dashboard"),

    # --- 4. Médias / 5. Pages / 6. Statistiques / 7. Rapports ---
    # (branchés au fur et à mesure de leur implémentation)
    path("api/medias/", include("medias.urls")),
    path("api/pages/", include("pages.urls")),
    path("api/stats/", include("evenements.urls")),
    path("api/rapports/", include("rapports.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
