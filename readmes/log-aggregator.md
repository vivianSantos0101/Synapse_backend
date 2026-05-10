# LogAggregator

Sistema centralizado de coleta, indexação e visualização de logs de todos os serviços da empresa.

## Visão Geral

O LogAggregator resolve o problema de logs espalhados em dezenas de microsserviços. Ele coleta logs estruturados de todas as aplicações, indexa em tempo real e oferece busca full-text com filtros avançados. Alertas automáticos notificam a equipe quando padrões anômalos são detectados.

## Funcionalidades

- Coleta de logs via Filebeat e Fluentd
- Indexação em tempo real com Elasticsearch
- Dashboard de visualização com Kibana
- Busca full-text com filtros por serviço, nível e período
- Alertas configuráveis por padrão de log (regex ou threshold)
- Retenção configurável por ambiente (prod: 90 dias, dev: 7 dias)
- Parsing automático de logs JSON e texto plano
- Correlação de logs por trace ID (OpenTelemetry)

## Arquitetura

Stack ELK customizada com camada de coleta distribuída.

```
Serviços → Filebeat → Kafka → Logstash → Elasticsearch → Kibana
```

Componentes:
- **Collectors**: Filebeat em cada nó, enviando para Kafka
- **Processor**: Logstash consome Kafka, parseia e enriquece
- **Index**: Elasticsearch com ILM (Index Lifecycle Management)
- **Visualizer**: Kibana com dashboards pré-configurados

## Stack Tecnológica

- Elasticsearch 8.x
- Logstash para processamento
- Kibana para visualização
- Kafka como buffer de ingestão
- Filebeat para coleta nos nós
- OpenTelemetry para correlação

## Instalação

```bash
git clone https://gitlab.empresa.com/observability/log-aggregator.git
cd log-aggregator
docker compose up -d
```

## Configuração

Arquivo `logstash/pipeline.conf`:
```
input {
  kafka {
    bootstrap_servers => "kafka:9092"
    topics => ["app-logs"]
  }
}
filter {
  json { source => "message" }
  date { match => ["timestamp", "ISO8601"] }
}
output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "logs-%{+YYYY.MM.dd}"
  }
}
```

## Limitações

- Custo de storage cresce rápido em ambientes com muito log
- Kibana requer treinamento para queries complexas
- Sem suporte nativo a métricas (apenas logs)

## Roadmap

- Integração com Grafana Loki como alternativa leve
- Machine learning para detecção de anomalias
- Dashboards auto-gerados por serviço
