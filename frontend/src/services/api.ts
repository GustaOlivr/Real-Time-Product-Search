export type Song = {
  id: string;
  title: string;
  artist: string;
  album: string;
  popularity: number;
  duration_ms: number;
};

type SearchResponse = {
  query: string;
  found: number;
  count: number;
  page: number;
  songs: Song[];
};

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8012/api/v1";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const headers = new Headers(init?.headers ?? {});

  if (init?.body && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers,
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed with status ${response.status}`);
  }

  return (await response.json()) as T;
}

export async function seedTopHits(): Promise<{
  message: string;
  total_indexed: number;
  indexed_by_query: Record<string, number>;
}> {
  return request("/songs/seed/top-hits", {
    method: "POST",
    body: JSON.stringify({}),
  });
}

export async function ingestSongs(query: string, limit: number): Promise<{
  message: string;
  count: number;
  songs: Song[];
}> {
  return request("/songs/ingest", {
    method: "POST",
    body: JSON.stringify({ query, limit }),
  });
}

export async function searchSongs(
  query: string,
  limit = 12,
  page = 1
): Promise<SearchResponse> {
  const encoded = encodeURIComponent(query);
  return request(`/songs/search?q=${encoded}&limit=${limit}&page=${page}`);
}
