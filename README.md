# 🕹️ Game Logger  
### *Track your completed games, analytics, and Metacritic insights — powered by FastAPI + Docusaurus*

![screenshot](https://user-images.githubusercontent.com/example/game-logger-dashboard.png)
*A modern, interactive dashboard to visualize your gaming history.*

---

## 🌟 Overview

**Game Logger** is a full-stack application that transforms your personal game log Excel sheet into an interactive web dashboard.  
It uses a **Python FastAPI** backend for data + analytics, and a **React-based Docusaurus** frontend for visualization.

### 🎮 Key Features
- Syncs directly with your local or cloud Excel sheet  
- Auto-fetches Metacritic scores via RAWG API  
- Beautiful, modern analytics dashboard  
- Auto-updates whenever Excel data changes  
- Ready for free hosting via **Render + GitHub Pages**

---

## 🧩 Tech Stack

| Layer | Technology | Purpose |
|-------|-------------|----------|
| Backend | **FastAPI**, **Uvicorn** | REST API + analytics engine |
| Database | **SQLite** | Cache for Metacritic data |
| Frontend | **Docusaurus (React + TypeScript)** | Interactive dashboard site |
| Data Source | **Excel (.xlsx)** | Stores your completed games |
| External API | **RAWG API** | Fetches Metacritic scores |
| Dev Tooling | **Concurrently** | Run backend + frontend together |

---

## 📂 Project Structure

```

game-logger/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entrypoint
│   │   ├── routers/             # API routes
│   │   ├── services/            # Excel, enrichment, analytics logic
│   │   ├── models.py
│   │   └── utils/banner.py
│   ├── requirements.txt
│   └── My Completed Games List-Rakuyo.xlsx
│
├── website/
│   ├── src/
│   │   ├── lib/api.ts           # Fetch logic for stats + games
│   │   ├── pages/index.tsx      # Dashboard layout
│   │   └── css/custom-dashboard.css
│   ├── docusaurus.config.ts
│   ├── package.json
│   └── build/
│
├── package.json                 # Root concurrent runner
└── README.md                    # You are here

````

---

## ⚙️ Local Development

### 🧱 Requirements
- Python ≥ 3.10  
- Node.js ≥ 18  
- npm or yarn  
- RAWG API key → [Get yours here](https://api.rawg.io/docs/)

### 🪄 1. Clone the repo
```bash
git clone https://github.com/<your-username>/game-logger.git
cd game-logger
````

### 🪄 2. Backend setup

```bash
cd backend
pip install -r requirements.txt
# create .env
echo RAWG_API_KEY=your_api_key_here > .env
cd ..
```

### 🪄 3. Frontend setup

```bash
cd website
npm install
cd ..
```

### 🪄 4. Start both together

At the repo root:

```bash
npm run dev
```

This launches:

* 🧠 FastAPI backend → [http://127.0.0.1:8000](http://127.0.0.1:8000)
* 💻 Docusaurus site → [http://localhost:3000](http://localhost:3000)

---

## 📊 Key API Endpoints

| Endpoint                         | Description                                             |
| -------------------------------- | ------------------------------------------------------- |
| `/api/games`                     | Returns all games from Excel                            |
| `/api/games?enrich=true`         | Enriches with RAWG/Metacritic data                      |
| `/api/stats`                     | Returns analytics (platforms, metascores, dev rankings) |
| `/api/meta/test?title=GameTitle` | Manual test enrichment                                  |

---

## 🧠 Architecture Highlights

* **Excel → FastAPI → JSON → React pipeline**
* Auto-updates Excel with Metacritic scores (persisted after enrichment)
* Smart caching via SQLite (avoids hitting API rate limits)
* Auto-enrichment of missing scores on backend startup
* Clean dashboard visuals with color-coded Metascore badges

---

## 🧑‍💻 Deployment (Free)

### 🔹 Backend (Render)

1. Push your repo to GitHub
2. Go to [Render.com](https://render.com) → *New Web Service*
3. Use these commands:

   ```
   Build: pip install -r backend/requirements.txt
   Start: cd backend && uvicorn app.main:app --host 0.0.0.0 --port 10000
   ```
4. Add env var: `RAWG_API_KEY`

### 🔹 Frontend (GitHub Pages)

1. In `website/docusaurus.config.ts`:

   ```ts
   url: 'https://<your-username>.github.io',
   baseUrl: '/game-logger/',
   ```
2. Deploy:

   ```bash
   cd website
   npm run build
   npm run deploy
   ```

### 🔹 Connect them

In `website/src/lib/api.ts`:

```ts
export const API_BASE = "https://game-logger-api.onrender.com/api";
```

---

## 🧠 Future Enhancements

* 🪩 Add authentication for multi-user tracking
* 📈 Compare stats across years / genres
* 💾 Cloud sync for Excel (Google Sheets API)
* 🎨 Theme switch (Light / Neon Dark)
* 🧰 Export analytics as PDF

---

## 🧡 Credits

* [RAWG.io API](https://rawg.io/apidocs) for Metacritic and game data
* [Docusaurus](https://docusaurus.io/) for the React-powered frontend
* [Render](https://render.com/) & [GitHub Pages](https://pages.github.com/) for free hosting
* Icons from [Lucide](https://lucide.dev/)

---

## 🪄 Quick Commands Reference

| Command           | Description                           |
| ----------------- | ------------------------------------- |
| `npm run dev`     | Start backend + frontend concurrently |
| `npm run dev:api` | Start only the backend                |
| `npm run dev:web` | Start only the frontend               |
| `npm run build`   | Build the Docusaurus site             |
| `npm run deploy`  | Deploy to GitHub Pages                |

---

## 📜 License

MIT License © 2025 [Your Name / Bikram Mitra]
Feel free to fork, remix, and extend the project for your own logs.
