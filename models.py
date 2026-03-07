from dataclasses import dataclass

@dataclass
class PlayerSeason:
    fbref_id: str
    player_name: str
    team: str
    league: str
    season: str
    apps: int
    starts: int
    minutes: int
    nineties: float
    goals: int
    npg: int
    assists: int
    ga: int
    npga: int
    pens: int
    pens_att: int
    goals_p90: float
    npg_p90: float
    assists_p90: float
    ga_p90: float
    npga_p90: float