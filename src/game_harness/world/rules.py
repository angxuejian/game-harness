from game_harness.world.state import GameState, GameAction

ACTION_STAMINA_COST = {
    GameAction.EXPLORE: 30,
    GameAction.REST: 10,
}


def check_alive(state: GameState) -> None:
    """
    Checks if the player is alive based on their HP.
    """
    if state.hp <= 0:
        state.alive = False


def consume_stamina(state: GameState, cost: int) -> bool:
    """
    Consumes stamina from the player if they have enough.
    """
    if cost <= 0:
        return False
    
    if state.stamina < cost:
        return False

    state.stamina -= cost
    return True

def can_perform_action(state: GameState, action: GameAction) -> bool:
    """
    Checks if the player can perform the given action based on their stamina.
    """
    if not state.alive:
        return False

    cost = ACTION_STAMINA_COST.get(action, 0)
    if state.stamina < cost:
        return False

    return True

def perform_action(state: GameState, action: GameAction) -> bool:
    """
    Performs the given action if the player can perform it.
    """

    if not can_perform_action(state, action):
        return False

    cost = ACTION_STAMINA_COST.get(action, 0)

    if not consume_stamina(state, cost):
        return False

    return True

def settle_day(state: GameState) -> None:

    state.hunger += 20
    state.thirst += 30
    apply_survival_damage(state)
    check_alive(state)

def apply_survival_damage(state: GameState) -> None:
    if state.hunger >= 100:
        state.hp -= 20

    if state.thirst >= 100:
        state.hp -= 30

def end_day(state: GameState) -> None:
    """
    Ends the current day or the game if the player is dead.
    """
    settle_day(state)
    if not state.alive:
        return
    state.day += 1