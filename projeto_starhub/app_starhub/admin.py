from django.contrib import admin
from .models import Usuario, Empresa, Vaga, Curriculo

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'nome', 'sobrenome', 'email', 'senha')  

@admin.register(Curriculo)
class CurriculoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'data_envio')
    
@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('id_empresa', 'nome_empresa', 'email_empresa', 'local', 'pais', 'estado', 'cidade', 'contato_empresa')
    search_fields = ('nome', 'cidade', 'estado', 'pais')
    list_filter = ('estado', 'pais')

@admin.register(Vaga)
class VagaAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'empresa', 'bolsa', 'local', 'horario')
    search_fields = ('titulo', 'local', 'empresa__nome')
    list_filter = ('local', 'empresa')
    
    
