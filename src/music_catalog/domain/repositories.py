from typing import Protocol

from music_catalog.domain.entities import Song


class SongSearchRepository(Protocol):
    def upsert_song(self, song: Song) -> dict:
        ...


class SpotifyRepository(Protocol):
    def search_tracks(self, query: str, limit: int) -> list[Song]:
        ...
