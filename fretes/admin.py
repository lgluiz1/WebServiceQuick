from django.contrib import admin
from .models import Fretes

@admin.register(Fretes)
class FretesAdmin(admin.ModelAdmin):
    list_display = ('frete_id', 'descricao', 'valor', 'data_criacao', 'status')
    list_filter = ('status', 'data_criacao')
    search_fields = ('frete_id', 'descricao')
