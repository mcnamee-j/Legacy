import random
import pandas as pd
from player import Player
from squad import Squad, FORMATIONS, SUBS
from team import Team

SALARY_CAP = 220 #220 000 - in 100-thousands
STARTING_FORMATION = "4-4-2"

SQUAD_PLAN = {"GK": 2, "DEF": 5, "MID": 6, "FOR": 3}
STARTER_POOL_SIZE = {"GK": 3, "DEF": 6, "MID": 8, "FOR": 4}

def load_united_players(path):
    dir = pd.read_excel(path)

    dir["firstname"] = dir["firstname"].fillna("").str.strip()
    dir["surname"] = dir["surname"].fillna("").str.strip()

    players = []
    for row in dir.to_dict("records"):
        players.append(Player.from_row(row))
    return players

def build_starting_squad(players):
    chosen = []
    for position, how_many in SQUAD_PLAN.items():
        in_position = [player for player in players if player.position == position]
        weakest = sorted(in_position, key=lambda p: p.overall)[:STARTER_POOL_SIZE[position]]
        chosen += random.sample(weakest, how_many)
    return chosen

def pick_lineup(squad_list, formation):
    # using dict()..below creates copy of formation, therefore adding a GK doesnt affect 
    # formation definitions
    required = dict(FORMATIONS[formation])
    required["GK"] = 1

    starting_xi = []

    for position, how_many in required.items():
        in_position= [player for player in squad_list if player.position == position]
        # reverse puts higher overall first in sort
        highest_ovr_first = sorted(in_position, key=lambda player: player.overall, reverse=True)
        starting_xi += highest_ovr_first[:how_many]

    # now rank remainder by overall
    leftover = [player for player in squad_list if player not in starting_xi]
    leftover.sort(key=lambda player: player.overall, reverse=True)

    # one backup goalkeeper, then the best outfield players for the other places
    backup_keeper = [player for player in leftover if player.position == "GK"][0]
    outfield = [player for player in leftover if player.position != "GK"]
    subs = [backup_keeper] + outfield[:SUBS - 1]

    return starting_xi, subs

def build_united(path):
    all_players = load_united_players(path)
    chosen = build_starting_squad(all_players)

    squad = Squad(players=chosen, salary_cap=SALARY_CAP)
    starting_xi, subs = pick_lineup(chosen, STARTING_FORMATION)
    squad.set_lineup(starting_xi, STARTING_FORMATION, subs)

    # returns the team and the entire list of players from Excel
    return Team("Manchester United", squad), all_players