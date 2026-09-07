"""校验游戏数据的关联完整性及代表性查询，无第三方依赖。"""

import json
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1] / "data"
    names = (
        "elements",
        "weapon_types",
        "classes",
        "items",
        "skills",
        "monsters",
        "maps",
    )
    tables = {}
    all_ids = set()
    for name in names:
        rows = json.loads((root / f"{name}.json").read_text(encoding="utf-8"))
        tables[name] = {row["id"]: row for row in rows}
        assert len(tables[name]) == len(rows), f"重复 ID: {name}"
        assert not all_ids.intersection(tables[name]), f"跨表重复 ID: {name}"
        all_ids.update(tables[name])

    targets = {
        "element": "elements",
        "weapon": "weapon_types",
        "class": "classes",
        "item": "items",
        "skill": "skills",
        "monster": "monsters",
        "map": "maps",
    }

    def check_refs(value):
        if isinstance(value, dict):
            for key, child in value.items():
                if key.endswith(("_id", "_ids")):
                    for ref in child if isinstance(child, list) else [child]:
                        table = targets[ref.split("_", 1)[0]]
                        assert ref in tables[table], f"悬空引用: {key}={ref}"
                else:
                    check_refs(child)
        elif isinstance(value, list):
            for child in value:
                check_refs(child)

    for table in tables.values():
        check_refs(list(table.values()))
    elements = set(tables["elements"])
    assert len(elements) == len(tables["classes"]) == len(tables["weapon_types"]) == 5
    for cls in tables["classes"].values():
        assert tables["weapon_types"][cls["weapon_type_id"]]["class_id"] == cls["id"]
        assert {a["element_id"] for a in cls["element_affinities"]} == elements
        for table_name in ("items", "skills"):
            rows = [
                r for r in tables[table_name].values() if r["class_id"] == cls["id"]
            ]
            assert len(rows) == 11
            assert {r["required_level"] for r in rows} == set(range(11))
            key = (
                "weapon_type_id" if table_name == "items" else "required_weapon_type_id"
            )
            assert all(r[key] == cls["weapon_type_id"] for r in rows)
        assert set(cls["skill_ids"]) == {
            s["id"] for s in tables["skills"].values() if s["class_id"] == cls["id"]
        }
    for skill in tables["skills"].values():
        for ref in skill["prerequisite_skill_ids"]:
            previous = tables["skills"][ref]
            assert previous["class_id"] == skill["class_id"]
            assert previous["required_level"] < skill["required_level"]
    assert {m["required_level"] for m in tables["maps"].values()} == set(range(11))
    for area in tables["maps"].values():
        mobs = [m for m in tables["monsters"].values() if m["map_id"] == area["id"]]
        assert {m["id"] for m in mobs} == set(area["monster_ids"])
        assert [m["id"] for m in mobs if m["rank"] == "lord"] == [
            area["lord_monster_id"]
        ]
        assert all(m["level"] == area["required_level"] for m in mobs)
        assert {d["item_id"] for m in mobs for d in m["drops"]} == set(
            area["drop_item_ids"]
        )
        for ref in area["connected_map_ids"]:
            assert area["id"] in tables["maps"][ref]["connected_map_ids"]
    for monster in tables["monsters"].values():
        assert {
            a["element_id"] for a in monster["incoming_element_multipliers"]
        } == elements
        assert all(
            0 <= d["probability"] <= 1 and d["quantity"] > 0 for d in monster["drops"]
        )
    for item in tables["items"].values():
        sources = [
            m
            for m in tables["monsters"].values()
            if any(d["item_id"] == item["id"] for d in m["drops"])
        ]
        assert sources
        assert {m["id"] for m in sources} == set(item["source_monster_ids"])
        assert {m["map_id"] for m in sources} == set(item["source_map_ids"])

    examples = json.loads((root / "query_examples.json").read_text(encoding="utf-8"))
    check_refs(examples)
    for example in examples:
        if "expected_map_ids" in example:
            actual = (
                tables["items"][example["item_id"]]["source_map_ids"]
                if "item_id" in example
                else [tables["monsters"][example["monster_id"]]["map_id"]]
            )
            assert actual == example["expected_map_ids"]
        if "expected_monster_ids" in example:
            assert (
                tables["items"][example["item_id"]]["source_monster_ids"]
                == example["expected_monster_ids"]
            )
        if "expected_accessible" in example:
            area = tables["maps"][example["map_id"]]
            assert (example["player_level"] >= area["required_level"]) == example[
                "expected_accessible"
            ]
            assert set(example["recommended_monster_ids"]) <= set(area["monster_ids"])
        if "expected_damage_multiplier" in example:
            monster = tables["monsters"][example["monster_id"]]
            rates = {
                r["element_id"]: r["damage_multiplier"]
                for r in monster["incoming_element_multipliers"]
            }
            assert rates[example["element_id"]] == example["expected_damage_multiplier"]
        if "expected_element_ids" in example:
            affinities = tables["classes"][example["class_id"]]["element_affinities"]
            maximum = max(a["damage_multiplier"] for a in affinities)
            assert [
                a["element_id"] for a in affinities if a["damage_multiplier"] == maximum
            ] == example["expected_element_ids"]
        if "expected_item_ids" in example:
            if "ranking_rule" in example:
                cls = tables["classes"][example["class_id"]]
                monster = tables["monsters"][example["monster_id"]]
                affinity = {
                    a["element_id"]: a["damage_multiplier"]
                    for a in cls["element_affinities"]
                }
                rates = {
                    a["element_id"]: a["damage_multiplier"]
                    for a in monster["incoming_element_multipliers"]
                }
                candidates = [
                    i
                    for i in tables["items"].values()
                    if i["class_id"] == cls["id"]
                    and i["required_level"] <= example["player_level"]
                ]
                best = max(
                    candidates,
                    key=lambda i: (
                        i["attack"] * affinity[i["element_id"]] * rates[i["element_id"]]
                    ),
                )
                actual = [best["id"]]
            elif "map_id" in example:
                actual = tables["maps"][example["map_id"]]["drop_item_ids"]
            else:
                actual = [
                    i["id"]
                    for i in tables["items"].values()
                    if i["element_id"] == example["element_id"]
                ]
            assert actual == example["expected_item_ids"], example["question"]
    print("校验通过：ID 引用、职业等级覆盖、掉落反向索引和 8 个示例查询。")


if __name__ == "__main__":
    main()
