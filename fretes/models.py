from django.db import models


class Fretes(models.Model):
    frete_id = models.CharField(max_length=20, unique=True)  # aumentei p/ segurança
    recebido_em = models.DateTimeField(auto_now_add=True)

    tipo_frete = models.CharField(max_length=20, blank=True, null=True)
    previsao_entrega = models.CharField(max_length=20, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)

    agente_entrega = models.CharField(max_length=100, blank=True, null=True)

    numero_nfe = models.CharField(max_length=20, blank=True, null=True)
    serie_nfe = models.CharField(max_length=10, blank=True, null=True)
    chave_nfe = models.TextField(blank=True, null=True)  # era 255

    data_emissao_nfe = models.CharField(max_length=20, blank=True, null=True)
    id_nfe = models.CharField(max_length=20, blank=True, null=True)

    cte_id = models.CharField(max_length=20, blank=True, null=True)
    cte_numero = models.CharField(max_length=20, blank=True, null=True)
    cte_key = models.TextField(blank=True, null=True)  # era 255
    data_emissao_cte = models.CharField(max_length=20, blank=True, null=True)

    minuta_id = models.CharField(max_length=20, blank=True, null=True)
    minuta_numero = models.CharField(max_length=20, blank=True, null=True)
    minuta_data_emissao = models.CharField(max_length=20, blank=True, null=True)

    doc_remetente = models.CharField(max_length=20, blank=True, null=True)
    nome_remetente = models.CharField(max_length=100, blank=True, null=True)

    doc_destinatario = models.CharField(max_length=20, blank=True, null=True)
    nome_destinatario = models.CharField(max_length=100, blank=True, null=True)

    cidade_destino = models.CharField(max_length=100, blank=True, null=True)
    uf_destino = models.CharField(max_length=5, blank=True, null=True)
    cep_destino = models.CharField(max_length=15, blank=True, null=True)

    endereco_destino = models.CharField(max_length=255, blank=True, null=True)
    bairro_destino = models.CharField(max_length=100, blank=True, null=True)
    tel_destinatario = models.CharField(max_length=20, blank=True, null=True)
    email_destinatario = models.CharField(max_length=100, blank=True, null=True)

    manifesto_id = models.CharField(max_length=20, blank=True, null=True)
    manifesto_numero = models.CharField(max_length=20, blank=True, null=True)
    manifesto_data_emissao = models.CharField(max_length=20, blank=True, null=True)

    motorista = models.CharField(max_length=100, blank=True, null=True)
    doc_motorista = models.CharField(max_length=20, blank=True, null=True)
    veiculo_placa = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        verbose_name = "Frete"
        verbose_name_plural = "Fretes"
