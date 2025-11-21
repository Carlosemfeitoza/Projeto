from django.forms import ModelForm
from django import forms
from .models import Cliente, Cidade, Medico, Agendamento
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UsuarioCustomizado
from django.contrib.auth import get_user_model


class UsuarioCustomizadoCreationForm(UserCreationForm):
    class Meta:
        model = UsuarioCustomizado
        fields = [
            "username",
            "email",
            "cpf",
            "telefone",
            "endereco",
            "bairro",
            "cidade",
            "data_nascimento",
            "foto_perfil",
            "password1",
            "password2",
        ]


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


class PerfilForm(forms.ModelForm):
    class Meta:
        model = UsuarioCustomizado
        fields = [
            "first_name",
            "email",
            "cpf",
            "telefone",
            "endereco",
            "data_nascimento",
            "foto_perfil",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "cpf": forms.TextInput(attrs={"class": "form-control"}),
            "telefone": forms.TextInput(attrs={"class": "form-control"}),
            "endereco": forms.TextInput(attrs={"class": "form-control"}),
            "data_nascimento": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }


class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ["nome", "email", "cpf", "telefone", "endereco", "cidade", "foto"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "cpf": forms.TextInput(attrs={"class": "form-control"}),
            "telefone": forms.TextInput(attrs={"class": "form-control"}),
            "endereco": forms.TextInput(attrs={"class": "form-control"}),
            "cidade": forms.Select(attrs={"class": "form-control"}),
            "foto": forms.FileInput(attrs={"class": "form-control"}),
        }


class CidadeForm(ModelForm):
    class Meta:
        model = Cidade
        fields = "__all__"
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "sigla_estado": forms.TextInput(attrs={"class": "form-control"}),
        }


class MedicoForm(ModelForm):
    class Meta:
        model = Medico
        fields = [
            "nome",
            "registro_profissional",
            "cpf",
            "email",
            "telefone",
            "data_nascimento",
            "especialidade",
            "salario",
            "data_contratacao",
            "ativo",
        ]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "registro_profissional": forms.TextInput(attrs={"class": "form-control"}),
            "cpf": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "telefone": forms.TextInput(attrs={"class": "form-control"}),
            "data_nascimento": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "especialidade": forms.TextInput(attrs={"class": "form-control"}),
            "salario": forms.NumberInput(attrs={"class": "form-control"}),
            "data_contratacao": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "foto": forms.FileInput(attrs={"class": "form-control"}),
        }


class AgendamentoForm(ModelForm):
    class Meta:
        model = Agendamento
        fields = "__all__"
        widgets = {
            "cliente": forms.Select(attrs={"class": "form-control"}),
            "medico": forms.Select(attrs={"class": "form-control"}),
            "data_hora": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "motivo": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }
