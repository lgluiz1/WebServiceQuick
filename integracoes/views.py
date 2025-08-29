from django.shortcuts import render
from notafiscal.models import IntegracaoSenac
from .functions import envia_para_senac_soap
from django.http import JsonResponse
from time import sleep

