from typing import List, Optional
from player import Player

#define formations and total subs constants
FORMATIONS = {
    "4-4-2": {"DEF": 4, "MID": 4, "FOR": 2},
    "4-2-3-1": {"DEF": 4, "MID": 5, "FOR": 1},
    "4-3-3": {"DEF": 4, "MID": 3, "FOR": 3},
    "4-1-2-1-2": {"DEF": 4, "MID": 4, "FOR": 2},
    "4-5-1": {"DEF": 4, "MID": 5, "FOR": 1},
    "3-5-2": {"DEF": 3, "MID": 5, "FOR": 2},
    "5-3-2": {"DEF": 5, "MID": 3, "FOR": 2},
}

SUBS = 5

# define exceptions here
class SalaryCapExceeded(Exception):
    pass

class InvalidLineup(Exception):
    pass

class Squad:
    def __init__(self, players: List[Player], salary_cap: int):
        self.players: List[Player] = players
        self.salary_cap = salary_cap
        self.starting_xi: List[Player] = []
        self.subs: List[Player] = []
        self.formation: Optional[str] = None

    #salary cap requires logic here including - total wage, salary cap remaining, a boolean flag if within/above cap
    #also need ability to add and remove players from squad
    @property
    def total_wage(self) -> int:
        total = 0
        for player in self.players:
            total = total + player.wage
        return total

    @property
    def cap_remaining(self) -> int:
        return self.salary_cap - self.total_wage

    def is_within_salary_cap(self) -> bool:
        return self.total_wage <= self.salary_cap

    #add_player e.g. from a pack, requires salary cap check
    def add_player(self, player: Player):
        if player.wage + self.total_wage > self.salary_cap:
            raise SalaryCapExceeded(
                f"By adding {player.name} (£{player.wage}k) you would exceed the current salaries budget"
                f"Current salary budget: £{self.total_wage}k/£{self.salary_cap}k"
            )
        self.players.append(player)

    #remove_player checks if player was in starting xi or subs also
    def remove_player(self, player: Player):
        self.players.remove(player)
        if player in self.starting_xi:
            self.starting_xi.remove(player)
        if player in self.subs:
            self.subs.remove(player)



    # need lineup functionality here - add, remove, select formation
    def set_lineup(self, starting_xi: List[Player], formation: str, subs: List[Player]):
        if formation not in FORMATIONS:
            raise InvalidLineup(
                f"The formation selected is unknown: {self.formation}"
            )
        if len(starting_xi) != 11:
            raise InvalidLineup(
                f"The starting lineup requires exactly 11 players - Currently selected: {len(self.starting_xi)}"
            )
        if len(subs) != SUBS:
            raise InvalidLineup(
                f"A total of 5 subs can be selected - Currently selected: {len(self.subs)}"
            )

        # should enforce a selection of goalkeeper also