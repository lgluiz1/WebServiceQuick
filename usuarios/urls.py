from django.urls import path
from . import views

urlpatterns = [
    path("ativar-conta/<str:token>/", views.ativar_conta, name="ativar-conta"),
]