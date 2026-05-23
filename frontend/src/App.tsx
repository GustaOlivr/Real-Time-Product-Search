import { FormEvent, useMemo, useState } from "react";

import { SongCard } from "./components/SongCard";
import { TopBar } from "./components/TopBar";
import { ingestSongs, searchSongs, seedTopHits, type Song } from "./services/api";

type Toast = {
  kind: "success" | "error";
  message: string;
};

export function App() {
  const [searchQuery, setSearchQuery] = useState("daft punk");
  const [ingestQuery, setIngestQuery] = useState("weeknd");
  const [limit, setLimit] = useState(12);

  const [songs, setSongs] = useState<Song[]>([]);
  const [found, setFound] = useState(0);
  const [busyAction, setBusyAction] = useState<string | null>(null);
  const [toast, setToast] = useState<Toast | null>(null);

  const subtitle = useMemo(() => {
    if (found === 0) return "Run a search to populate your grid.";
    return `${found} tracks found in Typesense.`;
  }, [found]);

  const runSearch = async (event?: FormEvent) => {
    event?.preventDefault();
    setBusyAction("search");
    setToast(null);

    try {
      const data = await searchSongs(searchQuery, limit, 1);
      setSongs(data.songs);
      setFound(data.found);
      setToast({ kind: "success", message: `Loaded ${data.count} tracks.` });
    } catch (error) {
      setToast({
        kind: "error",
        message: error instanceof Error ? error.message : "Failed to search songs.",
      });
    } finally {
      setBusyAction(null);
    }
  };

  const runSeed = async () => {
    setBusyAction("seed");
    setToast(null);

    try {
      const result = await seedTopHits();
      setToast({
        kind: "success",
        message: `${result.total_indexed} tracks indexed from top hits.`,
      });
      await runSearch();
    } catch (error) {
      setToast({
        kind: "error",
        message: error instanceof Error ? error.message : "Failed to seed top hits.",
      });
      setBusyAction(null);
    }
  };

  const runIngest = async (event: FormEvent) => {
    event.preventDefault();
    setBusyAction("ingest");
    setToast(null);

    try {
      const result = await ingestSongs(ingestQuery, limit);
      setToast({
        kind: "success",
        message: `${result.count} tracks ingested for '${ingestQuery}'.`,
      });
      setSearchQuery(ingestQuery);
      await runSearch();
    } catch (error) {
      setToast({
        kind: "error",
        message: error instanceof Error ? error.message : "Failed to ingest songs.",
      });
      setBusyAction(null);
    }
  };

  return (
    <div className="app-shell">
      <div className="backdrop-gradient" />
      <main className="layout">
        <TopBar />

        <section className="hero-panel">
          <p className="hero-panel__pill">Global Search + Seed Control</p>
          <h2>Search, seed and expand your catalog with a single dashboard</h2>
          <p>{subtitle}</p>

          <div className="hero-panel__actions">
            <button
              className="btn btn--primary"
              onClick={runSeed}
              disabled={busyAction !== null}
            >
              {busyAction === "seed" ? "Seeding..." : "Seed Top Hits"}
            </button>
            <form className="inline-form" onSubmit={runSearch}>
              <input
                value={searchQuery}
                onChange={(event) => setSearchQuery(event.target.value)}
                placeholder="Search in Typesense"
              />
              <button className="btn btn--ghost" disabled={busyAction !== null}>
                {busyAction === "search" ? "Searching..." : "Search"}
              </button>
            </form>
          </div>
        </section>

        <section className="control-grid">
          <form className="panel" onSubmit={runIngest}>
            <h3>Spotify Ingestion</h3>
            <p>Index tracks from Spotify directly into Typesense.</p>

            <label>
              Query
              <input
                value={ingestQuery}
                onChange={(event) => setIngestQuery(event.target.value)}
                placeholder="e.g. Bruno Mars"
              />
            </label>

            <label>
              Limit
              <input
                type="number"
                min={1}
                max={50}
                value={limit}
                onChange={(event) => setLimit(Number(event.target.value))}
              />
            </label>

            <button className="btn btn--primary" disabled={busyAction !== null}>
              {busyAction === "ingest" ? "Indexing..." : "Ingest to Typesense"}
            </button>
          </form>

          <aside className="panel panel--glass">
            <h3>System Notes</h3>
            <ul>
              <li>Use seed to bootstrap fast.</li>
              <li>Search endpoint reads global index.</li>
              <li>UI is tuned for dark Spotify styling.</li>
            </ul>
            {toast && (
              <p className={`toast toast--${toast.kind}`} role="status">
                {toast.message}
              </p>
            )}
          </aside>
        </section>

        <section className="results-grid">
          {songs.map((song) => (
            <SongCard key={song.id} song={song} />
          ))}
        </section>
      </main>
    </div>
  );
}
