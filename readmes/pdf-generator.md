# PDFGenerator

Serviço de geração de documentos PDF a partir de templates HTML com dados dinâmicos.

## Visão Geral

O PDFGenerator cria documentos PDF a partir de templates HTML/CSS preenchidos com dados dinâmicos. Usado para gerar relatórios, contratos, notas fiscais e certificados de forma automatizada.

## Funcionalidades

- Geração de PDF a partir de templates HTML com Jinja2
- Suporte a CSS completo incluindo flexbox e grid
- Cabeçalho e rodapé customizáveis por página
- Tabelas com quebra de página automática
- Inserção de imagens e logos
- Geração de código de barras e QR code no documento
- Assinatura digital com certificado A1
- Geração em batch (múltiplos documentos em paralelo)
- Merge de múltiplos PDFs

## Arquitetura

- **Template Engine**: Jinja2 renderiza HTML com dados
- **PDF Renderer**: Weasyprint converte HTML → PDF
- **Asset Manager**: gerencia imagens, fontes e logos
- **Signer**: aplica assinatura digital com pyHanko
- **Queue**: jobs de geração processados via Celery

## Stack Tecnológica

- Python 3.12 com FastAPI
- Weasyprint para renderização HTML → PDF
- Jinja2 para templates
- Celery para geração assíncrona
- MinIO para armazenamento dos PDFs gerados

## API

### POST /pdf/generate
Gera um PDF a partir de um template e dados.

```json
{
  "template": "invoice",
  "data": { "client": "Empresa XYZ", "items": [...] }
}
```

### GET /pdf/{id}/download
Faz download de um PDF gerado.

### GET /pdf/templates
Lista templates disponíveis.

## Limitações

- Sem suporte a JavaScript nos templates
- Fontes customizadas precisam ser instaladas no servidor
- PDFs maiores que 100 páginas podem ser lentos

## Roadmap

- Editor visual de templates (drag-and-drop)
- Suporte a DOCX como formato de saída alternativo
- Preview em tempo real do template
