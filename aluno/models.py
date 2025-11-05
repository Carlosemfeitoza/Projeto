from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class UsuarioCustomizado(AbstractUser):
    cpf = models.CharField(max_length=11, unique=True, verbose_name="CPF", blank=True, null=True)
    email = models.EmailField(unique=True, verbose_name="E-mail")
    telefone = models.CharField(max_length=15, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='perfil/', null=True, blank=True)
    ativo = models.BooleanField(default=True)
    receber_notificacoes = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username} - {self.cpf}"

    def is_gerente(self):
        return self.groups.filter(name="GERENTE").exists()

    def is_user_simples(self):
        return self.groups.filter(name="USUARIO_SIMPLES").exists()


class Cidade(models.Model):
    nome = models.CharField(max_length=100)
    sigla_estado = models.CharField(max_length=2)

    def __str__(self):
        return self.nome + " - " + self.sigla_estado 

class Cliente(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cliente',
        null=True, blank=True
    )
    nome = models.CharField(max_length=150)
    email = models.EmailField(blank=True, null=True)
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    cidade = models.ForeignKey('Cidade', on_delete=models.SET_NULL, blank=True, null=True)
    foto = models.ImageField(upload_to='fotos_clientes/', blank=True, null=True)

    def __str__(self):
        return self.nome
    
class Medico(models.Model):
    nome = models.CharField(max_length=100)               
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField()
    telefone = models.CharField(max_length=15, blank=True)
    data_nascimento = models.DateField(blank=True, null=True)
    especialidade = models.CharField(max_length=100)
    salario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    data_contratacao = models.DateField(blank=True, null=True)
    registro_profissional = models.CharField(max_length=50, blank=True, null=True)  
    ativo = models.BooleanField(default=True)
    foto = models.ImageField(upload_to='medicos/', blank=True, null=True)

    def __str__(self):
        return self.nome
    
class Agendamento(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pendente'),
        ('C', 'Confirmado'),
        ('X', 'Cancelado'),
        ('F', 'Concluído'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='agendamentos')
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='agendamentos')
    data_hora = models.DateTimeField()
    motivo = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.status
    



