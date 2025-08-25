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



urlpatterns = [
    path("admin/", admin.site.urls),

    # Redireciona raiz para /api/docs
    path('', lambda request: redirect('/api/docs/')),


    # JWT auth
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # JWT auth
    #path('api/token/', obtain_auth_token, name='api_token_auth'),

    # schema
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

    # APIs
    path("api/webhooks/", include("webhooks.urls")),
]
