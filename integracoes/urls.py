# apps/webhooks/urls.py
from django.urls import path
from .views import integracao_senac

urlpatterns = [
   path("envio/senac/", integracao_senac, name="integracao_senac"),
]