# apps/webhooks/urls.py
from django.urls import path
from .views import buscar_dados , processar_notas_senac, envio_unico_chave_senac

urlpatterns = [
    path("buscar/senac/notas/", buscar_dados, name="notas"),
    path("processar/senac/notas/", processar_notas_senac, name="processar_notas"),
    path("envio/unico/chave/senac/<str:chave_nfe>/", envio_unico_chave_senac, name="envio_unico_chave_senac"),
]