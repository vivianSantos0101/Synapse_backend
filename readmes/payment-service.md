# PaymentService

Serviço de processamento de pagamentos com suporte a cartão de crédito, PIX e boleto.

## Visão Geral

O PaymentService processa todos os pagamentos da plataforma. Integra com Stripe, PagSeguro, processa PIX via API do Banco Central e gera boletos bancários.

## Funcionalidades

- Pagamento via cartão de crédito (Stripe)
- PIX com QR code dinâmico
- Boleto bancário com registro automático
- Assinaturas recorrentes
- Estorno parcial e total
- Split de pagamento entre recebedores
- Conciliação bancária automática

## Stack Tecnológica

- Python 3.12, Django REST Framework
- Celery para processamento assíncrono
- PostgreSQL, Redis
- Stripe SDK

## API

### POST /payments/charge
Processa um pagamento.

### POST /payments/pix/generate
Gera QR code PIX.

### POST /payments/refund
Processa estorno.

## Limitações

- PIX limitado a bancos homologados
- Sem suporte a criptomoedas

## Roadmap

- Apple Pay e Google Pay
- Dashboard financeiro em tempo real
