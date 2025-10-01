from django.contrib import admin
from .models import Fretes

@admin.register(Fretes)
class FretesAdmin(admin.ModelAdmin):
    list_display = ('frete_id', 'recebido_em', 'processado', 'erro')
    list_filter = ('status', 'recebido_em', 'processado')
    search_fields = ('frete_id',)
    
