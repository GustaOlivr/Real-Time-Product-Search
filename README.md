# Spotify Music Catalog API

API em Django com foco em ingestão de músicas do Spotify e indexação no Typesense, seguindo princípios de Clean Architecture + DDD.

## Objetivo
- Buscar músicas no Spotify
- Alimentar o Typesense com os dados retornados
- Expor endpoint HTTP para ingestão
- Manter separação de camadas:
  - controllers
  - services
  - repositories
  - domain

## Estrutura
```text
src/
  config/
  music_catalog/
    controllers/
    domain/
    repositories/
    services/
```

## Variáveis de ambiente
Copie `.env.example` para `.env` e preencha:
```bash
cp .env.example .env
```

## Subir com Docker
```bash
docker compose up --build
```

API: `http://localhost:8000`
Typesense: `http://localhost:8108`

## Endpoint
`POST /api/v1/songs/ingest`

Body:
```json
{
  "query": "daft punk",
  "limit": 10
}
```

Resposta:
```json
{
  "message": "songs indexed",
  "count": 10,
  "songs": []
}
```

## Observações
- O projeto atual já está preparado para troca de nome sem impacto estrutural.
- A configuração do Typesense está toda via `env`.
