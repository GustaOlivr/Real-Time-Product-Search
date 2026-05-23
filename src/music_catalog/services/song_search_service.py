import logging

from music_catalog.domain.repositories import SongSearchRepository

logger = logging.getLogger(__name__)


class SongSearchService:
    def __init__(self, search_repository: SongSearchRepository) -> None:
        self.search_repository = search_repository

    def search(self, query: str, limit: int, page: int) -> dict:
        logger.debug("Searching songs query=%s limit=%s page=%s", query, limit, page)
        return self.search_repository.search_songs(query=query, limit=limit, page=page)
