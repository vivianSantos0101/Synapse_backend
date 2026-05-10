# SSOPortal

Portal de Single Sign-On (SSO) para login unificado em todos os sistemas internos da empresa.

## Visão Geral

O SSOPortal é a tela de login unificada da empresa. Todos os sistemas internos redirecionam para o portal quando o usuário não está autenticado. Suporta SAML 2.0, OpenID Connect e integração com Active Directory. Uma vez logado, o usuário acessa todos os sistemas sem precisar autenticar novamente.

## Funcionalidades

- Login unificado com sessão compartilhada entre sistemas
- Suporte a SAML 2.0 como Identity Provider
- OpenID Connect para aplicações modernas
- Integração com Active Directory / LDAP
- Tela de login customizável com branding da empresa
- Remember me com token persistente
- Gerenciamento de sessões ativas
- Logout centralizado (single logout)
- Página de recuperação de senha
- Auditoria de logins com IP e device

## Arquitetura

- **Login UI**: interface React com formulário de login
- **SAML IdP**: emite assertions SAML para service providers
- **OIDC Provider**: emite tokens OpenID Connect
- **Session Store**: Redis para sessões compartilhadas
- **AD Connector**: autentica contra Active Directory

## Stack Tecnológica

- Node.js 20 com Express
- React 18 para frontend
- Redis para sessões
- PostgreSQL para auditoria
- Passport.js para estratégias de autenticação

## Fluxo de Login

1. Usuário acessa sistema interno
2. Sistema redireciona para SSOPortal
3. Usuário faz login (credenciais ou AD)
4. Portal emite token/assertion e redireciona de volta
5. Sistema valida token e cria sessão local

## Limitações

- Sem suporte a login social (Google, GitHub)
- MFA apenas via TOTP (sem SMS ou biometria)
- Customização visual limitada a logo e cores

## Roadmap

- Login social como opção secundária
- MFA via push notification
- Passwordless com magic link
- Suporte a WebAuthn/FIDO2
