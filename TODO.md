# TODO — howLikelyWasThat

Building toward a single final vision: a public web app where anyone can look up any footballer's attacking season, compare it to a custom pool, and see how statistically likely it was.

No versions. Each task is a step toward that end state.

---

## Phase 1 — Project Setup

- [x] Create project folder structure (`scraper/`, `db/`, `analysis/`, `api/`, `frontend/`, `tests/`)
- [x] Set up Python virtual environment and `requirements.txt`
- [ ] Create `.env.example` with required variables (`SUPABASE_URL`, `SUPABASE_KEY`)
- [ ] Add `.env` to `.gitignore`
- [ ] Install core Python dependencies: `requests`, `beautifulsoup4`, `supabase`, `python-dotenv`, `fastapi`, `uvicorn`, `scipy`, `numpy`, `pandas`, `pytest`

---

## Phase 2 — Scraping

- [ ] Manually inspect the fbref La Liga standard stats page — understand the HTML table structure, column names, and player IDs
- [ ] Write a function that fetches and parses one season's La Liga standard stats table
- [ ] Map fbref column names to the `player_seasons` schema (`goals`, `npg`, `assists`, `ga`, `minutes`, etc.)
- [ ] Test the single-season scraper against a known season and verify row counts and values manually
- [ ] Expand to loop over the last 20 La Liga seasons — handle rate limiting with delays
- [ ] Save a few HTML fixtures locally for use in scraper unit tests
- [ ] Write scraper tests using saved HTML fixtures (no live network calls in tests)

---

## Phase 3 — Database

- [ ] Create the `player_seasons` table in Supabase with the agreed schema (see README)
- [ ] Add a unique constraint on `(fbref_id, season, league)` to support safe upserts
- [ ] Write a Supabase client setup module (`db/client.py`) that reads credentials from `.env`
- [ ] Write an upsert function (`db/upsert.py`) that takes a list of player season records and writes them to Supabase
- [ ] Run the La Liga scraper end-to-end and load all 20 seasons into Supabase
- [ ] Verify the data: row count per season, spot-check known values (e.g. Messi 2011/12 = 50 goals)
- [ ] Write a DB integration test that inserts a test row, reads it back, and cleans up

---

## Phase 4 — Statistical Analysis

- [ ] Load a full season from Supabase into a pandas DataFrame — explore the distribution visually (histogram, summary stats)
- [ ] Run a normality test (Shapiro-Wilk) on goals, npg, assists, and G+A for a sample season
- [ ] Decide on approach based on EDA results: z-score if normal, or alternative (e.g. percentile rank, fit a skewed distribution)
- [ ] Write `analysis/distribution.py`:
  - Given an array of values and a target value, return: mean, std, z-score, p-value (one-tailed), percentile rank, and distribution type used
- [ ] Write `analysis/compare.py`:
  - Given a player-season and a pool definition (league, season range, min goals, metric), query the pool from DB and run the distribution analysis
- [ ] Test with Messi 2011/12 vs all La Liga seasons — verify the output makes intuitive sense
- [ ] Write unit tests for distribution functions using synthetic data with known properties

---

## Phase 5 — FastAPI Backend

- [ ] Set up FastAPI project structure in `api/`
- [ ] Create a player search endpoint: `GET /players?q=messi` — returns matching player names and fbref IDs
- [ ] Create a player season endpoint: `GET /players/{fbref_id}/seasons` — returns all seasons for a player
- [ ] Create the core analysis endpoint: `POST /compare` — accepts player-season + pool definition, returns distribution stats + histogram data (array of bucket counts + player's value)
- [ ] Define Pydantic request and response models in `api/models.py`
- [ ] Add input validation: league must be valid, season format must be correct, min_goals must be non-negative
- [ ] Confirm the API works end-to-end: hit `/compare` for Messi 2011/12 with default pool and verify response
- [ ] Write API tests using FastAPI's `TestClient`

---

## Phase 6 — Next.js Frontend

- [ ] Scaffold a new Next.js project in `frontend/` with TypeScript and Tailwind CSS
- [ ] Understand the App Router structure — pages, layouts, server vs client components
- [ ] Create a typed API client in `frontend/lib/api.ts` that wraps all FastAPI calls
- [ ] Build the player search bar component — calls `/players?q=` on input, shows dropdown of results
- [ ] Build the season selector — once a player is selected, fetch and show their available seasons
- [ ] Build the metric selector — radio/checkbox group for: goals, npg, assists, G+A, per 90 variants
- [ ] Build the comparison pool controls — league selector, season range pickers, min goals input (with sensible defaults)
- [ ] Build the results section:
  - Histogram chart (distribution of the pool) with the selected player's value marked
  - Summary stats: mean, std, z-score, percentile, probability statement
- [ ] Wire everything together into a single page flow: search → configure → see result
- [ ] Handle loading states and errors visibly throughout

---

## Phase 7 — Deployment

- [ ] Deploy FastAPI to Railway — set environment variables, confirm public URL works
- [ ] Deploy Next.js to Vercel — connect to GitHub, set `NEXT_PUBLIC_API_URL` to Railway URL
- [ ] Test the full end-to-end flow on the live URLs
- [ ] Add the live URL to `README.md`

---

## Phase 8 — Serie A + Incremental Updates

- [ ] Verify fbref Serie A pages have the same structure as La Liga — adjust scraper if needed
- [ ] Run the scraper for Serie A (last 20 seasons) and load into Supabase
- [ ] Switch the scraper to upsert mode with a `scraped_at` timestamp — enables re-running without duplication
- [ ] Set up a mechanism to re-run the current season's scrape periodically (e.g. a script you can run manually, or a scheduled job)

---

## Ongoing

- [ ] Keep `requirements.txt` up to date as dependencies are added
- [ ] All new functions get a corresponding test
- [ ] Verify Messi 2011/12 numbers remain correct after any schema or logic change (use as a known-good integration test)
