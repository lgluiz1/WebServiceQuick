from django.utils.crypto import get_random_string
from django.db import models
from filial.models import Filial

# Cria perfil modelo de usuário personalizado finalizade usuario sistema , motoristas etc
class Usuario(models.Model):
    PERFIL_USUARIO = [
        ('admin', 'Administrador'),
        ('operador', 'Operador'),
        ('motorista', 'Motorista'),
        ('cliente', 'Cliente'),
    ]
    PERFIL_SEXO = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    ]
    CIDADES = [
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('AM', 'Amazonas'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MT', 'Mato Grosso'),
    ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PR', 'Paraná'),
    ('PE', 'Pernambuco'),
    ('PI', 'Piauí'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'),
    ('SE', 'Sergipe'),
    ('TO', 'Tocantins'),
    ]
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    tipo_perfil = models.CharField(max_length=20, choices=PERFIL_USUARIO)
    cpf = models.CharField(max_length=14, unique=True)
    rg = models.CharField(max_length=20, blank=True, null=True)
    data_emissao_rg = models.DateField(blank=True, null=True)
    orgao_emissor_rg = models.CharField(max_length=100, blank=True, null=True)
    cidade_emissao_rg = models.CharField(max_length=100, choices=CIDADES, blank=True, null=True)
    sexo = models.CharField(max_length=1, choices=PERFIL_SEXO, blank=True, null=True)
    filial = models.ForeignKey(Filial, on_delete=models.SET_NULL, blank=True, null=True) # Filial associada ao usuário
    ativo = models.BooleanField(default=True)
    data_nascimento = models.DateField(blank=True, null=True)
    cnh = models.CharField(max_length=20, blank=True, null=True)
    cnh_categoria = models.CharField(max_length=2, blank=True, null=True)
    cnh_validade = models.DateField(blank=True, null=True)
    endereco = models.CharField(max_length=200, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, choices=CIDADES, blank=True, null=True)
    uf = models.CharField(max_length=2, blank=True, null=True)
    cep = models.CharField(max_length=9, blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    nome_pai = models.CharField(max_length=100, blank=True, null=True)
    nome_mae = models.CharField(max_length=100, blank=True, null=True)
    token_ativacao = models.CharField(max_length=64, blank=True, null=True, unique=True)

    def gerar_token_ativacao(self):
        self.token_ativacao = get_random_string(48)
        self.save()
        return self.token_ativacao
    
    def __str__(self):
        return self.nome