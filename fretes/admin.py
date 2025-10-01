# fretes/admin.py
from django.contrib import admin
from .models import Frete

@admin.register(Frete)
class FreteAdmin(admin.ModelAdmin):
    list_display = ('frete_id', 'chave', 'numero', 'serie', 'valor', 'data_emissao', 'status')
    list_filter = ('status', 'data_emissao')
    search_fields = ('frete_id', 'chave')