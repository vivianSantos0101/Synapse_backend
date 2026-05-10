# UserAnalytics

Plataforma de analytics de comportamento de usuários com tracking de eventos, funnels e dashboards.

## Visão Geral

O UserAnalytics coleta eventos de interação dos usuários em todos os produtos da empresa, processa em tempo real e disponibiliza dashboards com métricas de engajamento, retenção e conversão.

## Funcionalidades

- Tracking de eventos customizáveis (cliques, pageviews, ações)
- Funnels de conversão configuráveis
- Análise de coorte e retenção
- Segmentação de usuários por comportamento
- Dashboards em tempo real com Grafana
- Exportação de dados para data lake
- SDK JavaScript para frontend e SDK Python para backend
- Heatmaps de interação (experimental)

## Arquitetura

```
SDK → API Collector → Kafka → Stream Processor → ClickHouse → Grafana
```

- **Collector API**: recebe eventos dos SDKs
- **Stream Processor**: enriquece e agrega eventos em tempo real
- **ClickHouse**: armazena eventos com queries analíticas rápidas
- **Grafana**: dashboards e visualizações

## Stack Tecnológica

- Node.js para Collector API
- Apache Kafka para streaming
- ClickHouse para armazenamento analítico
- Grafana para dashboards
- TypeScript para SDKs

## API

### POST /events/track
Registra um evento de usuário.

```json
{
  "event": "button_click",
  "user_id": "u123",
  "properties": { "button": "signup", "page": "/home" }
}
```

### GET /analytics/funnel?steps=signup,activate,purchase
Retorna dados de um funnel de conversão.

## Limitações

- Heatmaps apenas para aplicações web
- Sem análise preditiva (apenas descritiva)
- ClickHouse requer manutenção de storage

## Roadmap

- Análise preditiva com ML
- Integração com Mixpanel e Amplitude
- Alertas automáticos de queda de métricas
