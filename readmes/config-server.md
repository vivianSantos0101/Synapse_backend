# ConfigServer

Servidor centralizado de configurações e secrets para todos os microsserviços.

## Visão Geral

O ConfigServer armazena e distribui configurações de aplicação e secrets de forma centralizada. Cada microsserviço consulta o ConfigServer na inicialização e recebe atualizações em tempo real via WebSocket quando uma configuração muda.

## Funcionalidades

- Armazenamento centralizado de configurações por ambiente (dev, staging, prod)
- Secrets criptografados com chave AES-256
- Notificação de mudanças em tempo real via WebSocket
- Versionamento de configurações com histórico
- Validação de schema antes de aplicar mudanças
- Herança de configurações (global → ambiente → serviço)
- CLI para gerenciamento de configs
- Auditoria de quem alterou cada configuração

## Arquitetura

- **API REST**: CRUD de configurações
- **WebSocket Server**: notifica serviços de mudanças
- **Encryption Layer**: criptografa secrets antes de persistir
- **Validator**: valida schemas JSON antes de aceitar mudanças

## Stack Tecnológica

- Go 1.22
- PostgreSQL para persistência
- Redis para cache e pub/sub
- WebSocket para notificações

## API

### GET /config/{service}/{environment}
Retorna configurações de um serviço em um ambiente.

### PUT /config/{service}/{environment}
Atualiza configurações.

### GET /config/{service}/{environment}/history
Retorna histórico de alterações.

## Limitações

- Sem integração com HashiCorp Vault
- WebSocket não suporta reconexão automática no SDK
- Limite de 1MB por configuração

## Roadmap

- Integração com Vault para secrets
- SDK com reconexão automática
- UI web para gerenciamento visual
