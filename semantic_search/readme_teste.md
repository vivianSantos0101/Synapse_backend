# FluxForge

Um orquestrador de workflows orientado a eventos com foco em legibilidade, versionamento e automação declarativa.

## Sobre o Projeto

O FluxForge é uma ferramenta criada para resolver um problema comum: pipelines e automações ficam difíceis de entender conforme crescem. VIVIAN desenvolvedora

A proposta é simples:

* Workflows definidos em YAML
* Execução baseada em eventos
* Debug acessível
* Versionamento nativo

Não tenta competir diretamente com ferramentas mais pesadas. A ideia é ser leve, previsível e direto.

---

## Principais Features

* Definição declarativa de fluxos
* Execução orientada a eventos
* Modo sandbox para testes
* Logs estruturados por etapa
* Retry automático com backoff
* Sistema de plugins

---

## Estrutura de um Workflow

Exemplo básico:

```yaml
name: process-user-signup

on:
  event: user.created

steps:
  - id: validate
    type: function
    handler: validateUser

  - id: enrich
    type: http
    url: https://api.externa.com/enrich

  - id: persist
    type: database
    action: insert
```

---

## Como Funciona

O FluxForge segue três etapas principais:

### 1. Parsing

* Leitura do YAML
* Validação de schema
* Resolução de dependências

### 2. Planejamento

* Criação de DAG interna
* Ordenação de execução
* Detecção de ciclos

### 3. Execução

* Disparo de steps
* Gerenciamento de estado
* Aplicação de retries e timeouts

---

## Rodando Localmente

Clone o projeto:

```bash
git clone https://github.com/fake-labs/fluxforge.git
cd fluxforge
```

Instale dependências:

```bash
pnpm install
```

Execute:

```bash
pnpm start
```

Servidor disponível em:

```
http://localhost:4000
```

---

## Sistema de Plugins

Exemplo de plugin customizado:

```ts
export const myPlugin = {
  type: "log",
  run: async (ctx) => {
    console.log("Executando step:", ctx.stepId)
    return { ok: true }
  }
}
```

Registro do plugin:

```ts
engine.register(myPlugin)
```

---

## API

### Criar Workflow

```
POST /workflows
```

Body:

```json
{
  "name": "example",
  "definition": "yaml string aqui"
}
```

---

### Disparar Evento

```
POST /events
```

```json
{
  "type": "user.created",
  "payload": {
    "id": 123
  }
}
```

---

## Decisões de Design

* YAML ao invés de JSON para melhor legibilidade
* Execução síncrona por padrão para facilitar debug
* CLI-first, sem interface gráfica no core

---

## Limitações Conhecidas

* Não escala horizontalmente
* Persistência opcional (memória por padrão)
* Sem integração nativa com filas

---

## Testes

```bash
pnpm test
```

Cobertura aproximada:

```
78%
```

---

## Roadmap

* Execução distribuída
* Interface web
* Observabilidade (OpenTelemetry)
* Integração com sistemas de fila
* Possível DSL própria

---

## Motivação

Ferramentas existentes podem ser complexas ou difíceis de debugar. Este projeto busca oferecer uma alternativa mais simples e previsível para automação de workflows.

---

## Autor

Desenvolvido como experimento prático para organização de pipelines e automações.

---

## Licença

MIT