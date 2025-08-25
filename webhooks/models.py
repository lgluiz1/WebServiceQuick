# apps/webhooks/models.py
from django.db import models

class FretesWebhook(models.Model): 
    frete_id = models.CharField(max_length=255)  # id da NFE ou frete
    recebido_em = models.DateTimeField(auto_now_add=True)
    processado = models.BooleanField(default=False)
    erro = models.TextField(blank=True, null=True)
    payload = models.JSONField()  # corpo cru da requisição

    def __str__(self):
        return f"{self.frete_id} - {self.recebido_em.strftime('%d/%m/%Y %H:%M')} - {'Processado' if self.processado else 'Não processado'}"


    class Meta:
        verbose_name = "Frete Webhook"
        verbose_name_plural = "Fretes Webhooks"


class NfeWebhook(models.Model):
    numero_nfe = models.CharField(max_length=255)
    recebido_em = models.DateTimeField(auto_now_add=True)
    processado = models.BooleanField(default=False)
    erro = models.TextField(blank=True, null=True)
    payload = models.JSONField()

    def __str__(self):
        return f"{self.numero_nfe} - {self.recebido_em.strftime('%d/%m/%Y %H:%M')} - {'Processado' if self.processado else ' Não processado'}"
    
    class Meta:
        verbose_name = "NF-e Webhook" 
        verbose_name_plural = "NF-e Webhook"