# MobileApp

Aplicativo móvel corporativo para gestão de tarefas, comunicação interna e acesso a sistemas da empresa.

## Visão Geral

O MobileApp é o aplicativo oficial da empresa para colaboradores. Ele unifica acesso a tarefas, aprovações, comunicados internos e dashboards em uma única interface mobile. Disponível para iOS e Android.

## Funcionalidades

- Lista de tarefas com status e prioridade
- Push notifications para aprovações pendentes e comunicados
- Chat interno entre equipes
- Visualização de dashboards e KPIs
- Leitor de QR code para check-in em reuniões
- Modo offline com sincronização automática
- Autenticação via SSO corporativo

## Arquitetura

Aplicação construída com React Native e Expo, consumindo APIs REST do backend corporativo.

Componentes:
- **Navigation**: React Navigation com deep linking
- **State Management**: Zustand para estado global
- **API Layer**: Axios com interceptors para refresh de token
- **Push Service**: Firebase Cloud Messaging (FCM) e APNs
- **Offline Storage**: WatermelonDB para dados locais

## Stack Tecnológica

- React Native 0.73 com Expo SDK 50
- TypeScript
- Zustand para estado
- React Query para cache de API
- Firebase para push notifications e analytics

## Instalação

```bash
git clone https://gitlab.empresa.com/mobile/mobile-app.git
cd mobile-app
npm install
npx expo start
```

## Build

```bash
# iOS
eas build --platform ios --profile production

# Android
eas build --platform android --profile production
```

## Variáveis de Ambiente

- `API_BASE_URL`: URL da API backend
- `FIREBASE_CONFIG`: configuração do Firebase
- `SENTRY_DSN`: monitoramento de erros

## Limitações

- Sem suporte a tablets (layout otimizado apenas para smartphones)
- Chat não suporta envio de arquivos ainda
- Modo offline limitado a tarefas e comunicados

## Roadmap

- Suporte a tablets
- Envio de fotos e documentos no chat
- Biometria para aprovações sensíveis
- Widget para tela inicial
