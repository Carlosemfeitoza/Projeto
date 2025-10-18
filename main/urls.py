from django.contrib import admin
from django.urls import path
from aluno.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('cadastrar/', cadastrar_usuario, name='cadastrar_usuario'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('perfil/', perfil_view, name='perfil'),
    path('cliente/listar/', cliente_listar, name='cliente_listar'),
    path('cliente/criar/', cliente_criar, name='cliente_criar'),
    path('cliente/editar/<int:id>/', cliente_editar, name='cliente_editar'),
    path('cliente/remover/<int:id>/', cliente_remover, name='cliente_remover'),
    path('agendamento/listar/', agendamento_listar, name='agendamento_listar'),
    path('agendamento/cadastrar/', agendamento_cadastrar, name='agendamento_cadastrar'),
    path('agendamento/editar/<int:id>/', agendamento_editar, name='agendamento_editar'),
    path('agendamento/remover/<int:id>/', agendamento_remover, name='agendamento_remover'),
    path('agendamento/detalhar/<int:id>/', agendamento_detalhar, name='agendamento_detalhar'),
    path('cidade/listar/', cidade_listar, name='cidade_listar'),
    path('cidade/criar/', cidade_criar, name='cidade_criar'),
    path('cidade/editar/<int:id>/', cidade_editar, name='cidade_editar'),
    path('cidade/remover/<int:id>/', cidade_remover, name='cidade_remover'),
    path('medico/listar/', medico_listar, name='medico_listar'),
    path('medico/criar/', medico_cadastrar, name='medico_criar'),
    path('medico/editar/<int:id>/', medico_editar, name='medico_editar'),
    path('medico/remover/<int:id>/', medico_remover, name='medico_remover'),
    path('search/', search, name='search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
