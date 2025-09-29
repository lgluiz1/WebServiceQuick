# apps/webhooks/urls.py
from django.urls import path
from .views import ReceberWebhookAPIView, ReceberWebhookNfeAPIView, ReceberWebhookManifestoAPIView

urlpatterns = [
    path("fretes/", ReceberWebhookAPIView.as_view(), name="webhook-fretes"),
    path("nfe/", ReceberWebhookNfeAPIView.as_view(), name="webhook-nfe"),
    path("manifesto/", ReceberWebhookManifestoAPIView.as_view(), name="webhook-manifesto"),
]