export type Stats = {
  platform_counts: Record<string, number>;
  year_counts: Record<string, number>;
  category_counts: Record<string, number>;
  monthly_completions: Record<string, number>;
  avg_hours_by_platform: Record<string, number>;

  // 🆕 Metacritic analytics
  avg_metascore_by_platform: Record<string, number>;
  must_play_pct_by_platform: Record<string, number>;
  metascore_histogram: Record<string, number>;
  top_devs_by_metascore: {
    developer: string;
    avg_metascore: number;
    count: number;
  }[];
};

export const API_BASE = "http://127.0.0.1:8000/api";

export async function fetchGames() {
  const r = await fetch(`${API_BASE}/games`);
  if (!r.ok) throw new Error(`games: ${r.status}`);
  return r.json();
}

export async function fetchStats(): Promise<Stats> {
  const r = await fetch(`${API_BASE}/stats`);
  if (!r.ok) throw new Error(`stats: ${r.status}`);
  return r.json() as Promise<Stats>;
}
