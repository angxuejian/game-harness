from game_harness.data.backpack import BackpackItemType, GameFoodType
from game_harness.world.state import GameState


def eat(state: GameState, item_name: GameFoodType) -> str:
    """
    Allows the player to eat a food item from their backpack, reducing hunger.
    """

    item = next((item for item in state.backpack if item.name == item_name), None)

    if item is None:
        return f"{item_name} is not in the backpack."

    if item.type != BackpackItemType.FOOD:
        return f"{item.name} is not a food item."

    state.hunger = max(0, state.hunger - item.restore)
    state.backpack.remove(item)
    return f"Ate {item.name}. Hunger is now {state.hunger}."
