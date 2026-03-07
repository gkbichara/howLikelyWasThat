from db.client import supabase
from models import PlayerSeason
from dataclasses import asdict

def upsert_seasons(records: list[PlayerSeason]) -> None:
    data = [asdict(r) for r in records]
    supabase.table("player_seasons").upsert(data, on_conflict="fbref_id,season,league,team").execute()
    print(f"Upserted {len(records)} records")