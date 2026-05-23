from typing import Protocol

from music_catalog.domain.entities import Song


class SongSearchRepository(Protocol):
    def upsert_song(self, song: Song) -> dict:
        ...

    def search_songs(self, query: str, limit: int, page: int) -> dict:
        ...


class SpotifyRepository(Protocol):
    def search_tracks(self, query: str, limit: int) -> list[Song]:
        ...
