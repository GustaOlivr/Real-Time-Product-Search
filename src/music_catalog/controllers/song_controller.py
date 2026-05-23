import json
import logging
import os

from django.http import HttpRequest, JsonResponse
from django.views import View

from music_catalog.repositories.spotify_repository import SpotifyHttpRepository
from music_catalog.repositories.typesense_repository import TypesenseSongRepository
from music_catalog.services.song_ingestion_service import SongIngestionService
from music_catalog.services.song_search_service import SongSearchService

logger = logging.getLogger(__name__)


class SongIngestionController(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            payload = json.loads(request.body or "{}")
        except json.JSONDecodeError:
            logger.warning("Invalid JSON payload on songs ingestion endpoint")
            return JsonResponse({"error": "invalid json payload"}, status=400)

        query = payload.get("query")

        if not query:
            logger.warning("Ingestion request rejected because query is missing")
            return JsonResponse({"error": "query is required"}, status=400)

        limit = int(payload.get("limit", os.getenv("SEARCH_DEFAULT_LIMIT", "20")))
        logger.info("Starting songs ingestion query=%s limit=%s", query, limit)

        try:
            service = SongIngestionService(
                spotify_repository=SpotifyHttpRepository(),
                search_repository=TypesenseSongRepository(),
            )

            songs = service.ingest_from_spotify(query=query, limit=limit)
        except Exception:
            logger.exception("Unexpected error while ingesting songs query=%s", query)
            return JsonResponse({"error": "failed to ingest songs"}, status=500)

        logger.info("Songs ingestion completed query=%s indexed_count=%s", query, len(songs))

        return JsonResponse(
            {
                "message": "songs indexed",
                "count": len(songs),
                "songs": [song.to_typesense_document() for song in songs],
            },
            status=201,
        )


class SongTopHitsSeedController(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        queries_env = os.getenv(
            "SEED_TOP_HITS_QUERIES",
            "top hits,viral hits,global top 50,pop hits,rock hits",
        )
        queries = [item.strip() for item in queries_env.split(",") if item.strip()]
        limit_per_query = int(os.getenv("SEED_TOP_HITS_LIMIT_PER_QUERY", "20"))
        logger.info("Starting top hits seed queries=%s limit_per_query=%s", queries, limit_per_query)

        try:
            service = SongIngestionService(
                spotify_repository=SpotifyHttpRepository(),
                search_repository=TypesenseSongRepository(),
            )

            indexed_total = 0
            indexed_by_query: dict[str, int] = {}

            for query in queries:
                songs = service.ingest_from_spotify(query=query, limit=limit_per_query)
                indexed_by_query[query] = len(songs)
                indexed_total += len(songs)
                logger.info("Top hits chunk completed query=%s indexed_count=%s", query, len(songs))
        except Exception:
            logger.exception("Unexpected error while running top hits seed")
            return JsonResponse({"error": "failed to seed top hits"}, status=500)

        logger.info("Top hits seed completed total_indexed=%s", indexed_total)

        return JsonResponse(
            {
                "message": "top hits seeded",
                "total_indexed": indexed_total,
                "indexed_by_query": indexed_by_query,
                "queries": queries,
                "limit_per_query": limit_per_query,
            },
            status=201,
        )


class SongGlobalSearchController(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        query = request.GET.get("q", "").strip()
        if not query:
            logger.warning("Search request rejected because q is missing")
            return JsonResponse({"error": "q is required"}, status=400)

        try:
            limit = int(request.GET.get("limit", os.getenv("SEARCH_DEFAULT_LIMIT", "20")))
            page = int(request.GET.get("page", "1"))
        except ValueError:
            logger.warning("Search request rejected because limit/page are invalid")
            return JsonResponse({"error": "limit and page must be integers"}, status=400)

        if limit <= 0 or page <= 0:
            logger.warning("Search request rejected because limit/page are non-positive")
            return JsonResponse({"error": "limit and page must be greater than zero"}, status=400)
        logger.info("Starting global search query=%s limit=%s page=%s", query, limit, page)

        try:
            service = SongSearchService(search_repository=TypesenseSongRepository())
            result = service.search(query=query, limit=limit, page=page)
        except Exception:
            logger.exception("Unexpected error while searching songs query=%s", query)
            return JsonResponse({"error": "failed to search songs"}, status=500)

        hits = result.get("hits", [])
        songs = [hit.get("document", {}) for hit in hits]
        logger.info(
            "Global search completed query=%s found=%s returned=%s",
            query,
            result.get("found", 0),
            len(songs),
        )

        return JsonResponse(
            {
                "query": query,
                "found": result.get("found", 0),
                "count": len(songs),
                "page": result.get("page", page),
                "songs": songs,
            },
            status=200,
        )
