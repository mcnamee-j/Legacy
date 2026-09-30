from typing import Dict, List
from squad import Squad
from player import Player

class Team:
    def __init__(self, name: str, squad: Squad):
        self.name = name
        self.squad = squad

        # team stats starts empty on game creation
        self.team_stats: Dict[str, int] = {
            "played": 0, "won": 0, "drawn": 0, "lost": 0, "goals_for": 0, "goals_against": 0, "points": 0, "clean_sheets": 0,
        }
        # player stats generated as game progresses - starting development with apps, goals, assists
        self.player_stats: Dict[str, Dict[str, int]] = {
            player.name: {"appearances": 0, "goals": 0, "assists": 0}
            for player in squad.players
        }

    # record match team stats
    def record_match_team_results(self, goals_for: int, goals_against: int, scorers: List[str], assisters: List[str]):
        self.team_stats["played"] += 1
        self.team_stats["goals_for"] += goals_for
        self.team_stats["goals_against"] += goals_against
        if(goals_against == 0):
            self.team_stats["clean_sheets"] += 1

        if goals_for > goals_against:
            self.team_stats["won"] += 1
            self.team_stats["points"] += 3
        elif goals_for == goals_against:
            self.team_stats["drawn"] += 1
            self.team_stats["points"] += 1
        else:
            self.team_stats["lost"] += 1

        for player in self.squad.starting_xi + self.squad.subs:
            self.player_stats.setdefault(player.name, {"appearances": 0, "goals": 0, "assists": 0})
            self.player_stats[player.name]["appearances"] += 1

        for name in scorers:
            self.player_stats.setdefault(name, {"appearances": 0, "goals": 0, "assists": 0})
            self.player_stats[name]["goals"] += 1

        for name in assisters:
            self.player_stats.setdefault(name, {"appearances": 0, "goals": 0, "assists": 0})
            self.player_stats[name]["assists"] += 1

# get top goal scorer for the club
    def top_scorer(self):
        if not self.player_stats:
            return None
        return max(self.player_stats.items(), key=lambda kv: kv[1]["goals"])

# get top assister for the club
    def top_assister(self):
            if not self.player_stats:
                return None
            return max(self.player_stats.items(), key=lambda kv: kv[1]["assists"])