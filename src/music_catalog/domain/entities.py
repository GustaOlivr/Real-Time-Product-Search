from dataclasses import dataclass


@dataclass(slots=True)
class Song:
    spotify_id: str
    title: str
    artist: str
    album: str
    popularity: int
    duration_ms: int

    def to_typesense_document(self) -> dict:
        return {
            "id": self.spotify_id,
            "title": self.title,
            "artist": self.artist,
            "album": self.album,
            "popularity": self.popularity,
            "duration_ms": self.duration_ms,
        }
