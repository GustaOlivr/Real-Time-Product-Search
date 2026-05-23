import type { Song } from "../services/api";

type SongCardProps = {
  song: Song;
};

function formatDuration(ms: number): string {
  const minutes = Math.floor(ms / 60000);
  const seconds = Math.floor((ms % 60000) / 1000)
    .toString()
    .padStart(2, "0");
  return `${minutes}:${seconds}`;
}

export function SongCard({ song }: SongCardProps) {
  return (
    <article className="song-card">
      <div className="song-card__halo" />
      <p className="song-card__artist">{song.artist}</p>
      <h3 className="song-card__title">{song.title}</h3>
      <p className="song-card__album">{song.album}</p>
      <div className="song-card__meta">
        <span>Popularity {song.popularity}</span>
        <span>{formatDuration(song.duration_ms)}</span>
      </div>
    </article>
  );
}
