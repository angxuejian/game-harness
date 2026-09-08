

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