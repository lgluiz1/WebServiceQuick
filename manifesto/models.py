from django.db import models
from django.utils import timezone


# -----------------------
# Manifesto organizado
# -----------------------
class Manifesto(models.Model):
    manifesto_numero = models.CharField(max_length=255, unique=True)
    manifesto_id = models.CharField(max_length=50)
    data_emissao = models.DateField()
    filial_embarque = models.CharField(max_length=255)
    autor_documento = models.CharField(max_length=255)
    filial_origem = models.CharField(max_length=255)
    filial_destino = models.CharField(max_length=255)
    estado_origem = models.CharField(max_length=2)
    estado_destino = models.CharField(max_length=2)
    cidade_descarregamento = models.CharField(max_length=255)
    estado_passagem = models.CharField(max_length=2, blank=True, null=True)
    cidade_passagem = models.CharField(max_length=255, blank=True, null=True)
    tipo_do_contrato = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    agente_responsavel = models.CharField(max_length=255)
    tipo_manifesto = models.CharField(max_length=50)
    qtd_volumes = models.IntegerField()
    qtd_destinos = models.IntegerField()
    qtd_notas = models.IntegerField()
    peso_total = models.FloatField()
    peso_taxado = models.FloatField()
    valor_total = models.FloatField()
    motorista = models.CharField(max_length=255)
    veiculo_placa = models.CharField(max_length=20)
    motorista_cpf = models.CharField(max_length=14)
    motorista_cnh = models.CharField(max_length=20)
    previsao_saida = models.DateTimeField()
    previsao_entrega = models.DateField()
    observacoes_operacionais = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Manifesto {self.manifesto_numero}"


# -----------------------
# Modelos do manifesto (transferência, coleta, etc)
# -----------------------
class ManifestoModelo(models.Model):
    manifesto = models.ForeignKey(Manifesto, related_name="modelos", on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)
    qtd = models.IntegerField()


# -----------------------
# Descarregamentos
# -----------------------
class Descarregamento(models.Model):
    manifesto = models.ForeignKey(Manifesto, related_name="descarregamentos", on_delete=models.CASCADE)
    local = models.CharField(max_length=255)
    data_hora = models.DateTimeField()
    qtd_volumes = models.IntegerField()
    peso_total = models.FloatField()
    qtd_notas = models.IntegerField()
    valor_total = models.FloatField()


# -----------------------
# Minutas
# -----------------------
class Minuta(models.Model):
    manifesto = models.ForeignKey(Manifesto, related_name="minutas", on_delete=models.CASCADE)
    minuta_id = models.CharField(max_length=50)
    minuta_numero = models.CharField(max_length=50)
    data_emissao = models.DateField()


# -----------------------
# Resumo por natureza
# -----------------------
class ResumoNatureza(models.Model):
    manifesto = models.ForeignKey(Manifesto, related_name="resumo_naturezas", on_delete=models.CASCADE)
    natureza = models.CharField(max_length=255)
    qtd = models.IntegerField()
