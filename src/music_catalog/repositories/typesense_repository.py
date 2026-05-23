import os

import typesense
from typesense.exceptions import ObjectNotFound

from music_catalog.domain.entities import Song


class TypesenseSongRepository:
    def __init__(self) -> None:
        host = os.getenv("TYPESENSE_HOST", "typesense")
        port = os.getenv("TYPESENSE_PORT", "8108")
        protocol = os.getenv("TYPESENSE_PROTOCOL", "http")
        api_key = os.getenv("TYPESENSE_API_KEY", "xyz")

        self.collection_name = os.getenv("TYPESENSE_COLLECTION", "songs")
        self.client = typesense.Client(
            {
                "nodes": [{"host": host, "port": port, "protocol": protocol}],
                "api_key": api_key,
                "connection_timeout_seconds": 5,
            }
        )
        self._ensure_collection()

    def _ensure_collection(self) -> None:
        schema = {
            "name": self.collection_name,
            "fields": [
                {"name": "id", "type": "string"},
                {"name": "title", "type": "string"},
                {"name": "artist", "type": "string"},
                {"name": "album", "type": "string"},
                {"name": "popularity", "type": "int32"},
                {"name": "duration_ms", "type": "int32"},
            ],
            "default_sorting_field": "popularity",
        }

        try:
            self.client.collections[self.collection_name].retrieve()
        except ObjectNotFound:
            self.client.collections.create(schema)

    def upsert_song(self, song: Song) -> dict:
        document = song.to_typesense_document()
        return self.client.collections[self.collection_name].documents.upsert(document)
