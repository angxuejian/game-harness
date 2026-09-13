from dataclasses import dataclass
from enum import Enum

class BackpackItemType(str, Enum):
    """
    Represents the types of items that can be stored in the player's backpack.
    """
    FOOD = "food"
    DRINK = "drink"

class GameFoodType(str, Enum):
    """
    Represents the types of food items that can be consumed by the player.
    """
    CANNED_FOOD = "canned_food"
    COMPRESSED_BISCUIT = "compressed_biscuit"
    CHOCOLATE = "chocolate"

class GameDrinkType(str, Enum):
    """
    Represents the types of drink items that can be consumed by the player.
    """
    ELECTROLYTE_DRINK = "electrolyte_drink"
    GLUCOSE_DRINK = "glucose_drink"
    WATER = "water"

@dataclass(frozen=True)
class BackpackItem:
    name: GameFoodType | GameDrinkType
    type: BackpackItemType
    restore: int



# food
CANNED_FOOD = BackpackItem(
    name=GameFoodType.CANNED_FOOD,
    type=BackpackItemType.FOOD,
    restore=30,
)

COMPRESSED_BISCUIT = BackpackItem(
    name=GameFoodType.COMPRESSED_BISCUIT,
    type=BackpackItemType.FOOD,
    restore=20,
)
    
CHOCOLATE = BackpackItem(
    name=GameFoodType.CHOCOLATE,
    type=BackpackItemType.FOOD,
    restore=10,
)


# water
ELECTROLYTE_DRINK = BackpackItem(
    name=GameDrinkType.ELECTROLYTE_DRINK,
    type=BackpackItemType.DRINK,
    restore=30,
)

GLUCOSE_DRINK = BackpackItem(
    name=GameDrinkType.GLUCOSE_DRINK,
    type=BackpackItemType.DRINK,
    restore=20,
)

WATER = BackpackItem(
    name=GameDrinkType.WATER,
    type=BackpackItemType.DRINK,
    restore=10,
)