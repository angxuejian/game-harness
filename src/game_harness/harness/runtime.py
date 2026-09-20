from game_harness.harness.context import build_context
from game_harness.world.state import GameState
from game_harness.harness.context import build_tools, build_context, build_system_prompt
from game_harness.player.llm import create_player
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage, BaseMessage
from game_harness.trace.color import GREEN, BLUE, RESET, PURPLE
from pydantic import ValidationError


def run_game() -> GameState:
    """Runs the game loop until the game is over."""

    state = GameState()
    tools = build_tools(state)
    player = create_player().bind_tools(tools, parallel_tool_calls=False)
    tool_map = {tool.name: tool for tool in tools}

    system_message = SystemMessage(content=build_system_prompt())
    last_action: list[BaseMessage] = []
    last_day = 0
    consecutive_no_tool_calls = 0

    while state.alive:
        if state.day != last_day:
            last_day = state.day
            if state.day > 1:
                print("\n")
            print(state)

        messages = [
            system_message,
            *last_action,
            HumanMessage(content=build_context(state)),
        ]

        try:
            response = player.invoke(messages)
        except Exception as e:
            print(f"Game Over! The player request failed. Error: {e}")
            break

        if not response.tool_calls:
            consecutive_no_tool_calls += 1
            print("The model returned no tool calls. Retrying...")

            if consecutive_no_tool_calls >= 5:
                print(
                    "Game Over! The player failed to call a tool 5 consecutive times."
                )
            continue

        consecutive_no_tool_calls = 0
        last_action = [response]
        execution_failed = False

        for call in response.tool_calls:
            tool = tool_map[call["name"]]

            if not tool:
                result = ToolMessage(
                    content=f"Tool is not: {call['name']}, can use tool list: {','.join(tool_map)}",
                    tool_call_id=call["id"],
                )
            else:
                try:
                    result = tool.invoke(call)
                    print(
                        f"Tool {call['name']} returned: {PURPLE}stamina={state.stamina}{RESET} {GREEN}hunger={state.hunger}{RESET}, {BLUE}thirst={state.thirst}{RESET}"
                    )
                except ValidationError as v:
                    result = ToolMessage(
                        content=f"Parameter validation failed. {v}. please retry",
                        tool_call_id=call["id"],
                    )
                except Exception as e:
                    print(f"Tool {call['name']} run failed: {e}")
                    execution_failed = True
                    break

            last_action.append(result)
            if not state.alive:
                break

        if execution_failed:
            break

    print("\nGame Over! survived for", state.day, "days.")

    return state

