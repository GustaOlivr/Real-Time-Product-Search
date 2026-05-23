from django.urls import path

from music_catalog.controllers.song_controller import SongIngestionController

urlpatterns = [
    path("songs/ingest", SongIngestionController.as_view(), name="songs-ingest"),
]
