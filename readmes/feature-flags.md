# FeatureFlags

Serviço de feature flags para controle de rollout gradual e A/B testing.

## Visão Geral

O FeatureFlags permite ativar ou desativar funcionalidades em produção sem deploy. Suporta rollout percentual, segmentação por usuário e A/B testing com métricas integradas.

## Funcionalidades

- Toggle de features on/off em tempo real
- Rollout gradual por porcentagem de usuários
- Segmentação por atributos do usuário (plano, região, role)
- A/B testing com variantes e métricas de conversão
- Histórico de alterações com quem ativou/desativou
- SDK para Python, Node.js e React
- Cache local com refresh periódico
- API REST para gerenciamento

## Arquitetura

- **Admin API**: CRUD de flags e regras
- **Evaluation Engine**: resolve flag para cada usuário com base em regras
- **SDK Client**: avalia flags localmente com cache
- **Analytics Collector**: coleta eventos de exposição para A/B testing

## Stack Tecnológica

- Go 1.22 para o backend
- React para admin UI
- PostgreSQL para persistência
- Redis para cache de flags

## API

### GET /flags/{key}/evaluate?user_id=123
Avalia uma flag para um usuário específico.

### POST /flags
Cria uma nova feature flag.

### PATCH /flags/{key}
Atualiza regras de uma flag.

## Limitações

- Sem suporte a multi-tenancy
- A/B testing sem cálculo de significância estatística

## Roadmap

- Cálculo de significância estatística
- Integração com Segment e Amplitude
- Webhooks de mudança de flag
