# howLikelyWasThat

> Given any player's attacking season, how statistically likely — or absurd — was it?

Messi's 2011/12 La Liga season: 50 goals. Was that a 3-sigma outlier? A 5-sigma one? This tool answers that. Enter any player and season, define your comparison pool, and get back a distribution, a position on it, and a probability.

---

## What It Does

1. **Scrapes** historical player season data from fbref (La Liga first, then Serie A — last 20 seasons per league)
2. **Stores** it in a structured Postgres database via Supabase
3. **Analyses** the distribution of goal contributions across that pool — tests for normality, fits appropriately
4. **Serves** a FastAPI backend that computes where any player-season sits relative to a user-defined comparison pool
5. **Displays** a Next.js web app where anyone can search a player, pick a metric, define a pool, and see a histogram with their player highlighted and a probability statement

---

## Core Concept

A user selects:
- A **player + season** (e.g. Messi, 2011/12)
- A **metric** (goals / non-penalty goals / assists / G+A, raw or per 90)
- A **comparison pool** (defaults to same league + season; can be expanded to a range of seasons, across leagues, with a minimum goal threshold)

The app tests whether the pool is normally distributed. If it is, it computes z-scores and tail probabilities. If not, it fits an appropriate distribution or falls back to percentile rank. The result: a histogram, the player's position on it, and a plain-English probability statement.

---

## Stack

| Layer | Technology | Purpose |
|---|---|---|
| Scraping | Python + `requests` / `BeautifulSoup` | Fetch player season data from fbref |
| Database | Supabase (Postgres) | Store and query player season stats |
| Backend | FastAPI (Python) | API layer, statistical analysis |
| Frontend | Next.js (React) | Player search, metric selection, charts |
| Charts | Recharts / Plotly | Distribution histogram, player marker |
| Deployment | Vercel (frontend) + Railway (backend) | Public hosting |

---

## Data Model

Single unified table: `player_seasons`

| Column | Type | Notes |
|---|---|---|
| `id` | uuid | Primary key |
| `fbref_id` | text | Player identifier from fbref |
| `player_name` | text | Display name |
| `team` | text | Club that season |
| `league` | text | e.g. `la_liga`, `serie_a` |
| `season` | text | e.g. `2011-12` |
| `apps` | int | Appearances |
| `minutes` | int | Minutes played |
| `goals` | int | Total goals |
| `npg` | int | Non-penalty goals |
| `assists` | int | Assists |
| `ga` | int | Goals + assists |
| `npga` | int | Non-penalty goals + assists |
| `goals_p90` | float | Goals per 90 minutes |
| `npg_p90` | float | Non-penalty goals per 90 |
| `assists_p90` | float | Assists per 90 |
| `ga_p90` | float | G+A per 90 |
| `scraped_at` | timestamp | When this row was last updated |

---

## Project Structure

```
howLikelyWasThat/
├── scraper/            # Python fbref scraping scripts
│   ├── fbref.py        # Core scraping logic
│   └── run.py          # Entry point (league, season range)
├── db/                 # Database connection and write logic
│   ├── client.py       # Supabase client setup
│   └── upsert.py       # Insert/update player_seasons
├── analysis/           # Statistical analysis
│   ├── distribution.py # Normality tests, fitting, z-scores
│   └── compare.py      # Compare a player-season to a pool
├── api/                # FastAPI backend
│   ├── main.py         # App entry point, routes
│   └── models.py       # Pydantic request/response models
├── frontend/           # Next.js web app
│   ├── app/            # App router pages
│   ├── components/     # Reusable UI components
│   └── lib/            # API client, helpers
├── tests/              # Unit and integration tests
├── .env.example        # Environment variable template
├── requirements.txt    # Python dependencies
└── README.md
```

---

## Data Source

All data scraped from [fbref.com](https://fbref.com). Specifically the per-season league stats pages (standard stats table). Scraping is rate-limited and respectful of the site.

---

## Running Locally

> Setup instructions will be added once the project structure is in place. See `TODO.md` for current build status.

---

## Leagues Supported

- [x] La Liga (last 20 seasons)
- [ ] Serie A (planned)
- [ ] Others (future)
