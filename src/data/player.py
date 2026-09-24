from dataclasses import dataclass

@dataclass
class Player:
        name: str
        overall: int
        position: str
        position_d: str
        attack: int
        defense: int
        ability: int
        physicality: int
        tier: str
        wage: int
        era: str

        def __post_init__(self): #runs directly after constructor finishes
                if not (0 <= self.overall <= 99):
                        raise ValueError(f"{self.name} must have a rating between 0-99, currently {self.overall}")
                if self.wage < 0:
                        raise ValueError(f"{self.name} cannot have a negative wage")
        def __repr__(self):
                return f"Player: {self.name} [{self.position}] - {self.position_d}) OVR {self.overall} - {self.tier}"

        @classmethod
        def from_row(cls, row: dict) -> "Player":
                return cls(
                        name = f"{row.get('firstname', '')} {row.get('surname', '')}".strip(),
                        position = row["position"],
                        position_d = row.get("position_detailed", row["position"]),
                        overall = int(row["overall"]),
                        attack = int(row["attack"]),
                        defense = int(row["defense"]),
                        ability = int(row["ability"]),
                        physicality = int(row["physicality"]),
                        tier = row["tier"],
                        wage = int(row["wage"]),
                        era = row.get("era", "current")
                )