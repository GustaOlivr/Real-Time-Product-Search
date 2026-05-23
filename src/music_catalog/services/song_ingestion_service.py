from music_catalog.domain.entities import Song
from music_catalog.domain.repositories import SongSearchRepository, SpotifyRepository


class SongIngestionService:
    def __init__(self, spotify_repository: SpotifyRepository, search_repository: SongSearchRepository) -> None:
        self.spotify_repository = spotify_repository
        self.search_repository = search_repository

    def ingest_from_spotify(self, query: str, limit: int) -> list[Song]:
        songs = self.spotify_repository.search_tracks(query=query, limit=limit)
        for song in songs:
            self.search_repository.upsert_song(song)
        return songs
