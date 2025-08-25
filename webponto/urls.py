from .views import webponto
from django.urls import path


urlpatterns = [
    path('receber/', webponto, name='webponto')
]