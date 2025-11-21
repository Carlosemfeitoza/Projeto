from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth.models import Group
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Cliente, Agendamento, Cidade, Medico
from .forms import (
    ClienteForm,
    CidadeForm,
    MedicoForm,
    AgendamentoForm,
    UsuarioCustomizadoCreationForm,
    PerfilForm,
)


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuário", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        label="Senha", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


@login_required
def cliente_detalhar(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if not request.user.is_superuser and cliente.usuario != request.user:
        messages.error(request, "Você não tem permissão para visualizar este cliente.")
        return redirect("cliente_listar")

    return render(request, "cliente/cliente_detalhar.html", {"cliente": cliente})


@login_required
def cliente_editar(request, id):
    cliente = get_object_or_404(Cliente, id=id)

    if not (
        request.user.is_superuser
        or (hasattr(cliente, "usuario") and cliente.usuario == request.user)
    ):
        messages.error(request, "Você não tem permissão para acessar esta página.")
        return redirect("index")

    if request.method == "POST":
        form = ClienteForm(request.POST, request.FILES, instance=cliente)
        if form.is_valid():
            cliente = form.save()
            if cliente.usuario:
                user = cliente.usuario
                user.first_name = cliente.nome
                user.email = cliente.email or user.email
                user.cpf = cliente.cpf or user.cpf
                user.telefone = cliente.telefone or user.telefone
                user.endereco = cliente.endereco or user.endereco
                if cliente.foto:
                    user.foto_perfil = cliente.foto

                user.save()

            return redirect("cliente_listar")
    else:
        form = ClienteForm(instance=cliente)
    return render(request, "cliente/form.html", {"form": form})


@login_required
def cliente_remover(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if not (
        request.user.is_superuser
        or (hasattr(cliente, "usuario") and cliente.usuario == request.user)
    ):
        messages.error(request, "Você não tem permissão para executar esta ação.")
        return redirect("index")
    if hasattr(cliente, "usuario") and cliente.usuario == request.user:
        user_to_delete = cliente.usuario
        logout(request)
        user_to_delete.delete()
        messages.info(request, "Sua conta e perfil foram excluídos.")
        return redirect("login")
    cliente.delete()
    return redirect("cliente_listar")


@login_required
def cliente_criar(request):
    if not request.user.is_superuser:
        messages.error(request, "Você não tem permissão para acessar esta página.")
        return redirect("index")
    if request.method == "POST":
        form = ClienteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("cliente_listar")
    else:
        form = ClienteForm()
    return render(request, "cliente/form.html", {"form": form})


@login_required
def cliente_listar(request):
    qs = Cliente.objects.select_related("cidade").exclude(usuario__is_superuser=True)
    q = request.GET.get("q", "").strip()
    cidade_id = request.GET.get("cidade", "").strip()
    if q:
        qs = qs.filter(nome__icontains=q)
    if cidade_id:
        qs = qs.filter(cidade_id=cidade_id)
    paginator = Paginator(qs, 10)
    page_number = request.GET.get("page", 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    params = request.GET.copy()
    if "page" in params:
        params.pop("page")
    querystring = params.urlencode()
    context = {
        "page_obj": page_obj,
        "paginator": paginator,
        "is_paginated": page_obj.has_other_pages(),
        "querystring": querystring,
        "q": q,
        "cidade_selected": cidade_id,
        "cidades": Cidade.objects.all(),
        "clientes": page_obj.object_list,
    }
    return render(request, "cliente/clientes.html", context)


@login_required
def index(request):
    context = {
        "total_clientes": Cliente.objects.exclude(usuario__is_superuser=True).count(),
        "total_cidades": Cidade.objects.count(),
        "total_medicos": Medico.objects.count(),
        "total_agendamentos": Agendamento.objects.count(),
    }
    return render(request, "cliente/index.html", context)


@login_required
def agendamento_listar(request):
    qs = Agendamento.objects.select_related("cliente", "medico").all()
    if not request.user.is_superuser and hasattr(request.user, "cliente"):

        qs = qs.filter(cliente=request.user.cliente)
    cliente_id = request.GET.get("cliente", "").strip()
    medico_id = request.GET.get("medico", "").strip()
    status = request.GET.get("status", "").strip()
    start_date = request.GET.get("start_date", "").strip()
    end_date = request.GET.get("end_date", "").strip()

    if cliente_id:
        qs = qs.filter(cliente_id=cliente_id)
    if medico_id:
        qs = qs.filter(medico_id=medico_id)
    if status:
        qs = qs.filter(status=status)
    if start_date:
        qs = qs.filter(data_hora__date__gte=start_date)
    if end_date:
        qs = qs.filter(data_hora__date__lte=end_date)
    paginator = Paginator(qs, 10)
    page_number = request.GET.get("page", 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    params = request.GET.copy()
    if "page" in params:
        params.pop("page")
    querystring = params.urlencode()
    context = {
        "page_obj": page_obj,
        "paginator": paginator,
        "is_paginated": page_obj.has_other_pages(),
        "querystring": querystring,
        "cliente_selected": cliente_id,
        "medico_selected": medico_id,
        "status_selected": status,
        "start_date": start_date,
        "end_date": end_date,
        "clientes": Cliente.objects.all(),
        "medicos": Medico.objects.all(),
        "status_choices": Agendamento.STATUS_CHOICES,
        "agendamentos": page_obj.object_list,
    }

    return render(request, "agendamento/agendamentos.html", context)


@login_required
def agendamento_cadastrar(request):
    if request.method == "POST":
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("agendamento_listar")
    else:
        form = AgendamentoForm()
    return render(request, "agendamento/form.html", {"form": form})


@login_required
def agendamento_editar(request, id):
    agendamento = get_object_or_404(Agendamento, id=id)
    if not request.user.is_superuser and agendamento.cliente.usuario != request.user:
        return HttpResponseForbidden(
            "Você não tem permissão para editar este agendamento."
        )
    if request.method == "POST":
        form = AgendamentoForm(request.POST, instance=agendamento)
        if form.is_valid():
            form.save()
            return redirect("agendamento_listar")
    else:
        form = AgendamentoForm(instance=agendamento)

    return render(request, "agendamento/form.html", {"form": form})


@login_required
def agendamento_remover(request, id):
    agendamento = get_object_or_404(Agendamento, id=id)

    # Permissão
    if not request.user.is_superuser and agendamento.cliente.usuario != request.user:
        return HttpResponseForbidden(
            "Você não tem permissão para remover este agendamento."
        )

    if request.method == "POST":
        agendamento.delete()
        return redirect("agendamento_listar")

    # Se chegar aqui por GET, só redireciona para lista
    return redirect("agendamento_listar")


@login_required
def agendamento_detalhar(request, id):
    agendamento = get_object_or_404(Agendamento, id=id)
    if not request.user.is_superuser and agendamento.cliente.usuario != request.user:
        return HttpResponseForbidden(
            "Você não tem permissão para ver este agendamento."
        )

    return render(request, "agendamento/detalhes.html", {"agendamento": agendamento})


@login_required
def cidade_criar(request):
    if not request.user.is_superuser:
        messages.error(request, "Você não tem permissão para acessar esta página.")
        return redirect("index")
    if request.method == "POST":
        form = CidadeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("cidade_listar")
    else:
        form = CidadeForm()
    return render(request, "cidade/form.html", {"form": form})


@login_required
def cidade_editar(request, id):
    if not request.user.is_superuser:
        messages.error(request, "Você não tem permissão para acessar esta página.")
        return redirect("index")
    cidade = get_object_or_404(Cidade, id=id)
    if request.method == "POST":
        form = CidadeForm(request.POST, instance=cidade)
        if form.is_valid():
            form.save()
            return redirect("cidade_listar")
    else:
        form = CidadeForm(instance=cidade)
    return render(request, "cidade/form.html", {"form": form})


@login_required
def cidade_listar(request):
    qs = Cidade.objects.all()
    q = request.GET.get("q", "").strip()
    sigla = request.GET.get("sigla", "").strip()
    if q:
        qs = qs.filter(nome__icontains=q)
    if sigla:
        qs = qs.filter(sigla_estado__iexact=sigla)
    paginator = Paginator(qs, 10)
    page_number = request.GET.get("page", 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    params = request.GET.copy()
    if "page" in params:
        params.pop("page")
    querystring = params.urlencode()
    context = {
        "page_obj": page_obj,
        "paginator": paginator,
        "is_paginated": page_obj.has_other_pages(),
        "querystring": querystring,
        "q": q,
        "sigla": sigla,
        "cidades": page_obj.object_list,
    }
    return render(request, "cidade/cidade_listar.html", context)


@login_required
def cidade_remover(request, id):
    if not request.user.is_superuser:
        messages.error(request, "Você não tem permissão para acessar esta página.")
        return redirect("index")
    cidade = get_object_or_404(Cidade, id=id)
    cidade.delete()
    return redirect("cidade_listar")


@login_required
def medico_detalhar(request, id):
    medico = get_object_or_404(Medico, id=id)
    return render(request, "medico/medico_detalhes.html", {"medico": medico})


@login_required
def medico_listar(request):
    qs = Medico.objects.all()
    q = request.GET.get("q", "").strip()
    especialidade = request.GET.get("especialidade", "").strip()
    ativo = request.GET.get("ativo", "").strip()
    if q:
        qs = qs.filter(nome__icontains=q)
    if especialidade:
        qs = qs.filter(especialidade__icontains=especialidade)
    if ativo in ["0", "1"]:
        qs = qs.filter(ativo=(ativo == "1"))
    paginator = Paginator(qs, 10)
    page_number = request.GET.get("page", 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    params = request.GET.copy()
    if "page" in params:
        params.pop("page")
    querystring = params.urlencode()
    context = {
        "page_obj": page_obj,
        "paginator": paginator,
        "is_paginated": page_obj.has_other_pages(),
        "querystring": querystring,
        "q": q,
        "especialidade": especialidade,
        "ativo": ativo,
        "medicos": page_obj.object_list,
    }
    return render(request, "medico/medicos.html", context)


@login_required
def medico_cadastrar(request):
    if not request.user.is_superuser:
        messages.error(request, "Você não tem permissão para acessar esta página.")
        return redirect("index")
    if request.method == "POST":
        form = MedicoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("medico_listar")
    else:
        form = MedicoForm()
    return render(request, "medico/form.html", {"form": form})


@login_required
def medico_editar(request, id):
    if not request.user.is_superuser:
        messages.error(request, "Você não tem permissão para acessar esta página.")
        return redirect("index")
    medico = get_object_or_404(Medico, id=id)
    if request.method == "POST":
        form = MedicoForm(request.POST, request.FILES, instance=medico)
        if form.is_valid():
            form.save()
            return redirect("medico_listar")
    else:
        form = MedicoForm(instance=medico)
    return render(request, "medico/form.html", {"form": form})


@login_required
def medico_remover(request, id):
    if not request.user.is_superuser:
        messages.error(request, "Você não tem permissão para acessar esta página.")
        return redirect("index")
    medico = get_object_or_404(Medico, id=id)
    medico.delete()
    return redirect("medico_listar")


def cadastrar_usuario(request):
    if request.method == "POST":
        form = UsuarioCustomizadoCreationForm(request.POST, request.FILES)
        if form.is_valid():
            cpf = form.cleaned_data.get("cpf")
            # Checa se já existe um cliente com esse CPF
            cliente_existente = Cliente.objects.filter(cpf=cpf).first()

            # Cria o usuário
            user = form.save(commit=True)
            grupo_simples, _ = Group.objects.get_or_create(name="USUARIO_SIMPLES")
            user.groups.add(grupo_simples)

            # Apenas cria cliente se o usuário não for superuser
            if not user.is_superuser:
                if cliente_existente:
                    # Vincula o usuário existente ao cliente existente
                    cliente_existente.usuario = user
                    cliente_existente.nome = (
                        user.get_full_name() or cliente_existente.nome
                    )
                    cliente_existente.email = user.email or cliente_existente.email
                    cliente_existente.telefone = (
                        user.telefone or cliente_existente.telefone
                    )
                    cliente_existente.endereco = (
                        user.endereco or cliente_existente.endereco
                    )
                    if getattr(user, "cidade", None):
                        cliente_existente.cidade = user.cidade
                    if getattr(user, "foto_perfil", None):
                        cliente_existente.foto = user.foto_perfil
                    cliente_existente.save()
                else:
                    # Cria um cliente novo vinculado a esse usuário
                    Cliente.objects.create(
                        usuario=user,
                        nome=user.get_full_name() or user.username,
                        email=user.email,
                        cpf=user.cpf,
                        telefone=user.telefone,
                        endereco=user.endereco,
                        cidade=getattr(user, "cidade", None),
                        foto=getattr(user, "foto_perfil", None),
                    )

            messages.success(
                request, "Cadastro realizado com sucesso! Faça login para continuar."
            )
            return redirect("login")
    else:
        form = UsuarioCustomizadoCreationForm()

    return render(request, "usuarios/cadastrar.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bem-vindo, {user.username}!")
                return redirect("index")
            else:
                messages.error(request, "Usuário ou senha inválidos.")
    else:
        form = LoginForm(request)
    return render(request, "usuarios/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "Você saiu do sistema.")
    return redirect("login")


@login_required
def perfil_view(request):
    if request.method == "POST":
        form = PerfilForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            with transaction.atomic():
                user = form.save()

                # Apenas cria ou atualiza cliente se o usuário não for superuser
                if not user.is_superuser:
                    cliente, created = Cliente.objects.get_or_create(
                        usuario=user,
                        defaults={
                            "nome": user.get_full_name() or user.username,
                            "email": user.email or "",
                            "cpf": getattr(user, "cpf", "") or "",
                            "telefone": getattr(user, "telefone", "") or "",
                            "endereco": getattr(user, "endereco", "") or "",
                        },
                    )
                    cliente.nome = user.get_full_name() or user.username
                    cliente.email = user.email or cliente.email
                    if getattr(user, "cpf", None):
                        cliente.cpf = user.cpf
                    cliente.telefone = getattr(user, "telefone", cliente.telefone)
                    cliente.endereco = getattr(user, "endereco", cliente.endereco)
                    user_cidade = getattr(user, "cidade", None)
                    if user_cidade:
                        if isinstance(user_cidade, Cidade):
                            cliente.cidade = user_cidade
                        else:
                            try:
                                cidade_obj = Cidade.objects.filter(
                                    nome__iexact=str(user_cidade)
                                ).first()
                                if cidade_obj:
                                    cliente.cidade = cidade_obj
                            except Exception:
                                pass
                    if getattr(user, "foto_perfil", None):
                        cliente.foto = user.foto_perfil
                    cliente.save()

            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect("perfil")
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = PerfilForm(instance=request.user)
    return render(request, "usuarios/perfil.html", {"form": form})


@login_required
def search(request):
    q = request.GET.get("q", "").strip()
    clientes = []
    medicos = []
    cidades = []
    agendamentos = []
    total = 0
    if q:
        clientes_qs = Cliente.objects.filter(
            Q(nome__icontains=q) | Q(email__icontains=q) | Q(cpf__icontains=q)
        )
        medicos_qs = Medico.objects.filter(
            Q(nome__icontains=q)
            | Q(email__icontains=q)
            | Q(cpf__icontains=q)
            | Q(especialidade__icontains=q)
        )
        cidades_qs = Cidade.objects.filter(nome__icontains=q)
        agendamentos_qs = Agendamento.objects.select_related(
            "cliente", "medico"
        ).filter(
            Q(motivo__icontains=q)
            | Q(cliente__nome__icontains=q)
            | Q(medico__nome__icontains=q)
            | Q(status__icontains=q)
        )
        clientes = list(clientes_qs[:10])
        medicos = list(medicos_qs[:10])
        cidades = list(cidades_qs[:10])
        agendamentos = list(agendamentos_qs[:10])
        total = (
            clientes_qs.count()
            + medicos_qs.count()
            + cidades_qs.count()
            + agendamentos_qs.count()
        )
    context = {
        "q": q,
        "clientes": clientes,
        "medicos": medicos,
        "cidades": cidades,
        "agendamentos": agendamentos,
        "total": total,
    }
    return render(request, "busca/resultados.html", context)
