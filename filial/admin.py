from django.contrib import admin
from .models import Filial

@admin.register(Filial)
class FilialAdmin(admin.ModelAdmin):
    list_display = ('documento', 'ie', 'nome', 'endereco', 'bairro', 'cidade', 'uf', 'cep', 'telefone', 'email')
    search_fields = ('documento', 'ie', 'nome', 'cidade', 'uf', 'email')
    list_filter = ('uf', 'cidade')
