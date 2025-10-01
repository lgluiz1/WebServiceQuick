from django.contrib import admin
from .models import Fretes

@admin.register(Fretes)
class FretesAdmin(admin.ModelAdmin):
    list_display = [
        "frete_id",
        "numero",
        "serie",
        "status",
        "data_emissao",
        "data_saida_entrada",
    ]
    list_filter = [
        "status",
        "data_emissao",
        "tipo_operacao",
    ]
    
