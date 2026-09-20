# game-harness

一个为LLMs建造的生存游戏。参考《60 Seconds》游戏玩法。

## 规则

1. 不存在完美生存结局，只有活下去，越久越好
2. 玩家（LLM）
3. 生命值：100，体力值：100
4. 每天会根据饥饿，口渴来扣除生命值；
5. 执行行动会消耗体力值；玩家可以探索以获取资源，并自行决定何时结束当天。
   <!-- 7. 玩家背包限制10个格子（5个格子放选择的物品，5个格子放食物和水） -->
   <!-- 3. 游戏开始会从10件物品中，挑选5件携带 -->

<!-- main.py：CLI 入口，接收用户输入，然后调用 harness
harness.py：核心调度，决定怎么组织 context、调用 tool、返回结果
context.py：构造给 LLM 的上下文
tools.py：游戏世界允许调用的工具，比如 get_location()、inspect_npc()
runtime.py：真正执行工具的地方
permissions.py：限制什么操作允许做
guardrails.py：输入/输出规则、边界检查
state.py：保存当前玩家位置、历史动作、trace 等状态 -->

## 启动

1. 复制环境变量配置文件：

    ```bash
    cp .env.example .env
    ```

2. 编辑 `.env`，填写 `API Key` 和 `Base URL`。
3. 安装项目依赖：

    ```bash
    uv sync
    ```

4. 启动游戏：

    ```bash
    uv run game-harness
    ```

## 闲谈

当我完全意识到`harness`的设计，我非常惊叹和佩服！完全就是天才！

从广义的角度来看，我们何尝不是生活在一个被`harness`设计好的世界，开车要遵守交通的`harness`，生活要遵守当地的法律的`harness`，玩游戏要遵守游戏厂商的`harness`。

所以当我意识到`game-harness`是给 LLMs 玩的，突然联想到动漫中的游戏，比如刀剑神域、罗小黑的众生之门。当玩家是人时，要有好的操作体验，尽管画面在精致，目前也无法做到`Link Start`。但是对于 LLMs 来说画面本身也不是很重要，token即可。然后将一系列决策、打斗日志通过UI罗列出来 + 多个 LLMs 的合作通关至100层、妖王佛岚的赞赏。这何尝不是另一种 show
