import sys
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
sys.path.append(str(DATA_DIR))

from opponents import load_opponents
from simulator import play_match

teams = load_opponents(DATA_DIR / "opponents.xlsx")
by_name = {team.name: team for team in teams}

from united import build_united

united, pool = build_united(DATA_DIR / "United.xlsx")
print(united.squad.starting_xi)
print("Team overall:", round(united.squad.team_overall(), 1))
print("Wage bill:", united.squad.total_wage, "of", united.squad.salary_cap)