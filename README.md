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
git clone https://github.com/seu-usuario/ifal-eventos.git
cd ifal-eventos
```

### 2. Crie e ative o ambiente virtual

**Windows:**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados

```bash
# Gerar o Prisma Client
prisma generate

# Criar as tabelas no banco de dados
prisma db push
```

## Estrutura do Projeto

```
ifal-eventos/
├── prisma/
│   └── schema.prisma          # Schema do banco de dados
├── src/
│   ├── main.py                # Arquivo principal da aplicação
│   ├── telas/                 # Interfaces gráficas
│   │   ├── eventos.py
│   │   ├── participantes.py
│   │   ├── inscricoes.py
│   │   └── relatorios.py
│   └── utils/                 # Utilitários
│       └── icons.py
├── modules/
│   ├── evento/
│   │   └── evento.py          # Manager de eventos
│   └── participante/
│       └── participante.py    # Manager de participantes
├── .venv/                     # Ambiente virtual (não versionado)
├── requirements.txt           # Dependências do projeto
└── README.md                  # Este arquivo
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
prisma generate
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

