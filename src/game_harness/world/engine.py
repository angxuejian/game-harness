from langchain.tools import tool
from langchain_core.tools import BaseTool

from game_harness.tools.eat import eat
from game_harness.tools.drink import drink
from game_harness.world.backpack import GameFoodType, GameDrinkType
from game_harness.world.rules import end_day
from game_harness.world.state import GameState, GameConfig

def build_tools(state: GameState) -> list[BaseTool]:
      @tool("eat")
      def eat_tool(item_name: GameFoodType) -> bool:
          """Consume one food item from the backpack to reduce hunger."""
          return eat(state, item_name)

      @tool("drink")
      def drink_tool(item_name: GameDrinkType) -> bool:
          """Consume one drink from the backpack to reduce thirst."""
          return drink(state, item_name)

      @tool("end_day")
      def end_day_tool() -> str:
          """End the current day and apply hunger, thirst, and HP changes."""
          end_day(state)
          return str(state)

      return [eat_tool, drink_tool, end_day_tool]



def build_context(state: GameState) -> str:
    """
    Builds the context for the LLM based on the current game state and event.
    """
    backpack = "\n".join(
        f"- name: {item.name.value}, type: {item.type.value}, restore: {item.restore}"
        for item in state.backpack
    )

    return f"""
    Current game state:
    - Day: {state.day}
    - HP: {state.hp}/{GameConfig.max_hp}
    - Stamina: {state.stamina}/{GameConfig.max_stamina}
    - Hunger: {state.hunger}
    - Thirst: {state.thirst}

    Backpack contents:
    {backpack}
    """

def build_system_prompt() -> str:
    return f"""
    You are playing a survival game.
    Your goal is to survive as many days as possible.

    Goal: Survive as many days as possible in the game.

    Available tools:
    - eat(item_name): Eat one food item from your backpack.
    - drink(item_name): Drink one drink item from your backpack.
    - end_day(): End the current day.

    Rules:
    - You must eventually call end_day() to advance the game.
    - Staying on the same day does not increase your survival score.
    - Ending a day increases hunger and thirst.
    - High hunger or thirst causes HP damage.
    - If HP reaches 0, the game is over.
    - Food and drinks are consumed after use.
    """