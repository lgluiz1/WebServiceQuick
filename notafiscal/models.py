from django.db import models
from fretes.models import Fretes

class NotaFiscal(models.Model):
    frete = models.ForeignKey(Fretes, on_delete=models.CASCADE, related_name="notas_fiscais")
    chave = models.CharField(max_length=44, unique=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    numero = models.IntegerField( blank=True, null=True)
    serie = models.IntegerField( blank=True, null=True)
    comprovante_existe = models.BooleanField(default=False)
    comprovante_url = models.URLField(max_length=500, blank=True, null=True)
    data_entrega = models.DateField(blank=True, null=True)


    def __str__(self):
        return f"NFe {self.numero}/{self.serie} - {self.chave}"

    class Meta:
        verbose_name = 'Nota Fiscal'
        verbose_name_plural = 'Notas Fiscais'

class IntegracaoSenac(models.Model):
    status = models.BooleanField(default=False)
    id_nota_fiscal = models.CharField(max_length=20,null=True,blank=True)
    chave_nfe = models.CharField(max_length=250, unique=True)
    dados = models.JSONField()
    erro = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'NF-e Integração Senac'
        verbose_name_plural = 'NF-es Integrações Senac'

    def __str__(self):
        return f"Senac - Nota Fiscal {self.id_nota_fiscal} Chave {self.chave_nfe[:5]} - {'Enviada' if self.status else 'Não Enviada'}"