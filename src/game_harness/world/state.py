
from dataclasses import dataclass, field
from enum import Enum
from game_harness.world.backpack import CANNED_FOOD, ELECTROLYTE_DRINK, COMPRESSED_BISCUIT, WATER,CHOCOLATE,GLUCOSE_DRINK, BackpackItem

@dataclass
class GameState:
    """
    Represents the state of the game world.
    """
    hp: int = 100
    stamina: int = 100

    hunger: int = 0
    thirst: int = 0

    day: int = 1
    alive: bool = True

    backpack: list[BackpackItem] = field(default_factory=lambda: [
        CANNED_FOOD,
        ELECTROLYTE_DRINK,
        COMPRESSED_BISCUIT,
        WATER,
        CHOCOLATE,
        GLUCOSE_DRINK,
        CANNED_FOOD,
        ELECTROLYTE_DRINK
    ])

    def __str__(self) -> str:
        names = [item.name.value for item in self.backpack]
        return (
            f"GameState(day={self.day}, hp={self.hp}, stamina={self.stamina}, "
            f"hunger={self.hunger}, thirst={self.thirst}, "
            f"alive={self.alive}, backpack={names})"
        )

    def __post_init__(self):
        print(self)

@dataclass
class GameConfig:
    """
    Represents the configuration of the game world.
    """
    max_hp: int = 100
    max_stamina: int = 100


class GameAction(str, Enum):
    """
    Represents the possible actions a player can take in the game.
    """
    EXPLORE = "explore"
    REST = "rest"
    DRINK = "drink"
    EAT = "eat"
    USE = "use"
