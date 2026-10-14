import sys
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
sys.path.append(str(DATA_DIR))

from opponents import load_opponents
from simulator import play_match

teams = load_opponents(DATA_DIR / "opponents.xlsx")
by_name = {team.name: team for team in teams}

result = play_match(by_name["Arsenal"], by_name["Hull"])
print(result["home"], result["home_goals"], "-", result["away_goals"], result["away"])
print(result["home_events"])