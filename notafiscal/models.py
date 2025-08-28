from django.db import models

class NotaFiscal(models.Model):
    chave = models.CharField(max_length=250,blank=True, null=True)
    numero = models.CharField(max_length=20, unique=True)
    serie = models.CharField(max_length=5, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    data_emissao = models.DateTimeField()
    data_saida_entrada = models.DateTimeField(blank=True, null=True)
    tipo_operacao = models.CharField(max_length=20, blank=True, null=True)  # entrada / saída
    valor_total_produtos = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    valor_total_nota = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    peso_total_nota = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    nome_emitente = models.CharField(max_length=50,blank=True, null=True)
    documento_emitente = models.CharField(max_length=15,blank=True, null=True)
    nome_destinatario =  models.CharField(max_length=50,blank=True, null=True)
    documento_destinatario = models.CharField(max_length=15,blank=True, null=True)
    endereco_destinatario = models.CharField(max_length=100,blank=True, null=True)
    bairro_destinatario = models.CharField(max_length=20,blank=True, null=True)
    cidade_destinatario = models.CharField(max_length=20,blank=True, null=True)
    uf_destinatario = models.CharField(max_length=2,blank=True, null=True)
    cep_destinatario = models.CharField(max_length=10,blank=True, null=True)
    telefone_destinatario = models.CharField(max_length=11,blank=True, null=True)
    email_destinatario = models.EmailField(max_length=50,blank=True, null=True)
    url_comprovante = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = 'Nota Fiscal'
        verbose_name_plural = 'Notas Fiscais'
    

    def __str__(self):
        return f"NFe {self.numero} - {self.status} - {self.data_emissao.strftime('%d/%m/%Y')}"


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