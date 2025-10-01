from django.db import models

class Filial(models.Model):
    documento = models.CharField(max_length=14, unique=True)
    ie = models.CharField(max_length=14,blank=True, null=True)
    nome = models.CharField(max_length=100,blank=True, null=True)
    endereco = models.CharField(max_length=100,blank=True, null=True)
    bairro = models.CharField(max_length=100,blank=True, null=True)
    cidade = models.CharField(max_length=100,blank=True, null=True)
    uf = models.CharField(max_length=2,blank=True, null=True)
    cep = models.CharField(max_length=9,blank=True, null=True)
    telefone = models.CharField(max_length=14,blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    ultima_atualizacao = models.DateTimeField(auto_now=True,blank=True, null=True)

    def __str__(self):
        return f"{self.nome} "