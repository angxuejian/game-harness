# game-harness
A simple agent harness for exploring and reasoning about an RPG game world.


<!-- main.py：CLI 入口，接收用户输入，然后调用 harness
harness.py：核心调度，决定怎么组织 context、调用 tool、返回结果
context.py：构造给 LLM 的上下文
tools.py：游戏世界允许调用的工具，比如 get_location()、inspect_npc()
runtime.py：真正执行工具的地方
permissions.py：限制什么操作允许做
guardrails.py：输入/输出规则、边界检查
state.py：保存当前玩家位置、历史动作、trace 等状态 -->