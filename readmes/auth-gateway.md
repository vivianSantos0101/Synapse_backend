# AuthGateway

Gateway centralizado de autenticação e autorização para todos os serviços internos da empresa.

## Visão Geral

O AuthGateway é o ponto único de entrada para autenticação de usuários e serviços. Ele gerencia tokens JWT, integração com LDAP corporativo e fluxos OAuth2 para aplicações internas e parceiros externos.

Todo serviço que precisa validar identidade deve consultar o AuthGateway antes de processar requisições.

## Funcionalidades

- Autenticação via OAuth2 (Authorization Code, Client Credentials)
- Emissão e validação de tokens JWT com rotação automática de chaves
- Integração com Active Directory / LDAP para login corporativo
- Multi-factor authentication (MFA) via TOTP e SMS
- Rate limiting por IP e por usuário
- Sessões com TTL configurável e revogação instantânea
- Audit log de todos os eventos de autenticação

## Arquitetura

O serviço é stateless — toda a informação de sessão fica no Redis e os tokens são auto-contidos (JWT).

Componentes principais:
- **Token Service**: emite e valida JWTs, gerencia JWKS
- **Identity Provider Adapter**: abstrai LDAP, OAuth2 e provedores SAML
- **Session Manager**: controla sessões ativas no Redis
- **Rate Limiter**: proteção contra brute force via sliding window

## Stack Tecnológica

- Python 3.12 com FastAPI
- Redis para sessões e cache de tokens
- PostgreSQL para audit logs e configurações
- Integração com Keycloak como IdP secundário

## Instalação

```bash
git clone https://gitlab.empresa.com/infra/auth-gateway.git
cd auth-gateway
docker compose up -d
```

## Variáveis de Ambiente

- `JWT_SECRET`: chave para assinatura de tokens
- `LDAP_URL`: endereço do servidor LDAP
- `REDIS_URL`: conexão com Redis
- `DATABASE_URL`: conexão com PostgreSQL

## API

### POST /auth/token
Gera um token JWT a partir de credenciais válidas.

### POST /auth/refresh
Renova um token expirado usando o refresh token.

### POST /auth/revoke
Revoga uma sessão ativa.

### GET /auth/userinfo
Retorna informações do usuário autenticado.

## Limitações

- Não suporta WebAuthn / FIDO2 ainda
- Integração SAML limitada a um único IdP
- Logs de auditoria sem integração com SIEM externo

## Roadmap

- Suporte a WebAuthn
- Dashboard de sessões ativas
- Integração com Vault para gestão de segredos
