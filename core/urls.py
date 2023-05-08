from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import settings
from .yasg import urlpatterns as doc_api


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include('users.urls')),
    path("api/v1/", include('transfer.urls')),
    path("api/v1/", include('market.urls')),
    path("api/v1/", include('achievement.urls')),

    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += doc_api
