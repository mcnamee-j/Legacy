import random
import pandas as pd
from player import Player
from squad import Squad
from team import Team

# want to change the overalls of opposition players every year to achieve some sort of realism during simulation of different seasons

STAT_OFFSETS = {
    "GK": {"attack": -50, "defense": 5, "ability": -35, "physicality": 3},
    "DEF": {"attack": -40, "defense": 5, "ability": -15, "physicality": 3},
    "MID": {"attack": -10, "defense": -5, "ability": -3, "physicality": 0},
    "FOR": {"attack": -4, "defense": -50, "ability": 5, "physicality": 0},
} 

SPREAD = 5
RANGE_WIDTH = 3

# guard rail to avoid negative or >100 values
def guard_rail(value, low=1, high=99):
    return max(low, min(high, value))

def build_ai_player(name, position, team_overall):
    offsets = STAT_OFFSETS[position]

    stats = {}
    for stat, offset in offsets.items():
        stats[stat] = guard_rail(team_overall + offset + random.randint(-SPREAD, SPREAD))

    overall = guard_rail(team_overall + random.randint(-SPREAD, SPREAD))
    return Player(
        name=name, position= position, position_d= position,
        overall=overall,
        attack=stats["attack"], defense=stats["defense"], physicality=stats["physicality"], ability=stats["ability"],
        tier="CORE", wage=0, era="current",
        rating_min=guard_rail(overall - RANGE_WIDTH),
        rating_max=guard_rail(overall + RANGE_WIDTH),
    )

def load_opponents(path):
    teams_dir = pd.read_excel(path, sheet_name="teams")
    players_dir = pd.read_excel(path, sheet_name="players")

    teams = []

    # iterrows() iterates over each row, giving a pair: row number and the row itself - _ skips row number
    for _, team_row in teams_dir.iterrows():
        team_name = team_row["Team"]
        team_overall = team_row["Overall"]
                    # filters player sheet, keeping only rows for the current team
        squad_rows = players_dir[players_dir["team"] == team_name]

        players = []
        for _, player in squad_rows.iterrows():
            players.append(build_ai_player(player["name"], player["position"], team_overall))

        squad = Squad(players=players, salary_cap=10_000_000)
        squad.starting_xi = players
        teams.append(Team(team_name, squad))

    return teams

for team in load_opponents("opponents.xlsx"):
    print(f"{team.name:20} {team.squad.team_overall():5.1f}")