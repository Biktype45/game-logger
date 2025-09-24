export const API_BASE = "http://127.0.0.1:8000/api"

export async function fetchGames() {
  const r = await fetch(`${API_BASE}/games`);
  if (!r.ok) throw new Error(`games: ${r.status}`);
  return r.json() as Promise<Array<{
    idx: number; title: string; platform?: string;
    completed_on?: string; hours?: number; rating?: string; developer?: string;
  }>>;
}

export async function fetchStats() {
  const r = await fetch(`${API_BASE}/stats`);
  if (!r.ok) throw new Error(`stats: ${r.status}`);
  return r.json() as Promise<{ platform_counts: Record<string, number>; year_counts: Record<string, number> }>;
}

export async function fetchVersion() {
  const r = await fetch(`${API_BASE}/version`);
  if (!r.ok) throw new Error(`version: ${r.status}`);
  return r.json() as Promise<{ version: string }>;
}
