from enum import Enum
from game_harness.data.backpack import BackpackItemType
from dataclasses import dataclass


class ExploreEventType(Enum):
    ABANDONED_GROCERY_STORE = "abandoned_grocery_store"
    # WILD_DOG_ATTACK = "wild_dog_attack"
    BROKEN_VENDING_MACHINE = "broken_vending_machine"
    EMPTY_BUILDING = "empty_building"


@dataclass(frozen=True)
class EventType:
    name: ExploreEventType
    weight: int
    description: str
    backpack_item_type: BackpackItemType | None = None


EXPLORE_EVENTS = [
    EventType(
        name=ExploreEventType.ABANDONED_GROCERY_STORE,
        weight=3,
        description="发现废弃杂货店，里面有一些食物",
        backpack_item_type=BackpackItemType.FOOD,
    ),
    EventType(
        name=ExploreEventType.BROKEN_VENDING_MACHINE,
        weight=3,
        description="发现破损的自动售货机，里面有一些饮料",
        backpack_item_type=BackpackItemType.DRINK,
    ),
    EventType(
        name=ExploreEventType.EMPTY_BUILDING,
        weight=5,
        description="发现空荡荡的建筑，没有任何有用的东西",
    ),
]
