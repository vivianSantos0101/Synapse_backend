# DashboardAdmin

Painel administrativo web para gestão de usuários, permissões e visualização de métricas operacionais.

## Visão Geral

O DashboardAdmin é a interface administrativa central da empresa. Ele permite que gestores e administradores visualizem métricas de operação, gerenciem usuários e permissões, acompanhem indicadores de performance e configurem parâmetros do sistema.

## Funcionalidades

- Dashboard com gráficos interativos de métricas operacionais
- Gerenciamento de usuários (CRUD, ativação/desativação)
- Sistema de permissões baseado em roles (RBAC)
- Visualização de KPIs em tempo real com auto-refresh
- Exportação de relatórios em PDF e Excel
- Filtros avançados por período, equipe e projeto
- Tema dark/light com persistência de preferência
- Tabelas com paginação, ordenação e busca
- Logs de atividade dos administradores

## Arquitetura

Single Page Application (SPA) construída com React, consumindo APIs REST do backend.

Componentes:
- **Dashboard Module**: gráficos com Recharts e cards de KPI
- **User Management**: CRUD completo com formulários validados
- **Permissions**: tela de roles e atribuição de permissões
- **Reports**: geração e download de relatórios
- **Layout**: sidebar, header e sistema de navegação

## Stack Tecnológica

- React 18 com TypeScript
- Vite como bundler
- Recharts para gráficos
- TanStack Table para tabelas avançadas
- React Hook Form + Zod para formulários
- Axios para requisições à API
- CSS Modules para estilização

## Instalação

```bash
git clone https://gitlab.empresa.com/frontend/dashboard-admin.git
cd dashboard-admin
npm install
npm run dev
```

## Variáveis de Ambiente

- `VITE_API_URL`: URL da API backend
- `VITE_AUTH_URL`: URL do AuthGateway
- `VITE_SENTRY_DSN`: monitoramento de erros

## Limitações

- Não responsivo para mobile (otimizado para desktop)
- Gráficos limitados a 10.000 pontos de dados
- Sem suporte a internacionalização (apenas pt-BR)

## Roadmap

- Versão responsiva para tablets
- i18n com suporte a inglês e espanhol
- Dashboard customizável (drag-and-drop de widgets)
- Notificações em tempo real via WebSocket
