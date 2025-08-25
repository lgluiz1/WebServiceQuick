from django.db import models

class Webponto(models.Model):
    data = models.DateField(blank=True, null=True)
    hora = models.TimeField(blank=True, null=True)
    id_funcionario = models.IntegerField(blank=True, null=True)  # ID da empresa
    nome = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'webponto'
