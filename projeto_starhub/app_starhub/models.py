from django.db import models

class Usuario(models.Model):
    TIPO_USUARIO = [
        ('usuario', 'Usuário'),
        ('empresa', 'Empresa'),
    ]
    
    id_usuario = models.AutoField(primary_key=True)
    nome = models.TextField(max_length=255)
    sobrenome = models.TextField(max_length=255)
    email = models.EmailField(unique=True)
    senha = models.TextField(255)
    imagem = models.ImageField(upload_to='perfil/', null=True, blank=True)
    contato = models.CharField(max_length=20, null=True, blank=True)
    descricao = models.TextField(null=True, blank=True)
    cargo = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.nome} {self.sobrenome} ({self.tipo})'

class Curriculo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='curriculos', null=True, blank=True)
    arquivo = models.FileField(upload_to='curriculos/')
    data_envio = models.DateTimeField(auto_now_add=True)
    
class Empresa(models.Model):
    id_empresa = models.AutoField(primary_key=True)
    email_empresa = models.EmailField(unique=True)
    nome_empresa = models.CharField(max_length=50)
    local = models.CharField()
    cpf = models.CharField(max_length=14)
    pais = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    cidade = models.CharField(max_length=50)
    endereco = models.CharField(max_length=120)
    contato_empresa = models.IntegerField(null=True, blank=True)
    logo = models.ImageField(upload_to='perfil/', null=True, blank=True)
    descricao_empresa = models.TextField(null=True, blank=True)
    senha_empresa = models.CharField(max_length=255)

class Vaga(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='vagas')
    titulo = models.CharField(max_length=100)
    horario = models.TimeField()
    bolsa = models.FloatField()
    local = models.CharField(max_length=100)
    descricao = models.TextField()
    
    
