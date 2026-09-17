from game_harness.world.events import generate_backpack_item, generate_explore_event
from game_harness.world.rules import add_backpack_item, perform_action
from game_harness.world.state import GameAction, GameState


def explore(state: GameState) -> str:
    """
    Spend stamina to explore and add any discovered item to the backpack.

    Return the event description and item details, or explain why exploration failed.
    """
    if not perform_action(state=state, action=GameAction.EXPLORE):
        return "角色已死亡，无法探索。" if not state.alive else "体力不足，无法探索。"

    event = generate_explore_event()

    if event.backpack_item_type is None:
        return event.description

    item = generate_backpack_item(event.backpack_item_type)
    add_backpack_item(state=state, backpack_item=item)
    return f"{event.description}，获得：{item.name.value}，恢复：{item.restore}"
