
from game_harness.world.backpack import BackpackItemType, GameDrinkType
from game_harness.world.state import GameState


def drink(state: GameState, item_name: GameDrinkType) -> bool:
    """
    Allows the player to drink a beverage item from their backpack, reducing thirst.
    """
    item = next((item for item in state.backpack if item.name == item_name), None)

    if item is None:
        # print(f"{item_name} is not in the backpack.")
        return False

    if item.type != BackpackItemType.DRINK:
        # print(f"{item.name} is not a drink item.")
        return False

    state.thirst = max(0, state.thirst - item.restore)
    state.backpack.remove(item)
    # print(f"Drank {item.name}. Thirst is now {state.thirst}.")
    return True