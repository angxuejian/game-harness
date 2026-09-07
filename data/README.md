# 游戏示例数据

所有 JSON 顶层均为数组，UTF-8 编码。ID 全局唯一、名称用于展示；关联查询使用 ID，不依赖中文名称。等级范围包含 0 和 10。这是虚构的规则数据，不代表真实游戏。

| 文件 | 内容 |
| --- | --- |
| `classes.json` | 5 个职业、专属武器类型、五行契合度、技能 ID |
| `weapon_types.json` | 太刀/剑士、魔杖/法师、刺刀/刺客、长弓/游侠、战锤/守卫 |
| `elements.json` | 金木水火土及相克关系 |
| `items.json` | 55 件武器，每个职业每级一件，包含装备等级和掉落来源 |
| `skills.json` | 55 个技能，每个职业 0～10 级每级解锁一个 |
| `monsters.json` | 22 个普通怪物、11 个地图领主，包含属性倍率和掉落概率 |
| `maps.json` | 11 张地图、等级门槛、连接地图、怪物及可掉落装备 |
| `query_examples.json` | 8 个问题及预期查询结果，供检索测试 |

## 规则

- `required_level` 是最低等级；地图的推荐范围用于练级建议，不是进入上限。地图相邻双向连接，初心草原为起点。
- 武器必须满足职业、武器类型和等级要求。五种武器各自都有五行属性版本；并非每一级都有每种属性。火焰剑是 4 级火属性太刀，别名火焰太刀。
- 职业契合度是伤害倍率，越高越契合，并非装备限制。默认推荐契合度最高的属性；对具体敌人时综合武器攻击和怪物弱点。
- 通用规则为金克木、木克土、土克水、水克火、火克金：克制造成 1.5 倍伤害，反向克制造成 0.75 倍，其余 1 倍。
- 怪物的 `incoming_element_multipliers` 已包含通用规则和特殊弱点，是最终属性倍率，不再叠加通用相克。冰霜巨龙的冰甲特殊弱火，火伤 1.75 倍、土伤 1.5 倍。
- 简单武器推荐分数：`attack × 职业属性契合度 × 怪物受到的属性倍率`，先过滤职业和等级。该分数用于推荐，不是完整战斗伤害公式；可再按来源地图等级筛选玩家能获取的装备。
- 每次击杀，对 `drops` 中每一项独立判定一次；`probability` 为 0～1 概率，因此可无掉落或同时掉落多件，概率之和不必等于 1。
- 怪物 `drops` 是掉落事实来源；装备 `source_monster_ids`、`source_map_ids` 和地图 `drop_item_ids` 为反向索引，修改掉落时需同步维护。
- 技能按等级逐级学习，`prerequisite_skill_ids` 表示前置技能。技能属性独立于武器属性；伤害效果先按 `attack × attack_multiplier + flat_damage` 计算基础值，再使用技能属性对应的职业和怪物倍率。`target_count` 是最大目标数。技能示例采用逐阶强化设计。

## ID 查询路径

- 装备哪里获得：`items.id → source_monster_ids → monsters.id → map_id → maps.id`。
- 怪物在哪：`monsters.id → map_id → maps.id`。
- 打怪推荐装备：查怪物属性倍率，按 `items.class_id`、`required_level` 过滤武器，再结合职业契合度计算推荐分数。
- 地图爆什么装备：`maps.id → drop_item_ids → items.id`；具体掉率查看该图怪物的 `drops`。
- 某属性武器：用 `items.element_id` 筛选；职业技能用 `classes.skill_ids` 查询。
- 输入中文名称时，先将 `name` 或 `aliases` 解析为 ID，再执行关联查询。

运行 `python3 scripts/validate_data.py` 可检查 ID 引用、双向索引、等级覆盖和示例查询。
