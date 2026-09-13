
from game_harness.world.backpack import BackpackItemType, GameFoodType
from game_harness.world.state import GameState


def eat(state: GameState, item_name: GameFoodType) -> bool:
    """
    Allows the player to eat a food item from their backpack, reducing hunger.
    """

    item = next((item for item in state.backpack if item.name == item_name), None)

    if item is None:
        # print(f"{item_name} is not in the backpack.")
        return False

    if item.type != BackpackItemType.FOOD:
        # print(f"{item.name} is not a food item.")
        return False

    state.hunger = max(0, state.hunger - item.restore)
    state.backpack.remove(item)
    # print(f"Ate {item.name}. Hunger is now {state.hunger}.")
    return True