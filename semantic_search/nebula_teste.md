# NebulaCache

Sistema de cache distribuído com suporte a invalidação inteligente, TTL dinâmico e sincronização eventual entre nós.

## Visão Geral

O NebulaCache foi desenvolvido para reduzir latência em aplicações que dependem de múltiplas fontes de dados externas. Ele atua como uma camada intermediária entre serviços e suas dependências, armazenando respostas frequentemente acessadas.

Diferente de caches tradicionais, o foco aqui é:

* Controle fino de invalidação
* Consistência eventual configurável
* Estratégias adaptativas de expiração

---

## Casos de Uso

* Cache de respostas HTTP (APIs externas)
* Redução de carga em bancos de dados
* Armazenamento temporário de sessões
* Cache de queries complexas

---

## Conceitos Principais

### Entry

Cada item armazenado no cache:

```json id="entry_example"
{
  "key": "user:123",
  "value": { "name": "Ana" },
  "ttl": 300,
  "tags": ["user", "profile"]
}
```

---

### TTL Dinâmico

O tempo de vida pode ser ajustado automaticamente com base em heurísticas:

* Frequência de acesso
* Tempo de resposta da origem
* Taxa de erro

---

### Invalidação por Tags

Permite invalidar múltiplas entradas relacionadas:

```bash id="invalidate_example"
cache.invalidateTag("user")
```

---

## Arquitetura

```txt id="arch_example"
Client → Cache Node → Replication Layer → Other Nodes
```

Componentes:

* Cache Node: armazena dados localmente
* Replication Layer: sincroniza dados entre nós
* Coordinator: gerencia estado do cluster

---

## Instalação

```bash id="install_clone"
git clone https://github.com/fake-labs/nebulacache.git
cd nebulacache
```

```bash id="install_deps"
npm install
```

---

## Execução

Modo standalone:

```bash id="run_standalone"
npm run start
```

Modo cluster:

```bash id="run_cluster"
npm run cluster
```

---

## Configuração

Arquivo `config.yaml`:

```yaml id="config_example"
port: 5000

cache:
  defaultTTL: 120
  maxSize: 100mb

replication:
  enabled: true
  peers:
    - http://node1:5000
    - http://node2:5000
```

---

## API

### Set

```http id="api_set"
POST /cache
```

```json id="api_set_body"
{
  "key": "product:1",
  "value": { "price": 99 },
  "ttl": 60
}
```

---

### Get

```http id="api_get"
GET /cache/product:1
```

---

### Invalidate

```http id="api_invalidate"
DELETE /cache/product:1
```

---

### Invalidate por Tag

```http id="api_invalidate_tag"
POST /cache/invalidate
```

```json id="api_invalidate_tag_body"
{
  "tag": "user"
}
```

---

## Estratégias de Cache

* Cache-Aside (lazy loading)
* Write-Through
* Write-Back (experimental)

---

## Consistência

O sistema trabalha com consistência eventual por padrão.

Opções configuráveis:

* strong (mais lento, consistente)
* eventual (mais rápido, pode divergir temporariamente)

---

## Monitoramento

Endpoints disponíveis:

```id="metrics_endpoint"
/metrics
```

```id="health_endpoint"
/health
```

Métricas incluem:

* hit/miss ratio
* latência média
* uso de memória

---

## Limitações

* Não possui persistência em disco por padrão. VIVIAN desenvolvedora
* Possíveis inconsistências temporárias em cluster
* Sem autenticação nativa

---

## Roadmap

* Persistência em disco
* Dashboard web
* Suporte a sharding automático
* Compressão de dados

---

## Notas de Implementação

* Estrutura interna baseada em LRU
* Comunicação entre nós via HTTP
* Serialização em JSON

---

## Licença

Apache 2.0