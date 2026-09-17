
from game_harness.world.engine import build_context
from game_harness.world.state import GameState
from game_harness.world.engine import build_tools, build_context, build_system_prompt
from game_harness.player.llm import create_player
from langchain_core.messages import SystemMessage, HumanMessage
from game_harness.trace.color import GREEN, BLUE, RESET, PURPLE

def run_game() -> GameState:
    """Runs the game loop until the game is over."""
    
    state = GameState()
    tools = build_tools(state)
    player = create_player().bind_tools(tools, parallel_tool_calls=False)
    tool_map = {tool.name: tool for tool in tools}

    system_message = SystemMessage(content=build_system_prompt())
    last_action = []
    last_day = 0

    while state.alive:
        if state.day != last_day:
            last_day = state.day
            if state.day > 1:
                print('\n')
            print(state)
        
        
        messages = [
            system_message,
            *last_action,
            HumanMessage(content=build_context(state))
        ]
        response = player.invoke(messages)

        if not response.tool_calls:
            print("The model returned no tool calls. Retrying...")
            continue            

        last_action = [response]
        for call in response.tool_calls:
            result = tool_map[call["name"]].invoke(call)
            last_action.append(result)
            print(f"Tool {call['name']} returned: {PURPLE}stamina={state.stamina}{RESET} {GREEN}hunger={state.hunger}{RESET}, {BLUE}thirst={state.thirst}{RESET}")

    print("\nGame Over! survived for", state.day, "days.")


# while state.alive:
#     engine.start_day(state)

#     event = engine.generate_event(state)
#     engine.resolve_event(state, event)

#     if not state.alive:
#         break

#     while state.actions_remaining > 0 and state.alive:
#         context = build_context(state, event)
#         action = llm.decide(context)
#         execute_tool(action, state)

#     if state.alive:
#         engine.end_day(state)

# engine.game_over(state)