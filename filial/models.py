from django.db import models

class Filial(models.Model):
    documento = models.CharField(max_length=14, unique=True)
    ie = models.CharField(max_length=14)
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)
    cep = models.CharField(max_length=9)
    telefone = models.CharField(max_length=14)
    email = models.EmailField()
    ultima_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome} "