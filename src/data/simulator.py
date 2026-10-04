import random
import math

BASE_XG = 1.2
HOME_ADVANTAGE = 0.2
XG_FACTOR = 22
XG_FLOOR = 0.05
XG_CAP = 3.5
ASSIST_CHANCE = 0.77

POSITION_GOAL_WEIGHT = {"FOR": 1.0, "MID": 0.45, "DEF": 0.2, "GK": 0.01}
POSITION_ASSIST_WEIGHT = {"FOR": 0.8, "MID": 0.8, "DEF": 0.4, "GK": 0.07}

# knuth poisson algorithm to assign goals from the calculated xG values (lam)
def convert_xg_to_goals(lam):
    L = math.exp(-lam)
    k = 0
    p = 1
    while True:
        k += 1
        p *= random.random()
        if p <= L:
            return k - 1

def simulate_match(home_team_ovr, away_team_ovr):
    # can manipulate the base xG based on team overall and home advantage
    diff_ovr = home_team_ovr - away_team_ovr

    # calculate xG of each team
    home_team_xg = (BASE_XG * math.exp(diff_ovr/XG_FACTOR)) + HOME_ADVANTAGE
    away_team_xg = (BASE_XG * math.exp(-diff_ovr/XG_FACTOR))

    # ensures xG values do not go lower than xg_floor value - the max() method returns the higher value of the two, min() takes the smallest
    home_team_xg = min(XG_CAP, max(XG_FLOOR, home_team_xg))
    away_team_xg = min(XG_CAP, max(XG_FLOOR, away_team_xg))

    home_goals = convert_xg_to_goals(home_team_xg)
    away_goals = convert_xg_to_goals(away_team_xg)

    return home_goals, home_team_xg, away_goals, away_team_xg

# for _ in range(10):
#     home, home_xg, away, away_xg = simulate_match(70, 65)
#     print(f"Home {home} - {away} Away  (xG: {home_xg:.2f} - {away_xg:.2f})")

def generate_goal_events(starting_xi, goals_scored):
    if goals_scored == 0:
        return []

    goal_events = []
    
    goal_scorers = random.choices(starting_xi, weights = [(player.attack ** 2) * POSITION_GOAL_WEIGHT[player.position] for player in starting_xi], k = goals_scored)

    # for assists, need to remove goal scorers and also consider that not all goals have assists   
    for scorer in goal_scorers:
        assister_name = None

        # random.choices returns a list therefore to pull out a single assister, as below, you add the [0] index at the end
        if random.random() < ASSIST_CHANCE:
            possible_assisters = [player for player in starting_xi if player != scorer]
            assister = random.choices(possible_assisters, weights = [(player.ability ** 2) * POSITION_ASSIST_WEIGHT[player.position] for player in possible_assisters], k = 1)[0]
            assister_name = assister.name
        goal_events.append({"scorer": scorer.name, "assister": assister_name})

    return goal_events