from django.contrib import admin
from .models import Manifesto, Minuta, ResumoNatureza, Descarregamento, ManifestoModelo

@admin.register(Manifesto)
class ManifestoAdmin(admin.ModelAdmin):
    list_display = ('manifesto_numero', 'data_emissao', 'filial_origem', 'filial_destino', 'status', 'motorista', 'veiculo_placa', 'qtd_volumes', 'peso_total', 'valor_total', 'criado_em', 'atualizado_em')
    list_filter = ('status', 'filial_origem', 'filial_destino', 'data_emissao', 'criado_em', 'atualizado_em')
    search_fields = ('manifesto_numero', 'motorista', 'veiculo_placa')
    
@admin.register(Minuta)
class MinutaAdmin(admin.ModelAdmin):
    list_display = ('minuta_numero', 'manifesto', 'data_emissao', 'atualizado_em')
    list_filter = ('data_emissao', 'atualizado_em')
    search_fields = ('minuta_numero', 'manifesto__manifesto_numero')

@admin.register(ResumoNatureza)
class ResumoNaturezaAdmin(admin.ModelAdmin):
    list_display = ('manifesto', 'natureza', 'qtd', 'atualizado_em')
    list_filter = ('natureza', 'atualizado_em')
    search_fields = ('manifesto__manifesto_numero', 'natureza')

@admin.register(Descarregamento)
class DescarregamentoAdmin(admin.ModelAdmin):
    list_display = ('manifesto', 'local', 'data_hora', 'qtd_volumes', 'peso_total', 'qtd_notas', 'valor_total', 'atualizado_em')
    list_filter = ('local', 'data_hora', 'atualizado_em')
    search_fields = ('manifesto__manifesto_numero', 'local')

@admin.register(ManifestoModelo)
class ManifestoModeloAdmin(admin.ModelAdmin):
    list_display = ('manifesto', 'tipo', 'qtd', 'atualizado_em')
    list_filter = ('tipo', 'atualizado_em')
    search_fields = ('manifesto__manifesto_numero', 'tipo')

