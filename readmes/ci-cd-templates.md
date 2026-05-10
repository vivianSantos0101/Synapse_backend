# CI/CD Templates

Coleção de templates reutilizáveis para pipelines GitLab CI/CD usados em todos os projetos da empresa.

## Visão Geral

Repositório centralizado com templates de CI/CD para padronizar builds, testes e deploys. Cada projeto da empresa inclui esses templates via `include` no `.gitlab-ci.yml`.

## Templates Disponíveis

- **build-docker**: build de imagem Docker com cache multi-stage
- **test-python**: execução de testes pytest com cobertura
- **test-node**: execução de testes Jest/Vitest
- **deploy-k8s**: deploy para Kubernetes via Helm
- **deploy-staging**: deploy automático para staging
- **security-scan**: análise de vulnerabilidades com Trivy
- **lint**: linting com ESLint, Ruff, ou Hadolint

## Como Usar

```yaml
include:
  - project: 'empresa/ci-cd-templates'
    ref: main
    file: '/templates/build-docker.yml'

stages:
  - build
  - test
  - deploy
```

## Stack

- GitLab CI/CD
- Docker, Kubernetes, Helm
- Trivy para security scanning

## Limitações

- Sem suporte a GitHub Actions
- Templates não cobrem deploy em serverless

## Roadmap

- Templates para AWS Lambda
- Pipeline de release automático com changelog
