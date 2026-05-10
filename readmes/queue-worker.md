# QueueWorker

Framework de processamento de jobs assíncronos com filas RabbitMQ e gerenciamento de retries.

## Visão Geral

O QueueWorker é o sistema de processamento assíncrono da empresa. Serviços publicam mensagens em filas RabbitMQ e workers dedicados processam essas mensagens. Suporta retry com backoff exponencial, dead letter queues e monitoramento de jobs.

## Funcionalidades

- Workers para processamento de filas RabbitMQ
- Retry automático com backoff exponencial
- Dead letter queue para mensagens que falharam
- Priorização de mensagens por fila
- Monitoramento de throughput e latência
- Suporte a múltiplos workers por fila
- Graceful shutdown com finalização de jobs em andamento
- Logging estruturado por job

## Arquitetura

```
Serviço Producer → RabbitMQ → Worker Consumer → Resultado
                                    ↓ (falha)
                              Retry Queue → DLQ
```

- **Producer SDK**: biblioteca para publicar mensagens
- **Worker Runtime**: gerencia lifecycle dos consumers
- **Retry Manager**: controla tentativas com backoff
- **Monitor**: expõe métricas de processamento

## Stack Tecnológica

- Python 3.12
- RabbitMQ como message broker
- Celery para gerenciamento de workers
- Redis como result backend
- Flower para monitoramento

## Uso

```python
from queue_worker import task

@task(queue="emails", max_retries=3)
def send_email(to: str, subject: str, body: str):
    # lógica de envio
    pass

# Publicar
send_email.delay(to="user@email.com", subject="Oi", body="Teste")
```

## Limitações

- Sem suporte a Kafka (apenas RabbitMQ)
- Monitoramento depende do Flower (externo)
- Sem priorização dinâmica de jobs

## Roadmap

- Suporte a Kafka como alternativa
- Dashboard próprio de monitoramento
- Agendamento de jobs (cron-like)
