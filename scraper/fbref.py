from bs4 import BeautifulSoup
from models import PlayerSeason


def extract_data(row, season: str, league: str) -> PlayerSeason:
    """
    Parse a single <tr> row from the fbref standard stats table into a PlayerSeason.

    Args:
        row: A BeautifulSoup Tag representing one player's <tr> element.
        season: Season string in the format '2011-12'.
        league: League identifier string e.g. 'la_liga'.

    Returns:
        A PlayerSeason dataclass instance with all stats extracted from the row.
    """
    
    player_td = row.find("td", {"data-stat": "player"})
    name = player_td.get("csk")
    fbref_id = player_td.get("data-append-csv")
    team = row.find("td", {"data-stat": "team"}).text.strip()

    minutes = int( row.find("td", {'data-stat': 'minutes'}).text.replace(",", "") or 0)
    apps = int( row.find("td", {'data-stat': 'games'}).text or 0)
    starts = int( row.find("td", {'data-stat': 'games_starts'}).text or 0)
    nineties = float( row.find("td", {'data-stat': 'minutes_90s'}).text or 0)

    goals = int( row.find("td", {'data-stat': 'goals'}).text or 0)
    assists = int( row.find("td", {'data-stat': 'assists'}).text or 0)
    npg = int( row.find("td", {'data-stat': 'goals_pens'}).text or 0)
    goals_assists = int( row.find("td", {'data-stat': 'goals_assists'}).text or 0)
    pens = int( row.find("td", {'data-stat': 'pens_made'}).text or 0)
    pens_attempted = int( row.find("td", {'data-stat': 'pens_att'}).text or 0)
    npga = npg + assists

    goals_p90 = float( row.find("td", {'data-stat': 'goals_per90'}).text or 0)
    assists_p90 = float( row.find("td", {'data-stat': 'assists_per90'}).text or 0)
    goals_assists_p90 = float( row.find("td", {'data-stat': 'goals_assists_per90'}).text or 0)
    npg_p90 = float( row.find("td", {'data-stat': 'goals_pens_per90'}).text or 0)
    npg_assists_p90 = float( row.find("td", {'data-stat': 'goals_assists_pens_per90'}).text or 0)
    
    return PlayerSeason(
        fbref_id=fbref_id,
        player_name=name,
        team=team,
        league=league,
        season=season,
        apps=apps,
        starts=starts,
        minutes=minutes,
        nineties=nineties,
        goals=goals,
        npg=npg,
        assists=assists,
        ga=goals_assists,
        npga=npga,
        pens=pens,
        pens_att=pens_attempted,
        goals_p90=goals_p90,
        npg_p90=npg_p90,
        assists_p90=assists_p90,
        ga_p90=goals_assists_p90,
        npga_p90=npg_assists_p90,
    )



def parse_season(html: str, season: str, league: str) -> list[PlayerSeason]:
    """
    Parse all player rows from a full fbref standard stats page HTML string.

    Args:
        html: Raw HTML string of the fbref league season stats page.
        season: Season string in the format '2011-12'.
        league: League identifier string e.g. 'la_liga'.

    Returns:
        List of PlayerSeason instances, one per player row, excluding header rows.
    """
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", id="stats_standard")
    tbody = table.find("tbody")
    rows = tbody.find_all("tr")
    data = []
    for row in rows:
        if "thead" in row.get("class", []):
            continue
        record = extract_data(row, season=season, league=league)
        data.append(record)
    return data


def main():
    with open("tests/fixtures/la_liga_2025_26.html", "r", encoding="utf-8") as f:
        html = f.read()

    season_data = parse_season(html, '2025-26', 'la_liga')
    print(len(season_data))

if __name__ == "__main__":
    main()