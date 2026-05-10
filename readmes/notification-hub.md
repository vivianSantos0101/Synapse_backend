# NotificationHub

Serviço centralizado de envio de notificações multicanal: e-mail, SMS, push e webhooks.

## Visão Geral

O NotificationHub é o serviço unificado para envio de notificações a usuários e sistemas. Qualquer serviço interno que precise notificar alguém envia uma requisição ao hub, que se encarrega de rotear para o canal correto, aplicar templates e garantir a entrega.

## Funcionalidades

- Envio de e-mails transacionais via SendGrid e SMTP
- SMS via Twilio com fallback para outro provedor
- Push notifications para iOS (APNs) e Android (FCM)
- Webhooks configuráveis para integrações externas
- Sistema de templates com variáveis dinâmicas (Handlebars)
- Fila de envio com retry automático e dead letter queue
- Preferências de canal por usuário (opt-in / opt-out)
- Histórico de notificações enviadas com status de entrega
- Agendamento de envios futuros

## Arquitetura

Baseado em filas assíncronas para garantir desacoplamento e resiliência.

Componentes:
- **API de Disparo**: recebe requisições de envio
- **Template Engine**: renderiza templates com dados dinâmicos
- **Channel Router**: decide qual provedor usar por canal
- **Queue Workers**: processam envios de cada canal
- **Delivery Tracker**: monitora status de entrega

## Stack Tecnológica

- Node.js 20 com NestJS
- RabbitMQ para filas de envio
- Redis para cache de templates
- PostgreSQL para histórico e preferências
- Handlebars para templates

## Instalação

```bash
git clone https://gitlab.empresa.com/platform/notification-hub.git
cd notification-hub
npm install
docker compose up -d
```

## API

### POST /notifications/send
Envia uma notificação imediata.

```json
{
  "recipient": "user@empresa.com",
  "channel": "email",
  "template": "welcome",
  "data": { "name": "João" }
}
```

### POST /notifications/schedule
Agenda uma notificação para envio futuro.

### GET /notifications/{id}/status
Consulta o status de entrega de uma notificação.

## Limitações

- SMS limitado a 160 caracteres por mensagem
- Sem suporte a notificações in-app (apenas canais externos)
- Templates não suportam condicional complexa (apenas variáveis)

## Roadmap

- Notificações in-app com WebSocket
- Editor visual de templates
- A/B testing de mensagens
- Suporte a WhatsApp Business API
