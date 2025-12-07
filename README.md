MedAgenda — Sistema de Agendamentos Médicos

Projeto desenvolvido utilizando o framework Django para criação de um sistema de gerenciamento de clientes, médicos, cidades e agendamentos. O sistema possui autenticação, upload de imagens, filtros em todas as listagens e controle básico de permissões. O objetivo do projeto é disponibilizar uma forma simples e organizada de cadastrar médicos, registrar clientes e criar agendamentos de consultas.

Instruções de instalação e configuração
Pré-requisitos

Windows 10/11
Python 3.10+ (marque a opção “Add Python to PATH” ao instalar)
Git (necessário para clonar o repositório)

Passo a passo (Windows)
Clonar o projeto
git clone https://github.com/Carlosemfeitoza/Projeto
cd seu-repositorio

Criar o ambiente virtual
python -m venv venv

Ativar o ambiente virtual
.\venv\Scripts\Activate

Instalar dependências
pip install -r requirements.txt

Aplicar migrações
python manage.py migrate

Criar superusuário (necessário para acessar /admin e gerenciar os cadastros)
python manage.py createsuperuser

Executar o servidor
python manage.py runserver

Abrir o app

Interface principal: http://127.0.0.1:8000/

Admin Django: http://127.0.0.1:8000/admin/

Funcionamento geral do sistema

O sistema oferece:

— Cadastro de Médicos
— Cadastro de Clientes
— Cadastro de Cidades
— Cadastro e gerenciamento de Agendamentos
— Filtros em todas as listagens (clientes, médicos, cidades e agendamentos)
— Paginação nas listagens
— Upload de imagens (perfil e fotos)
— Autenticação com login, logout, registro e recuperação de senha
— Interface simples, organizada e responsiva

Esses recursos permitem que o usuário gerencie todos os dados básicos de uma clínica de forma prática.

Estrutura básica do projeto

O projeto utiliza:

Django (backend e templates)

SQLite (banco de dados padrão)

HTML + CSS + Bootstrap (interface)

Pillow (upload de imagens)

O repositório contém:

Aplicações separadas por função

Templates organizados

Sistema de mensagens

Páginas específicas para login, cadastro e recuperação de senha

Pastas para armazenamento de imagens (media/)

Observações importantes

Durante o desenvolvimento, o envio de e-mails usa o backend de console, então o link de redefinição de senha aparece diretamente no terminal onde o servidor está rodando.

Em settings.py, certifique-se de que MEDIA_URL e MEDIA_ROOT estão configurados corretamente para exibir imagens.

A pasta media/ será criada automaticamente após o primeiro upload.

Em produção, é necessário configurar um servidor de arquivos estáticos e de mídia.

requirements.txt sugerido
Django==4.2.2
pillow
