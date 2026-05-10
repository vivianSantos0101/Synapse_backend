# InventoryAPI

API de gestão de estoque com controle de entradas, saídas, alertas de reposição e multi-armazém.

## Visão Geral

O InventoryAPI gerencia todo o estoque da empresa. Controla entradas e saídas de produtos, movimentações entre armazéns, alertas de estoque mínimo e integrações com sistemas de compras e vendas.

## Funcionalidades

- Cadastro de produtos com SKU, categorias e atributos
- Controle de entradas e saídas com rastreabilidade
- Múltiplos armazéns com transferências entre eles
- Alertas automáticos de estoque mínimo
- Inventário físico com contagem e ajuste
- Reserva de estoque para pedidos pendentes
- Histórico completo de movimentações
- Relatórios de giro de estoque
- Integração com leitores de código de barras

## Arquitetura

- **Product Service**: CRUD de produtos e categorias
- **Stock Engine**: controla saldos e movimentações
- **Alert Service**: monitora níveis e dispara alertas
- **Integration Layer**: conecta com ERP e sistemas de venda

## Stack Tecnológica

- Java 21 com Spring Boot
- PostgreSQL para persistência
- Redis para cache de saldos
- RabbitMQ para eventos de movimentação
- Swagger para documentação de API

## API

### GET /inventory/products/{sku}/stock
Retorna saldo atual de um produto.

### POST /inventory/movements
Registra uma movimentação (entrada, saída ou transferência).

### GET /inventory/alerts
Lista alertas de estoque mínimo ativos.

### POST /inventory/count
Registra contagem de inventário físico.

## Limitações

- Sem suporte a lotes e validade
- Custo médio ponderado apenas (sem FIFO/LIFO)
- Sem integração com transportadoras

## Roadmap

- Controle de lotes e validade
- Integração com marketplaces
- Previsão de demanda com ML
