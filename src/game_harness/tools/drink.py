from game_harness.data.backpack import BackpackItemType, GameDrinkType
from game_harness.world.state import GameState


def drink(state: GameState, item_name: GameDrinkType) -> str:
    """
    Allows the player to drink a beverage item from their backpack, reducing thirst.
    """
    item = next((item for item in state.backpack if item.name == item_name), None)

    if item is None:
        return f"{item_name} is not in the backpack."

    if item.type != BackpackItemType.DRINK:
        return f"{item.name} is not a drink item."

    state.thirst = max(0, state.thirst - item.restore)
    state.backpack.remove(item)
    return f"Drank {item.name}. Thirst is now {state.thirst}."
