# FileStorage

Serviço de armazenamento de arquivos compatível com S3, com upload seguro e URLs pré-assinadas.

## Visão Geral

O FileStorage é a camada de armazenamento de arquivos da empresa. Ele oferece uma API simples para upload, download e gerenciamento de arquivos, com suporte a presigned URLs para acesso temporário seguro. Utiliza MinIO como backend, compatível com a API S3 da AWS.

## Funcionalidades

- Upload e download de arquivos via API REST
- Presigned URLs com expiração configurável
- Organização em buckets por projeto ou equipe
- Versionamento de arquivos
- Limite de tamanho configurável por bucket
- Compressão automática para arquivos de texto
- Scan de antivírus no upload (ClamAV)
- Thumbnails automáticos para imagens
- Metadados customizáveis por arquivo

## Arquitetura

Camada de API sobre MinIO com processamento assíncrono para tarefas pesadas.

Componentes:
- **Upload API**: recebe arquivos via multipart/form-data
- **Storage Backend**: MinIO com replicação
- **Media Processor**: gera thumbnails e comprime arquivos
- **Virus Scanner**: ClamAV em container separado
- **URL Signer**: gera presigned URLs com tempo de expiração

## Stack Tecnológica

- Go 1.22
- MinIO como object storage
- Redis para cache de metadados
- ClamAV para scan de vírus
- FFmpeg para processamento de mídia

## Instalação

```bash
git clone https://gitlab.empresa.com/platform/file-storage.git
cd file-storage
docker compose up -d
```

## API

### POST /files/upload
Upload de arquivo com metadados opcionais.

### GET /files/{id}/download
Download direto do arquivo.

### POST /files/{id}/presign
Gera uma URL pré-assinada para acesso temporário.

### DELETE /files/{id}
Remove um arquivo (soft delete com retenção de 30 dias).

## Variáveis de Ambiente

- `MINIO_ENDPOINT`: endereço do MinIO
- `MINIO_ACCESS_KEY`: chave de acesso
- `MINIO_SECRET_KEY`: chave secreta
- `MAX_FILE_SIZE`: tamanho máximo por upload (default: 100MB)

## Limitações

- Sem suporte a streaming de vídeo
- Thumbnails apenas para JPEG e PNG
- Sem CDN integrado — servido diretamente do MinIO

## Roadmap

- CDN com CloudFront ou similar
- Streaming de vídeo com HLS
- Integração com Google Drive e OneDrive
- Compressão de imagens com WebP
