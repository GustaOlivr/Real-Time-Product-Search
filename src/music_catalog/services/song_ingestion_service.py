import logging

from music_catalog.domain.entities import Song
from music_catalog.domain.repositories import SongSearchRepository, SpotifyRepository

logger = logging.getLogger(__name__)


class SongIngestionService:
    def __init__(self, spotify_repository: SpotifyRepository, search_repository: SongSearchRepository) -> None:
        self.spotify_repository = spotify_repository
        self.search_repository = search_repository

    def ingest_from_spotify(self, query: str, limit: int) -> list[Song]:
        logger.debug("Fetching songs from Spotify query=%s limit=%s", query, limit)
        songs = self.spotify_repository.search_tracks(query=query, limit=limit)
        logger.debug("Fetched songs from Spotify query=%s count=%s", query, len(songs))
        for song in songs:
            self.search_repository.upsert_song(song)
        logger.debug("Persisted songs in search repository query=%s count=%s", query, len(songs))
        return songs
