# Sistema de Gerenciamento de Eventos - IFAL

### Introdução

Sistema desktop para gerenciamento de eventos acadêmicos do IFAL, desenvolvido em Python com interface gráfica moderna utilizando CustomTkinter e banco de dados SQLite com Prisma ORM.

## Funcionalidades

- 📅 Gerenciamento completo de eventos (criar, editar, excluir, listar)
- 👥 Cadastro e gestão de participantes
- ✅ Sistema de inscrições em eventos
- 📊 Relatórios e estatísticas
- 🎫 Controle de presença e certificados

## Pré-requisitos

Para executar este projeto, você precisará ter instalado:

1. **Python 3.8+** - [Download](https://www.python.org/downloads/)
2. **Git** - [Download](https://git-scm.com/downloads)
3. **pip** (geralmente incluído com o Python)

## Instalação

### 1. Clone o repositório

```bash
https://github.com/rafaelbarross/ifal-eventos.git
```

### 2. Crie e ative o ambiente virtual

**Windows:**

```
.venv/Scripts/Activate.ps1
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados

```bash
# Criar as tabelas no banco de dados e Gerar o Prisma Client
prisma db push
```

## Estrutura do Projeto

```
├── 📁 certificados
├── 📁 modules
│   ├── 📁 evento
│   │   └── 🐍 evento.py
│   ├── 📁 inscricao
│   │   └── 🐍 inscricao.py
│   └── 📁 participante
│       └── 🐍 participante.py
├── 📁 prisma
│   ├── 📄 evento.db
│   └── 📄 schema.prisma
├── 📁 relatorios
├── 📁 src
│   ├── 📁 telas
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 eventos.py
│   │   ├── 🐍 inscricoes.py
│   │   ├── 🐍 participantes.py
│   │   └── 🐍 relatorios.py
│   ├── 📁 utils
│   │   ├── 🐍 __init__.py
│   │   └── 🐍 icons.py
│   └── 🐍 main.py
├── 📝 README.md
└── 📄 requirements.txt
```

## Execução

Para executar o projeto:

```bash
# Certifique-se de que o ambiente virtual está ativado
python src/main.py
```

## Banco de Dados

O projeto utiliza **SQLite** como banco de dados, gerenciado através do **Prisma ORM**.

### Schema Principal

- **Evento**: Armazena informações dos eventos (nome, data, local, vagas, etc.)
- **Participante**: Cadastro de participantes (nome, CPF, email, curso, turma)
- **Inscricao**: Relacionamento entre eventos e participantes

### Comandos Úteis do Prisma

```bash
# Visualizar o banco de dados no navegador
prisma studio

# Atualizar o schema após mudanças
prisma db push

# Gerar novamente o cliente Prisma
prisma generate --watch
```

## Tecnologias Utilizadas

- **Python 3.x** - Linguagem principal
- **CustomTkinter** - Interface gráfica moderna
- **Prisma Python** - ORM para banco de dados
- **SQLite** - Banco de dados embutido
- **asyncio** - Programação assíncrona

## Desenvolvimento

### Adicionar novas dependências

```bash
# Instalar nova biblioteca
pip install nome-da-biblioteca

# Atualizar o requirements.txt
pip freeze > requirements.txt
```

### Modificar o schema do banco

1. Edite o arquivo `prisma/schema.prisma`
2. Execute `prisma db push` para aplicar as mudanças
3. Execute `prisma generate` para atualizar o cliente

## Solução de Problemas

### Erro: "Event loop is closed"

- Certifique-se de que está usando a função `executar_async()` para operações assíncronas

### Erro: "Prisma Client not found"

- Execute `prisma generate` novamente

### Erro ao importar módulos

- Verifique se o ambiente virtual está ativado
- Reinstale as dependências: `pip install -r requirements.txt`
