from django.contrib import admin
from django.utils.html import format_html
from .models import Cliente, Cidade, Medico, Agendamento

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'endereco', 'email', 'cidade', 'foto_thumbnail')
    fields = ('nome', 'endereco', 'email', 'cpf', 'cidade', 'foto')

    def foto_thumbnail(self, obj):
        if obj.foto:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />',
                obj.foto.url
            )
        return "Sem foto"
    foto_thumbnail.short_description = 'Foto'


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'especialidade', 'email', 'telefone', 'ativo')
    fields = ('nome', 'cpf', 'email', 'telefone', 'data_nascimento', 'especialidade', 'salario', 'data_contratacao', 'ativo')


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'medico', 'data_hora', 'status')
    fields = ('cliente', 'medico', 'data_hora', 'motivo', 'status')
    list_filter = ('status', 'medico', 'data_hora')
    search_fields = ('cliente__nome', 'medico__nome')


@admin.register(Cidade)
class CidadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sigla_estado')