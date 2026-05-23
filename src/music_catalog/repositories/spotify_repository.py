import base64
import logging
import os

import requests

from music_catalog.domain.entities import Song

logger = logging.getLogger(__name__)


class SpotifyHttpRepository:
    def __init__(self) -> None:
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID", "")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET", "")
        self.base_url = os.getenv("SPOTIFY_BASE_URL", "https://api.spotify.com/v1")
        self.auth_url = os.getenv("SPOTIFY_AUTH_URL", "https://accounts.spotify.com/api/token")

    def _get_access_token(self) -> str:
        logger.debug("Requesting Spotify access token")
        credentials = f"{self.client_id}:{self.client_secret}".encode("utf-8")
        basic_token = base64.b64encode(credentials).decode("utf-8")

        response = requests.post(
            self.auth_url,
            headers={
                "Authorization": f"Basic {basic_token}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={"grant_type": "client_credentials"},
            timeout=15,
        )
        response.raise_for_status()
        logger.debug("Spotify access token fetched successfully")
        return response.json()["access_token"]

    def search_tracks(self, query: str, limit: int) -> list[Song]:
        logger.info("Searching tracks on Spotify query=%s limit=%s", query, limit)
        token = self._get_access_token()
        response = requests.get(
            f"{self.base_url}/search",
            headers={"Authorization": f"Bearer {token}"},
            params={"q": query, "type": "track", "limit": limit},
            timeout=15,
        )
        response.raise_for_status()

        tracks = response.json().get("tracks", {}).get("items", [])
        logger.info("Spotify returned tracks query=%s count=%s", query, len(tracks))
        songs: list[Song] = []

        for track in tracks:
            songs.append(
                Song(
                    spotify_id=track.get("id", ""),
                    title=track.get("name", ""),
                    artist=(track.get("artists") or [{}])[0].get("name", ""),
                    album=(track.get("album") or {}).get("name", ""),
                    popularity=track.get("popularity", 0),
                    duration_ms=track.get("duration_ms", 0),
                )
            )

        return songs
