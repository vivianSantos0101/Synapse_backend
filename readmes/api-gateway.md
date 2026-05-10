# API Gateway

Gateway de entrada para todos os microsserviços da empresa, com roteamento, rate limiting e observabilidade.

## Visão Geral

O API Gateway atua como proxy reverso centralizado para toda a arquitetura de microsserviços. Ele gerencia roteamento de requisições, aplica políticas de rate limiting, autentica tokens e coleta métricas de tráfego.

Nenhuma requisição externa chega diretamente aos microsserviços — tudo passa pelo gateway.

## Funcionalidades

- Roteamento dinâmico baseado em rotas configuráveis
- Rate limiting por API key, IP e endpoint
- Validação de tokens JWT (integrado com AuthGateway)
- Load balancing entre instâncias de serviços
- Circuit breaker para proteção contra falhas em cascata
- Request/Response transformation
- Cache de respostas para endpoints idempotentes
- Métricas expostas em formato Prometheus

## Arquitetura

Baseado em Kong Gateway com plugins customizados em Lua e Go.

Componentes:
- **Router**: resolve rotas e faz proxy para upstream services
- **Auth Plugin**: valida JWT e verifica permissões
- **Rate Limiter Plugin**: sliding window com Redis como backend
- **Metrics Collector**: exporta métricas para Prometheus/Grafana

## Stack Tecnológica

- Kong Gateway 3.x
- Redis para rate limiting e cache
- Lua e Go para plugins customizados
- Prometheus + Grafana para métricas
- Docker e Kubernetes para deploy

## Instalação

```bash
git clone https://gitlab.empresa.com/infra/api-gateway.git
cd api-gateway
docker compose up -d
```

## Configuração de Rotas

Arquivo `routes.yaml`:
```yaml
services:
  - name: user-service
    url: http://user-service:3000
    routes:
      - paths: ["/api/users"]
        methods: ["GET", "POST"]
    plugins:
      - name: rate-limiting
        config:
          minute: 100
      - name: jwt
```

## Limitações

- Não suporta gRPC nativamente (apenas HTTP/REST)
- WebSocket proxying em beta
- Configuração via YAML, sem interface administrativa

## Roadmap

- Admin UI para gerenciamento de rotas
- Suporte a gRPC
- A/B testing no nível do gateway
- API versioning automático
