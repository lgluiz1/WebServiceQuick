from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularSwaggerView

from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path("admin/", admin.site.urls),

    # Redireciona raiz para /api/docs
    path('', lambda request: redirect('/api/docs/')),

    # JWT auth
    #path('api/token/', obtain_auth_token, name='api_token_auth'),

    # schema
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

    # APIs
    path("api/webhooks/", include("webhooks.urls")),
    path("api/webponto/", include("webponto.urls")),
    path("api/notafiscal/", include("notafiscal.urls")),
    #path("api/integracoes/", include("integracoes.urls")),

    # USUARIOS E AUTENTICAÇÃO
    path("user/", include("usuarios.urls")),


]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)