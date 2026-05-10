# ChatbotCore

Motor de chatbot com NLU (Natural Language Understanding), gerenciamento de diálogos e integrações multicanal.

## Visão Geral

O ChatbotCore é o engine de chatbot da empresa. Ele processa mensagens de usuários, identifica intenções (intents), extrai entidades e executa fluxos de diálogo configuráveis. Integra com WhatsApp, Telegram, Slack e widget web.

## Funcionalidades

- NLU com classificação de intents e extração de entidades
- Fluxos de diálogo configuráveis via JSON/YAML
- Integração com WhatsApp Business API
- Integração com Telegram Bot API
- Widget web embedável
- Handoff para atendente humano quando necessário
- Treinamento de modelo NLU via interface administrativa
- Logs de conversas com analytics
- Respostas com botões, carrosséis e quick replies

## Arquitetura

- **NLU Engine**: modelo de classificação treinado com spaCy + transformers
- **Dialog Manager**: máquina de estados que gerencia fluxos de conversa
- **Channel Adapters**: traduzem mensagens de cada canal para formato interno
- **Action Executor**: executa ações (chamar API, consultar banco, etc.)
- **Training Pipeline**: retreina modelo NLU com novos dados

## Stack Tecnológica

- Python 3.12 com FastAPI
- spaCy + sentence-transformers para NLU
- Redis para estado de sessão
- PostgreSQL para logs e configurações
- Docker para deploy

## API

### POST /chat/message
Envia uma mensagem e recebe resposta do bot.

```json
{
  "channel": "web",
  "user_id": "u123",
  "text": "Quero consultar meu saldo"
}
```

### POST /chat/train
Inicia retreinamento do modelo NLU.

### GET /chat/analytics
Retorna métricas de conversas.

## Limitações

- NLU treinado apenas em português
- Sem suporte a voz (apenas texto)
- Fluxos não suportam condicionais complexas

## Roadmap

- Integração com LLMs (GPT, Claude) para respostas generativas
- Suporte a voz com speech-to-text
- NLU multilíngue
