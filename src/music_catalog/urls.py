from django.urls import path

from music_catalog.controllers.song_controller import (
    SongGlobalSearchController,
    SongIngestionController,
    SongTopHitsSeedController,
)

urlpatterns = [
    path("songs/ingest", SongIngestionController.as_view(), name="songs-ingest"),
    path(
        "songs/seed/top-hits",
        SongTopHitsSeedController.as_view(),
        name="songs-seed-top-hits",
    ),
    path("songs/search", SongGlobalSearchController.as_view(), name="songs-search"),
]
