from game_harness.world.events import generate_backpack_item, generate_explore_event
from game_harness.world.rules import add_backpack_item, perform_action
from game_harness.world.state import GameAction, GameState


def explore(state: GameState) -> str:
    """
    Spend stamina to explore and add any discovered item to the backpack.

    Return the event description and item details, or explain why exploration failed.
    """
    if not perform_action(state=state, action=GameAction.EXPLORE):
        return "The player has died and cannot explore." if not state.alive else "Insufficient stamina and cannot explore."

    event = generate_explore_event()

    if event.backpack_item_type is None:
        return event.description

    item = generate_backpack_item(event.backpack_item_type)
    add_backpack_item(state=state, backpack_item=item)
    return f"{event.description}, get: {item.name.value}, restore: {item.restore}"
