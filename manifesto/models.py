from django.db import models
from django.utils import timezone


# -----------------------
# Manifesto organizado
# -----------------------
class Manifesto(models.Model):
    manifesto_numero = models.CharField(max_length=255, unique=True)
    manifesto_id = models.CharField(max_length=50,null=True, blank=True)
    data_emissao = models.DateField(null=True, blank=True)
    filial_embarque = models.CharField(max_length=255,null=True, blank=True)
    autor_documento = models.CharField(max_length=255,null=True, blank=True)
    filial_origem = models.CharField(max_length=255,null=True, blank=True)
    filial_destino = models.CharField(max_length=255,null=True, blank=True)
    estado_origem = models.CharField(max_length=2,null=True, blank=True)
    estado_destino = models.CharField(max_length=2,null=True, blank=True)
    cidade_descarregamento = models.CharField(max_length=255,null=True, blank=True)
    estado_passagem = models.CharField(max_length=2, blank=True, null=True)
    cidade_passagem = models.CharField(max_length=255, blank=True, null=True)
    tipo_do_contrato = models.CharField(max_length=50,null=True, blank=True)
    status = models.CharField(max_length=50,null=True, blank=True)
    agente_responsavel = models.CharField(max_length=255,null=True, blank=True)
    tipo_manifesto = models.CharField(max_length=50,null=True, blank=True)
    qtd_volumes = models.IntegerField(null=True, blank=True)
    qtd_destinos = models.IntegerField(null=True, blank=True)
    qtd_notas = models.IntegerField(null=True, blank=True)
    peso_total = models.FloatField(null=True, blank=True)
    peso_taxado = models.FloatField(null=True, blank=True)
    valor_total = models.FloatField(null=True, blank=True)
    motorista = models.CharField(max_length=255,null=True, blank=True)
    veiculo_placa = models.CharField(max_length=20,null=True, blank=True)
    motorista_cpf = models.CharField(max_length=14,null=True, blank=True)
    motorista_cnh = models.CharField(max_length=20,null=True, blank=True)
    previsao_saida = models.DateTimeField(null=True, blank=True)
    previsao_entrega = models.DateField(null=True, blank=True)
    observacoes_operacionais = models.TextField(blank=True , null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True) # Atualiza sempre que o registro é salvo

    def __str__(self):
        return f"Manifesto {self.manifesto_numero} - {self.atualizado_em.strftime('%d/%m/%Y %H:%M')}"


# -----------------------
# Modelos do manifesto (transferência, coleta, etc)
# -----------------------
class ManifestoModelo(models.Model):
    manifesto = models.ForeignKey(Manifesto, related_name="modelos", on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50,null=True, blank=True)
    qtd = models.IntegerField(null=True, blank=True)
    atualizado_em = models.DateTimeField(auto_now=True) # Atualiza sempre que o registro é salvo

    def __str__(self):
        return f"{self.manifesto.manifesto_numero} - {self.tipo} - {self.atualizado_em.strftime('%d/%m/%Y %H:%M')}"


# -----------------------
# Descarregamentos
# -----------------------
class Descarregamento(models.Model):
    manifesto = models.ForeignKey(Manifesto, related_name="descarregamentos", on_delete=models.CASCADE)
    local = models.CharField(max_length=255 , )
    data_hora = models.DateTimeField(null=True, blank=True)
    qtd_volumes = models.IntegerField(null=True, blank=True)
    peso_total = models.FloatField(null=True, blank=True)
    qtd_notas = models.IntegerField(null=True, blank=True)
    valor_total = models.FloatField(null=True, blank=True)
    atualizado_em = models.DateTimeField(auto_now=True) # Atualiza sempre que o registro é salvo

    def __str__(self):
        return f"{self.manifesto.manifesto_numero} - {self.local} - {self.atualizado_em.strftime('%d/%m/%Y %H:%M')}"


# -----------------------
# Minutas
# -----------------------
class Minuta(models.Model):
    manifesto = models.ForeignKey(Manifesto, related_name="minutas", on_delete=models.CASCADE)
    minuta_id = models.CharField(max_length=50,null=True, blank=True)
    minuta_numero = models.CharField(max_length=50,null=True, blank=True)
    data_emissao = models.DateField(null=True, blank=True)
    atualizado_em = models.DateTimeField(auto_now=True) # Atualiza sempre que o registro é salvo
    def __str__(self):
        return f"{self.manifesto.manifesto_numero} - {self.minuta_numero} - {self.atualizado_em.strftime('%d/%m/%Y %H:%M')}"


# -----------------------
# Resumo por natureza
# -----------------------
class ResumoNatureza(models.Model):
    manifesto = models.ForeignKey(Manifesto, related_name="resumo_naturezas", on_delete=models.CASCADE)
    natureza = models.CharField(max_length=255,null=True, blank=True)
    qtd = models.IntegerField(null=True, blank=True)
    atualizado_em = models.DateTimeField(auto_now=True) # Atualiza sempre que o registro é salvo
    def __str__(self):
        return f"{self.manifesto.manifesto_numero} - {self.natureza} - {self.atualizado_em.strftime('%d/%m/%Y %H:%M')}"
