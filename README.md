# Spotify Music Catalog Platform

Backend em Django + frontend em React para ingestão e busca global de músicas com Spotify + Typesense, seguindo princípios de Clean Architecture + DDD.

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
frontend/
  src/
    components/
    services/
    styles/
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

Logs:
- `DJANGO_LOG_LEVEL=INFO` (ex.: `DEBUG`, `INFO`, `WARNING`, `ERROR`)

## Subir com Docker
```bash
docker compose up --build
```

API: `http://localhost:${API_PORT}`  
Frontend: `http://localhost:${FRONTEND_PORT}`  
Typesense (host): `http://localhost:${TYPESENSE_HOST_PORT}`

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

`POST /api/v1/songs/seed/top-hits`

Body:
```json
{}
```

Resposta:
```json
{
  "message": "top hits seeded",
  "total_indexed": 100,
  "indexed_by_query": {
    "top hits": 20
  },
  "queries": ["top hits"],
  "limit_per_query": 20
}
```

`GET /api/v1/songs/search?q=daft%20punk&limit=10&page=1`

Resposta:
```json
{
  "query": "daft punk",
  "found": 42,
  "count": 10,
  "page": 1,
  "songs": []
}
```

## Frontend
Interface React com estética inspirada no Spotify:
- tema escuro com verde de destaque
- cards com depth + glow
- dashboard único para `seed`, `ingest` e `search`
- responsivo para desktop/mobile

Se quiser rodar só o frontend localmente:
```bash
cd frontend
npm install
npm run dev
```

Variável usada pelo frontend:
- `VITE_API_BASE_URL=http://localhost:8012/api/v1`

## Observações
- O projeto atual já está preparado para troca de nome sem impacto estrutural.
- A configuração do Typesense está toda via `env`.
