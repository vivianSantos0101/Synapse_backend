# DataPipeline

Plataforma de ingestão, transformação e entrega de dados para o data lake corporativo.

## Visão Geral

O DataPipeline é a espinha dorsal da infraestrutura de dados da empresa. Ele coleta dados de múltiplas fontes (bancos transacionais, APIs externas, arquivos CSV/Parquet), aplica transformações e disponibiliza os resultados no data lake para consumo por times de analytics e ciência de dados.

## Funcionalidades

- Ingestão de dados em batch e streaming
- Conectores pré-construídos para PostgreSQL, MySQL, MongoDB, S3 e APIs REST
- Transformações via Apache Spark com suporte a PySpark
- Orquestração de pipelines com Apache Airflow
- Validação de qualidade de dados com Great Expectations
- Catálogo de dados com linhagem automática
- Alertas de falha via Slack e e-mail

## Arquitetura

```
Fontes → Ingestão (Kafka) → Transformação (Spark) → Data Lake (S3/MinIO) → Catálogo
```

Componentes:
- **Ingestion Workers**: consumidores Kafka que normalizam dados de entrada
- **Spark Jobs**: transformações em batch agendadas pelo Airflow
- **Data Quality Gate**: validações que bloqueiam dados corrompidos
- **Catalog Service**: metadados e linhagem dos datasets

## Stack Tecnológica

- Python 3.11, PySpark
- Apache Kafka para streaming
- Apache Airflow para orquestração
- MinIO como object storage compatível com S3
- Delta Lake para versionamento de tabelas

## Instalação

```bash
git clone https://gitlab.empresa.com/data/data-pipeline.git
cd data-pipeline
docker compose up -d
```

## Configuração

Arquivo `config/pipeline.yaml`:
```yaml
sources:
  - name: vendas_db
    type: postgresql
    connection: ${VENDAS_DB_URL}
    schedule: "0 */6 * * *"

  - name: api_parceiros
    type: rest
    url: https://api.parceiro.com/v2/pedidos
    auth: bearer
```

## Limitações

- Streaming limitado a 10k eventos/segundo por partição
- Sem suporte a CDC (Change Data Capture) nativo
- Airflow requer manutenção manual do scheduler

## Roadmap

- CDC com Debezium
- Interface visual para criação de pipelines
- Suporte a dbt para transformações SQL
