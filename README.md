# Synapse — Buscador Semântico de Repositórios

Sistema RAG (Retrieval-Augmented Generation) que indexa READMEs de projetos e permite busca semântica para verificar se determinada ferramenta ou funcionalidade já existe em algum repositório.

## Pré-requisitos

- **Python 3.10+**
- **Docker** e **Docker Compose** (para o PostgreSQL com pgvector)
- **pip** (gerenciador de pacotes Python)

## Início Rápido

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/synapse-semantic-search.git
cd synapse-semantic-search/semantic_search
```

### 2. Configure as variáveis de ambiente

```bash
cp .env.example .env
```

Edite o `.env` se quiser alterar usuário, senha ou porta do PostgreSQL. Os valores padrão funcionam para desenvolvimento local.

### 3. Suba o banco de dados

```bash
docker compose up -d
```

Isso inicia um container PostgreSQL 16 com a extensão **pgvector** já instalada. Os dados ficam persistidos no volume `pgdata`.

Para verificar se o container está rodando:

```bash
docker compose ps
```

### 4. Instale as dependências Python

```bash
pip install -r requirements.txt
```

### 5. Indexe os READMEs

```bash
python cli.py index --dir readmes/
```

### 6. Faça uma busca

```bash
python cli.py search "autenticação OAuth JWT"
```

Ou diretamente (sem o `search`):

```bash
python cli.py "pagamento via PIX"
```

## Comandos do CLI

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `index --dir <pasta>` | Indexa todos os `.md` de uma pasta | `python cli.py index --dir readmes/` |
| `index --file <arquivo> --repo <nome>` | Indexa um arquivo específico | `python cli.py index --file README.md --repo empresa/meu-projeto` |
| `search "<consulta>"` | Busca semântica | `python cli.py search "deploy kubernetes"` |
| `stats` | Mostra estatísticas da base | `python cli.py stats` |

### Opções do search

| Opção | Padrão | Descrição |
|-------|--------|-----------|
| `--top-k` | 10 | Número máximo de resultados |
| `--min-score` | 0.30 | Score mínimo de similaridade |

## API REST (FastAPI)

O projeto também expõe uma API REST. Para iniciar o servidor:

```bash
uvicorn app.main:app --reload
```

O servidor roda em `http://localhost:8000`. Documentação interativa em `http://localhost:8000/docs`.

### Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/api/v1/index` | Indexa um README |
| `DELETE` | `/api/v1/index/{repo_name}` | Remove um repositório |
| `POST` | `/api/v1/search` | Busca semântica |
| `GET` | `/api/v1/stats` | Estatísticas da base |
| `GET` | `/health` | Health check |

## Estrutura do Projeto

```
semantic_search/
├── app/
│   ├── api/
│   │   └── routes.py           # Endpoints da API REST
│   ├── core/
│   │   ├── init_db.py          # Inicialização do banco
│   │   └── settings.py         # Configurações (variáveis de ambiente)
│   ├── models/
│   │   └── schemas.py          # Schemas Pydantic
│   ├── services/
│   │   ├── chunker.py          # Quebra READMEs em chunks
│   │   ├── embedding_service.py # Gera embeddings com sentence-transformers
│   │   └── vector_store.py     # Operações no banco vetorial (pgvector)
│   └── main.py                 # Ponto de entrada da API FastAPI
├── readmes/                    # READMEs de exemplo para teste
├── cli.py                      # Interface de linha de comando
├── testar_readme.py            # Script de teste via HTTP
├── docker-compose.yml          # PostgreSQL + pgvector
├── requirements.txt            # Dependências Python
├── .env.example                # Template de variáveis de ambiente
└── .gitignore
```

## Stack Técnica

| Componente | Tecnologia |
|------------|------------|
| Banco vetorial | PostgreSQL 16 + pgvector |
| Embeddings | sentence-transformers (paraphrase-multilingual-MiniLM-L12-v2) |
| API | FastAPI |
| CLI | argparse + rich |
| Container | Docker Compose |
| Driver PostgreSQL | psycopg 3 |

## Comandos Úteis

```bash
# Parar o banco de dados
docker compose down

# Parar e apagar todos os dados
docker compose down -v

# Ver logs do container
docker compose logs -f

# Reindexar tudo (apaga dados antigos de cada repo antes)
python cli.py index --dir readmes/
```

## Variáveis de Ambiente

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `PG_USER` | `synapse` | Usuário do PostgreSQL |
| `PG_PASSWORD` | `synapse` | Senha do PostgreSQL |
| `PG_HOST` | `localhost` | Host do PostgreSQL |
| `PG_PORT` | `5432` | Porta do PostgreSQL |
| `PG_DATABASE` | `synapse_search` | Nome do banco |
| `DATABASE_URL` | `postgresql://synapse:synapse@localhost:5432/synapse_search` | URL completa de conexão |
| `EMBEDDING_MODEL` | `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` | Modelo de embedding |
| `DEBUG` | `false` | Modo debug |
