from enum import Enum
import random
from game_harness.world.backpack import BackpackItem, BackpackItemType, CANNED_FOOD, COMPRESSED_BISCUIT, CHOCOLATE, ELECTROLYTE_DRINK, GLUCOSE_DRINK, WATER
from dataclasses import dataclass

class ExploreEventType(Enum):
    ABANDONED_GROCERY_STORE = "abandoned_grocery_store"
    # WILD_DOG_ATTACK = "wild_dog_attack"
    BROKEN_VENDING_MACHINE = "broken_vending_machine"
    EMPTY_BUILDING = "empty_building"

@dataclass(frozen=True)
class EventType():
    name: ExploreEventType
    weight: int
    description: str
    backpack_item_type: BackpackItemType | None = None

EXPLORE_EVENTS = [
    EventType(
        name=ExploreEventType.ABANDONED_GROCERY_STORE,
        weight=3,
        description="发现废弃杂货店，里面有一些食物",
        backpack_item_type=BackpackItemType.FOOD
    ),
    EventType(
        name=ExploreEventType.BROKEN_VENDING_MACHINE,
        weight=3,
        description="发现破损的自动售货机，里面有一些饮料",
        backpack_item_type=BackpackItemType.DRINK

    ),
    EventType(
        name=ExploreEventType.EMPTY_BUILDING,
        weight=5,
        description="发现空荡荡的建筑，没有任何有用的东西",
    ),
]


def generate_backpack_item(type: BackpackItemType) -> BackpackItem:
    if type == BackpackItemType.FOOD:
        return random.choices([
            CANNED_FOOD,
            COMPRESSED_BISCUIT,
            CHOCOLATE,
        ], weights=[0.2, 0.3, 0.5], k=1)[0]  # Adjust weights as needed
    elif type == BackpackItemType.DRINK:
        return random.choices([
            ELECTROLYTE_DRINK,
            GLUCOSE_DRINK,
            WATER,
        ], weights=[0.2, 0.3, 0.5], k=1)[0]  # Adjust weights as needed
    else:
        raise ValueError(f"Unknown backpack item type: {type}")



def generate_explore_event() -> EventType:

    weights = [e.weight for e in EXPLORE_EVENTS]

    item_event = random.choices(EXPLORE_EVENTS, weights=weights, k=1)[0]
    return item_event
