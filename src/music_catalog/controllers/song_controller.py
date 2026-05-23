import json
import os

from django.http import HttpRequest, JsonResponse
from django.views import View

from music_catalog.repositories.spotify_repository import SpotifyHttpRepository
from music_catalog.repositories.typesense_repository import TypesenseSongRepository
from music_catalog.services.song_ingestion_service import SongIngestionService


class SongIngestionController(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        payload = json.loads(request.body or "{}")
        query = payload.get("query")

        if not query:
            return JsonResponse({"error": "query is required"}, status=400)

        limit = int(payload.get("limit", os.getenv("SEARCH_DEFAULT_LIMIT", "20")))

        service = SongIngestionService(
            spotify_repository=SpotifyHttpRepository(),
            search_repository=TypesenseSongRepository(),
        )

        songs = service.ingest_from_spotify(query=query, limit=limit)

        return JsonResponse(
            {
                "message": "songs indexed",
                "count": len(songs),
                "songs": [song.to_typesense_document() for song in songs],
            },
            status=201,
        )
