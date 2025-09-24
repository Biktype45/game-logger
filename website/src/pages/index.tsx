import React, { useEffect, useMemo, useState } from "react";
import Layout from "@theme/Layout";
import { fetchGames, fetchStats } from "../lib/api";
import { usePollVersion } from "../hooks/usePollVersion";
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid } from "recharts";

type Game = {
  idx: number; title: string; platform?: string;
  completed_on?: string; hours?: number; rating?: string; developer?: string;
};

export default function Home(): JSX.Element {
  const [games, setGames] = useState<Game[]>([]);
  const [stats, setStats] = useState<{ platform_counts: Record<string, number>; year_counts: Record<string, number> } | null>(null);
  const [loading, setLoading] = useState(true);

  async function load() {
    setLoading(true);
    const [g, s] = await Promise.all([fetchGames(), fetchStats()]);
    setGames(g);
    setStats(s);
    setLoading(false);
  }

  useEffect(() => { load(); }, []);
  usePollVersion(load, 8000); // re-fetch when Excel changes

  const platformData = useMemo(() =>
    stats ? Object.entries(stats.platform_counts).map(([name, value]) => ({ name, value })) : [], [stats]
  );
  const yearData = useMemo(() =>
    stats ? Object.entries(stats.year_counts).map(([year, value]) => ({ year, value })) : [], [stats]
  );

  return (
    <Layout title="Game Logger" description="Your completed games, at a glance">
      <main className="container margin-vert--lg">
        <h1 style={{ marginBottom: 8 }}>Game Logger Dashboard</h1>
        <p style={{ opacity: 0.8, marginTop: 0 }}>Read-only. Update the Excel to refresh data.</p>

        {loading && <p>Loading…</p>}

        {!loading && stats && (
          <div className="row">
            <div className="col col--6">
              <div className="card" style={{ padding: 16 }}>
                <h3>Platforms</h3>
                <div style={{ width: "100%", height: 280 }}>
                  <ResponsiveContainer>
                    <PieChart>
                      <Pie data={platformData} dataKey="value" nameKey="name" outerRadius={110} label />
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
            <div className="col col--6">
              <div className="card" style={{ padding: 16 }}>
                <h3>Completions by Year</h3>
                <div style={{ width: "100%", height: 280 }}>
                  <ResponsiveContainer>
                    <BarChart data={yearData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="year" />
                      <YAxis allowDecimals={false} />
                      <Tooltip />
                      <Bar dataKey="value" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
          </div>
        )}

        {!loading && (
          <div className="card" style={{ padding: 16, marginTop: 24 }}>
            <h3>Games ({games.length})</h3>
            <div style={{ overflowX: "auto" }}>
              <table className="table">
                <thead>
                  <tr>
                    <th>#</th><th>Title</th><th>Platform</th><th>Completed On</th><th>Hours</th><th>Rating</th><th>Developer</th>
                  </tr>
                </thead>
                <tbody>
                  {games.map(g => (
                    <tr key={g.idx}>
                      <td>{g.idx + 1}</td>
                      <td>{g.title}</td>
                      <td>{g.platform ?? ""}</td>
                      <td>{g.completed_on ?? ""}</td>
                      <td>{g.hours ?? ""}</td>
                      <td>{g.rating ?? ""}</td>
                      <td>{g.developer ?? ""}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <p style={{ fontSize: 12, opacity: 0.7, marginTop: 8 }}>
              Tip: Edit the Excel → the page auto-refreshes within ~8 seconds.
            </p>
          </div>
        )}
      </main>
    </Layout>
  );
}
