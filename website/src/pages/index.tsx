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
  const [stats, setStats] = useState<{
    platform_counts: Record<string, number>;
    year_counts: Record<string, number>;
    category_counts: Record<string, number>;
    monthly_completions: Record<string, number>;
    avg_hours_by_platform: Record<string, number>;
  } | null>(null);
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
  usePollVersion(load, 8000); // re-fetch when Excel changes

  const platformData = useMemo(() =>
    stats ? Object.entries(stats.platform_counts).map(([name, value]) => ({ name, value })) : [], [stats]
  );
  const yearData = useMemo(() =>
    stats ? Object.entries(stats.year_counts).map(([year, value]) => ({ year, value })) : [], [stats]
  );

  const categoryData = useMemo(
  () => stats ? Object.entries(stats.category_counts).map(([name, value]) => ({ name, value })) : [],
  [stats]
);

// sort YYYY-MM ascending
const monthlyData = useMemo(() => {
  if (!stats) return [];
  const rows = Object.entries(stats.monthly_completions).map(([month, value]) => ({ month, value }));
  rows.sort((a, b) => a.month.localeCompare(b.month));
  return rows;
}, [stats]);

const hoursData = useMemo(
  () => stats ? Object.entries(stats.avg_hours_by_platform).map(([platform, value]) => ({ platform, value })) : [],
  [stats]
);

// Simple color palette
const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042", "#AF19FF", "#E91E63", "#9C27B0"];


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
          <div style={{ display: "flex", justifyContent: "center", margin: "20px" }}>
            <div>
              <h4>Loading data…</h4>
              <div style={{ display: "flex", justifyContent: "center" }}>
                <img src="https://i.gifer.com/ZZ5H.gif" width={40} alt="Loading spinner" />
              </div>
            </div>
          </div>
        )}

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

        {!loading && stats && (
            <div className="row" style={{ marginTop: 24 }}>
          <div className="col col--4">
            <div className="card" style={{ padding: 16 }}>
              <h3>Categories</h3>
              <div style={{ width: "100%", height: 260 }}>
                <ResponsiveContainer>
                  <PieChart>
                    <Pie data={categoryData} dataKey="value" nameKey="name" outerRadius={90} label>
                      {categoryData.map((_, i) => (
                        <Cell key={i} fill={COLORS[i % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>

          <div className="col col--4">
            <div className="card" style={{ padding: 16 }}>
              <h3>Monthly Completions</h3>
              <div style={{ width: "100%", height: 260 }}>
                <ResponsiveContainer>
                  <BarChart data={monthlyData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis allowDecimals={false} />
                    <Tooltip />
                    <Bar dataKey="value" fill="#82ca9d" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>

          <div className="col col--4">
            <div className="card" style={{ padding: 16 }}>
              <h3>Avg Hours by Platform</h3>
              <div style={{ width: "100%", height: 260 }}>
                <ResponsiveContainer>
                  <BarChart data={hoursData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="platform" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="value" fill="#8884d8" />
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
                      <td>{g.completed_on ? g.completed_on : "Unknown"}</td>
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
