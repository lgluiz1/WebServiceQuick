# apps/webhooks/urls.py
from django.urls import path
from .views import buscar_dados , processar_dados_senac

urlpatterns = [
    path("buscar/senac/notas/", buscar_dados, name="notas"),
    path("processar/senac/notas/", processar_dados_senac, name="processar_notas"),
]