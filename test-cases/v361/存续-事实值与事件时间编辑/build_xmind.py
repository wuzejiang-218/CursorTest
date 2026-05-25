# -*- coding: utf-8 -*-
"""Generate XMind: product × trigger event (semantic titles, no TC-* ids)."""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from _xmind_common import module, scenario, sheet, topic, write_xmind  # noqa: E402

OUTPUT = Path(__file__).with_name("存续-事实值与事件时间编辑-测试用例.xmind")

PRODUCTS: list[tuple[str, list[tuple[str, str]]]] = [
    (
        "FCN",
        [
            ("KO Crossed", "Coupon payment；Principal"),
            ("Final Fixing: Cash", "Coupon payment；Principal"),
            ("Final Fixing: Physical", "Shares；Fractional Share Amount"),
            ("KO Not Crossed", "Coupon Payment（观察顺序约束）"),
        ],
    ),
    ("Step-down FCN", [("同 FCN 四事件", "字段与 FCN 一致")]),
    (
        "Sharkfin",
        [
            ("Final Fixing: Performance Coupon", "Principal；Coupon"),
            ("Final Fixing: KO Coupon", "Principal；Coupon"),
        ],
    ),
    (
        "ELN",
        [
            ("Final Fixing: Cash", "Principal"),
            ("Final Fixing: Physical", "Shares；Fractional"),
        ],
    ),
    (
        "BEN",
        [
            ("Final Fixing: Cash", "Coupon；Principal"),
            ("Final Fixing: Physical", "Shares；Fractional"),
        ],
    ),
    (
        "Step-down SCN",
        [
            ("KO Crossed", "Coupon；Principal"),
            ("Final Fixing: Cash（含 Coupon）", "Coupon；Principal"),
            ("Final Fixing: Cash（仅 Principal）", "Principal"),
            ("Final Fixing: Physical", "Shares；Fractional"),
        ],
    ),
    (
        "AQ",
        [
            ("KO Crossed", "Shares；cost"),
            ("KO Not Crossed", "Shares；cost（顺序约束）"),
            ("Final Fixing: Did Not Early Called", "Shares；cost"),
        ],
    ),
    (
        "DQ",
        [
            ("KO Crossed", "Shares；got"),
            ("KO Not Crossed", "Shares；got（顺序约束）"),
            ("Final Fixing: Did Not Early Called", "Shares；got"),
        ],
    ),
]


def event_branch(trigger: str, fields: str) -> dict:
    return topic(
        trigger,
        [
            topic(f"可编辑：{fields}"),
            scenario(
                "编辑事实值",
                ["步骤：点击 ✏️ 修改各字段", "预期：保存成功并持久化"],
            ),
            scenario(
                "修改事件时间",
                ["步骤：修改事件日期", "预期：时间轴更新"],
            ),
            scenario(
                "事件未结束",
                ["预期：无编辑入口"],
            ),
        ],
    )


def build_tree() -> list[dict]:
    product_modules = [
        topic(name, [event_branch(tr, fd) for tr, fd in events])
        for name, events in PRODUCTS
    ]
    return sheet(
        "v3.61 · 存续 Event Schedule\n事实值 + 事件时间可编辑",
        "v3.61 事实值与事件时间",
        [
            module(
                "通用",
                [
                    scenario("事件日程 UI", ["图例：票息/敲出观察", "时间轴展示"]),
                    scenario("权限与弱网", ["无权限只读", "弱网可重试"]),
                    scenario("输入校验", ["非法事实值/日期拦截"]),
                ],
            ),
            *product_modules,
        ],
    )


if __name__ == "__main__":
    write_xmind(OUTPUT, build_tree())
    print(f"Written: {OUTPUT}")
