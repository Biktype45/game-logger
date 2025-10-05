import React, { useEffect, useMemo, useState } from "react";
import Layout from "@theme/Layout";
import {
  PieChart, Pie, Tooltip, ResponsiveContainer,
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Cell
} from "recharts";
import { fetchGames, fetchStats, type Stats } from "../lib/api";
import "../css/custom-dashboard.css";

type Game = {
  idx: number;
  title: string;
  platform?: string;
  completed_on?: string;
  hours?: number;
  rating?: string;
  developer?: string;
  metascore?: number;
  metacritic_url?: string;
};

function getMetascoreColor(score: number): string {
  if (score >= 90) return "#00C853";  // green
  if (score >= 80) return "#2196F3";  // blue
  if (score >= 70) return "#FB8C00";  // orange
  return "#9E9E9E";                   // gray
}

function shortenPlatform(name: string): string {
  const lower = name.toLowerCase();
  if (lower.includes("nintendo")) return "Switch";
  if (lower.includes("playstation 5") || lower.includes("ps5")) return "PS5";
  if (lower.includes("playstation 4") || lower.includes("ps4")) return "PS4";
  if (lower.includes("xbox")) return "Xbox";
  if (lower.includes("pc")) return "PC";
  return name;
}


export default function Home(): JSX.Element {
  const [games, setGames] = useState<Game[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    try {
      setLoading(true);
      setError(null);
      const [g, s] = await Promise.all([fetchGames(), fetchStats()]);
      setGames(g);
      setStats(s);
    } catch (e: any) {
      setError("⚠️ Backend API not reachable at port 8000");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { load(); }, []);

  // Base analytics
  const platformData = useMemo(
    () => stats ? Object.entries(stats.platform_counts).map(([name, value]) => ({ name, value })) : [],
    [stats]
  );

  const yearData = useMemo(
    () => stats ? Object.entries(stats.year_counts).map(([year, value]) => ({ year, value })) : [],
    [stats]
  );

  const avgMetaData = useMemo(
  () => stats
    ? Object.entries(stats.avg_metascore_by_platform)
        .map(([platform, value]) => ({ platform: shortenPlatform(platform), value }))
    : [],
  [stats]
);

const mustPlayData = useMemo(
  () => stats
    ? Object.entries(stats.must_play_pct_by_platform)
        .map(([platform, value]) => ({ platform: shortenPlatform(platform), value }))
    : [],
  [stats]
);


  const histoData = useMemo(
    () => stats ? Object.entries(stats.metascore_histogram).map(([range, value]) => ({ range, value })) : [],
    [stats]
  );

  const topDevsData = useMemo(() => stats?.top_devs_by_metascore ?? [], [stats]);

  const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042", "#AF19FF"];

  return (
    <Layout title="Game Logger" description="Your completed games, at a glance">
      <main className="container margin-vert--lg">
        <h1 style={{ marginBottom: 8 }}>Game Logger Dashboard</h1>

        {error && (
          <div style={{ background: "#ffe4e1", color: "#a00", padding: "8px 12px", borderRadius: 6, marginBottom: 16 }}>
            {error}
          </div>
        )}
        <p style={{ opacity: 0.8, marginTop: 0 }}>Read-only. Update the Excel to refresh data.</p>

        {loading && (
          <div style={{ textAlign: "center", marginTop: 40 }}>
            <h4>Loading data…</h4>
            <img src="https://i.gifer.com/ZZ5H.gif" width={40} alt="Loading spinner" />
          </div>
        )}

        {/* Row 1 — Platforms + Years */}
        {!loading && stats && (
          <div className="row">
            <div className="col col--6">
              <div className="card" style={{ padding: 16 }}>
                <h3>Platforms</h3>
                <div style={{ width: "100%", height: 280 }}>
                  <ResponsiveContainer>
                    <PieChart>
                      <Pie data={platformData} dataKey="value" nameKey="name" outerRadius={110} label>
                        {platformData.map((_, i) => (
                          <Cell key={i} fill={COLORS[i % COLORS.length]} />
                        ))}
                      </Pie>
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
                      <Bar dataKey="value" fill="#8884d8" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Row 3 — Metacritic Highlights */}
        {!loading && stats && (
          <>
            <div className="row" style={{ marginTop: 24 }}>
              <div className="col col--4">
                <div className="card" style={{ padding: 16 }}>
                  <h3>Avg Metascore by Platform</h3>
                  <div style={{ width: "100%", height: 260 }}>
                    <ResponsiveContainer>
                      <BarChart data={avgMetaData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="platform" />
                        <YAxis />
                        <Tooltip />
                        <Bar dataKey="value" fill="#2196F3" />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              </div>

              <div className="col col--4">
                <div className="card" style={{ padding: 16 }}>
                  <h3>% Must-Play (≥90)</h3>
                  <div style={{ width: "100%", height: 260 }}>
                    <ResponsiveContainer>
                      <BarChart data={mustPlayData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="platform" />
                        <YAxis />
                        <Tooltip />
                        <Bar dataKey="value" fill="#00C853" />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              </div>

              <div className="col col--4">
                <div className="card" style={{ padding: 16 }}>
                  <h3>Metascore Distribution</h3>
                  <div style={{ width: "100%", height: 260 }}>
                    <ResponsiveContainer>
                      <BarChart data={histoData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="range" />
                        <YAxis allowDecimals={false} />
                        <Tooltip />
                        <Bar dataKey="value" fill="#FB8C00" />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              </div>
            </div>

            {/* Row 4 — Top Developers */}
            <div className="row" style={{ marginTop: 24 }}>
              <div className="col col--12">
                <div className="card" style={{ padding: 16 }}>
                  <h3>Top Developers by Avg Metascore</h3>
                  <div style={{ width: "100%", height: 300 }}>
                    <ResponsiveContainer>
                      <BarChart
                        data={topDevsData}
                        layout="vertical"
                        margin={{ top: 5, right: 30, left: 60, bottom: 5 }}
                      >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis type="number" />
                        <YAxis dataKey="developer" type="category" />
                        <Tooltip />
                        <Bar dataKey="avg_metascore" fill="#8884d8" />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              </div>
            </div>
          </>
        )}

        {/* Games Table */}
        {!loading && (
          <div className="card" style={{ padding: 16, marginTop: 24 }}>
            <h3>Games ({games.length})</h3>
            <div style={{ overflowX: "auto" }}>
              <table className="table">
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Title</th>
                    <th>Platform</th>
                    <th>Completed On</th>
                    <th>Hours</th>
                    <th>Category</th>
                    <th>Developer</th>
                    <th>Metascore</th>
                  </tr>
                </thead>
                <tbody>
                  {games.map((g) => (
                    <tr key={g.idx}>
                      <td>{g.idx + 1}</td>
                      <td>{g.title}</td>
                      <td>{g.platform ?? ""}</td>
                      <td>{g.completed_on ?? "Unknown"}</td>
                      <td>{g.hours ?? ""}</td>
                      <td>{g.rating ?? ""}</td>
                      <td>{g.developer ?? ""}</td>
                      <td>
                        {g.metascore ? (
                          <a
                            href={g.metacritic_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            style={{
                              backgroundColor: getMetascoreColor(g.metascore),
                              color: "white",
                              padding: "4px 8px",
                              borderRadius: "12px",
                              fontWeight: "bold",
                              textDecoration: "none",
                            }}
                          >
                            {g.metascore}
                          </a>
                        ) : (
                          <span style={{ opacity: 0.6 }}>N/A</span>
                        )}
                      </td>
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
