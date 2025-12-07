# **MedAgenda — Sistema de Agendamentos Médicos 🏥**

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-blue)
![Python](https://img.shields.io/badge/Python-3.10+-yellow)
![Django](https://img.shields.io/badge/Django-4.2-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

Sistema web desenvolvido com **Django** para gerenciar **clientes**, **médicos**, **cidades** e **agendamentos médicos**.  
O projeto oferece uma interface simples, funcional e ideal para uso acadêmico.

---

## **📌 Funcionalidades Principais**

- **Gerenciamento completo de Médicos**
  - Cadastro, edição, exclusão e upload de foto

- **Gerenciamento de Clientes**
  - Inclusão, edição, exclusão e foto de perfil

- **Cadastro de Cidades**
  - Utilizadas como referência para médicos e clientes

- **Agendamentos Médicos**
  - Criação, edição, detalhamento e cancelamento (POST seguro)
  - Exibição organizada com paginação e datas formatadas

- **Filtros em todas as listagens**
  - Por nome, cidade, especialidade, datas, status etc.

- **Sistema de Autenticação**
  - Login
  - Logout
  - Cadastro de usuário
  - Recuperação de senha via console

- **Controle básico de permissões**
  - Usuário só pode editar e excluir seus próprios agendamentos
  - Superusuários podem gerenciar tudo

- **Interface Responsiva**
  - Desenvolvida com **Bootstrap**

---

## **📦 Tecnologias Utilizadas**

- **Python 3.x**
- **Django 4.2**
- **SQLite** como banco padrão
- **Bootstrap 4/5**
- **Pillow** (upload de imagens)

---

## **🔧 Instalação e Configuração (Windows)**

### **Pré-requisitos**
- Windows 10 ou 11  
- Python 3.10+ (com “Add Python to PATH”)  
- Git instalado  

---

## **🚀 Passo a Passo para Rodar o Projeto**

### **1. Clonar o repositório**
```bash
git clone https://github.com/Carlosemfeitoza/Projeto
cd seu-repositorio
```

### **2. Criar o ambiente virtual**
```bash
python -m venv venv
```

### **3. Ativar o ambiente virtual**
```bash
.\venv\Scripts\Activate
```

### **4. Instalar dependências**
```bash
pip install -r requirements.txt
```

### **5. Aplicar migrações**
```bash
python manage.py migrate
```

### **6. Criar superusuário**
```bash
python manage.py createsuperuser
```

### **7. Iniciar o servidor**
```bash
python manage.py runserver
```

---

## **🌐 Acessos**

- Interface principal: **http://127.0.0.1:8000/**
- Admin Django: **http://127.0.0.1:8000/admin/**
- Recuperação de senha: prints no console

---

## **🗂 Estrutura Geral do Projeto**

```
MedAgenda/
│
├── agendamento/      # App que gerencia agendamentos
├── cliente/          # App que gerencia clientes
├── medico/           # App dos médicos
├── cidade/           # App das cidades
│
├── templates/        # Templates HTML do sistema
├── static/           # Arquivos estáticos (CSS, JS, imagens)
├── media/            # Uploads de fotos
│
├── manage.py
└── requirements.txt
```

---

## **📷 Uploads**
- Fotos de médicos e clientes são armazenadas na pasta `media/`.
- Criada automaticamente no primeiro upload.

---

## **📌 requirements.txt**
```
Django==4.2.2
pillow
```

---

## **🙌 Créditos**
Projeto desenvolvido para fins educacionais, seguindo princípios de boas práticas em Django, organização de templates, autenticação e CRUDs completos.

