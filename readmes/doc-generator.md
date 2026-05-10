# DocGenerator

Gerador automático de documentação de API a partir de código-fonte e anotações OpenAPI.

## Visão Geral

O DocGenerator analisa código-fonte de projetos da empresa e gera documentação de API atualizada automaticamente. Suporta Swagger/OpenAPI, gera páginas estáticas em Markdown e publica no GitLab Pages.

## Funcionalidades

- Extração automática de endpoints a partir de FastAPI, Django e Express
- Geração de documentação OpenAPI 3.0
- Renderização em páginas estáticas com tema customizado
- Publicação automática via CI/CD no GitLab Pages
- Versionamento de docs por branch/tag
- Busca full-text na documentação
- Exemplos de request/response gerados automaticamente
- Suporte a Markdown para documentação complementar

## Como Usar

```bash
doc-generator scan --project ./meu-projeto --output ./docs
doc-generator publish --docs ./docs --pages-url https://docs.empresa.com
```

## Stack Tecnológica

- Python 3.12
- Jinja2 para templates
- MkDocs Material para renderização
- GitLab CI para publicação

## Limitações

- Suporta apenas Python e Node.js
- Não gera docs de WebSocket ou gRPC

## Roadmap

- Suporte a Java/Spring
- Changelog automático entre versões
- Playground interativo para testar endpoints
