from django.db import models
from filial.models import Filial

class Frete(models.Model):
    frete_id = models.CharField(max_length=50, unique=True)
    chave = models.CharField(max_length=44,blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)
    serie = models.IntegerField(blank=True, null=True)
    
    STATUS_CHOICES = [
        (1, "Entregue"),
        (2, "Cancelada"),
        (3, "Em trânsito"),
    ]
    status = models.IntegerField(choices=STATUS_CHOICES)

    filial_emissao = models.ForeignKey(Filial, on_delete=models.CASCADE, related_name="fretes_emitidos",blank=True, null=True)
    origem = models.ForeignKey(Filial, on_delete=models.CASCADE, related_name="fretes_origem",blank=True, null=True)
    destino = models.ForeignKey(Filial, on_delete=models.CASCADE, related_name="fretes_destino",blank=True, null=True)

    data_emissao = models.DateTimeField(blank=True, null=True)
    data_saida_entrada = models.DateTimeField(blank=True, null=True)
    tipo_operacao = models.CharField(max_length=50)
    modelo_frete = models.CharField(max_length=50,blank=True, null=True)
    valor_total_produtos = models.DecimalField(max_digits=12, decimal_places=2,blank=True, null=True)
    tipo_servico = models.CharField(max_length=50,blank=True, null=True)
    tipo_emissao = models.CharField(max_length=100,blank=True, null=True)
    valor_total_nota = models.DecimalField(max_digits=12, decimal_places=2,blank=True, null=True)
    peso_total_nota = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    url_comprovante = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Frete {self.frete_id} - Status: {self.get_status_display()}"
