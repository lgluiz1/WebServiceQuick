from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('email', 'nome', 'perfil', 'telefone', 'cpf', 'filial' )
    search_fields = ('email', 'nome', 'cpf', 'telefone')
    list_filter = ('perfil', 'filial')
