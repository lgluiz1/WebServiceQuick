from django.contrib import admin
from .models import FretesWebhook, NfeWebhook, ManifestoWebhook

@admin.register(FretesWebhook)
class FretesWebhookAdmin(admin.ModelAdmin):
    list_display = ('frete_id', 'recebido_em', 'processado', 'processado_em', 'erro')
    list_filter = ('processado', 'recebido_em')
    search_fields = ('frete_id',)
@admin.register(ManifestoWebhook)
class ManifestoWebhookAdmin(admin.ModelAdmin):
    list_display = ('manifesto_numero', 'recebido_em', 'processado', 'processado_em', 'erro')
    list_filter = ('processado', 'recebido_em', 'processado_em')
    search_fields = ('manifesto_numero',)
@admin.register(NfeWebhook)
class NfeWebhookAdmin(admin.ModelAdmin):
    list_display = ('numero_nfe', 'recebido_em', 'processado', 'processado_em', 'erro')
    list_filter = ('processado', 'recebido_em')
    search_fields = ('numero_nfe',)


