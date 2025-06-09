# API de Produtores Rurais

Este projeto é uma API REST desenvolvida em Python utilizando FastAPI para gerenciamento de produtores rurais.

## 🏗️ Arquitetura

O projeto segue uma arquitetura em camadas, organizada da seguinte forma:

```
app/
├── api/            # Endpoints da API e rotas
├── core/           # Configurações core da aplicação
├── db/             # Configurações do banco de dados
├── domain/         # Modelos de domínio e regras de negócio
├── repositories/   # Camada de acesso a dados
├── services/       # Lógica de negócio
└── utils/          # Utilitários e helpers
```

### Camadas da Aplicação

1. **API Layer** (`app/api/`)
   - Controllers e rotas da API
   - Validação de entrada de dados
   - Documentação automática (Swagger/OpenAPI)

2. **Domain Layer** (`app/domain/`)
   - Modelos de domínio
   - Entidades de negócio
   - Regras de negócio centrais

3. **Service Layer** (`app/services/`)
   - Implementação da lógica de negócio
   - Orquestração de operações
   - Validações complexas

4. **Repository Layer** (`app/repositories/`)
   - Acesso ao banco de dados
   - Operações CRUD
   - Queries complexas

5. **Core** (`app/core/`)
   - Configurações da aplicação
   - Middlewares
   - Segurança e autenticação

6. **Database** (`app/db/`)
   - Configurações do banco de dados
   - Migrações (Alembic)
   - Conexões e sessões

## 🛠️ Tecnologias Principais

- **FastAPI**: Framework web moderno e rápido para APIs
- **SQLAlchemy**: ORM para interação com banco de dados
- **Pydantic**: Validação de dados e serialização
- **Alembic**: Gerenciamento de migrações do banco de dados
- **PostgreSQL**: Banco de dados relacional
- **Pytest**: Framework de testes
- **Uvicorn**: Servidor ASGI

## 🔧 Requisitos

- Python 3.8+
- PostgreSQL
- Dependências listadas em `requirements.txt`

   ```
## 🏃‍♂️ Executando o Projeto

Para iniciar o servidor de desenvolvimento:

```bash
uvicorn app.main:app --reload
```

A documentação da API estará disponível em:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🧪 Testes

Para executar os testes:

```bash
make tdb-up
make tdb-run
```

## 📝 Convenções de Código

- Formatação: Black
- Linting: Ruff
- Testes: Pytest
- Documentação: Docstrings no formato Google Style

## 🔐 Segurança

- Autenticação via JWT
- Senhas hasheadas com bcrypt
- Validação de dados com Pydantic
- Proteção contra injeção SQL via SQLAlchemy

## 📈 Logging

O projeto utiliza logging estruturado com `python-json-logger` para melhor observabilidade e integração com ferramentas de monitoramento.
