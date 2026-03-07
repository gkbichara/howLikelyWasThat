from scraper.fbref import parse_season
from db.upsert import upsert_seasons

def main():
    """
    Orchestrates the full scrape-and-store pipeline.
    Reads HTML, parses player season data, and upserts to Supabase.
    """
    with open("tests/fixtures/la_liga_2025_26.html", "r", encoding="utf-8") as f:
        html = f.read()

    season_data = parse_season(html, '2025-26', 'la_liga')
    upsert_seasons(season_data)

if __name__ == "__main__":
    main()