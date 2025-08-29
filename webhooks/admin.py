from django.contrib import admin
from .models import FretesWebhook, NfeWebhook

admin.site.register(FretesWebhook)
@admin.register(NfeWebhook)
class NfeWebhookAdmin(admin.ModelAdmin):
    list_display = ('numero_nfe', 'recebido_em', 'processado', 'erro')
    list_filter = ('processado', 'recebido_em')
    search_fields = ('numero_nfe',)


