from django.contrib import admin
from django.urls import path
from app_starhub import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cadastro/', views.cadastro,name='cadastro'),
    path('', views.index, name='index'),
    path('inicio/', views.inicio, name='inicio'),
    path('curriculo/', views.upload_curriculo, name='curriculo'),  # <-- aqui a view correta!
    path('usuarios/', views.usuarios, name='listagem_usuarios'),
    path('perfil/', views.perfil, name='perfil'),
    path('login/', views.login, name='login'),
    path('cadastro_empresa/', views.cadastro_empresa, name='cadastro_empresa'),
    path('inicio_empresa/', views.inicio_empresa, name='inicio_empresa'),
    path('postar_vagas/', views.postar_vagas, name='postar_vagas'),
    path('vagas/', views.vagas, name='vagas'),
    path('vaga/<int:id>/', views.detalhes_vaga, name='detalhes_vaga'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)