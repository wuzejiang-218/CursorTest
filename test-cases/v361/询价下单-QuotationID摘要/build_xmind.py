# -*- coding: utf-8 -*-
"""Generate XMind for Quotation ID summary (semantic titles, no TC-* ids)."""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from _xmind_common import module, scenario, sheet, write_xmind  # noqa: E402

OUTPUT = Path(__file__).with_name("询价下单-QuotationID摘要-测试用例.xmind")


def build_tree() -> list[dict]:
    return sheet(
        "v3.61 · 询价下单 Quotation ID\nⓘ 摘要 · Blotter",
        "v3.61 Quotation ID 询价摘要",
        [
            module(
                "1. UI 与交互",
                [
                    scenario(
                        "Quotation ID 旁信息图标",
                        ["预期：ID 右侧 ⓘ 可见对齐"],
                    ),
                    scenario(
                        "点击图标查看摘要",
                        ["预期：浮层展示；当前页不跳转"],
                    ),
                    scenario(
                        "点击 ID 文本跳转",
                        ["预期：仍进入询价页（回归）"],
                    ),
                    scenario("非询价单", ["预期：无 ⓘ 或无报错"]),
                ],
            ),
            module(
                "2. 摘要数据",
                [
                    scenario(
                        "与 Best Price 一致",
                        ["预期：摘要=各 Payoff 最优价字段"],
                    ),
                    scenario("多 Payoff", ["预期：每 Payoff 独立摘要块"]),
                    scenario("改单后刷新", ["预期：展示最新 Best Price"]),
                ],
            ),
            module(
                "3. 权限",
                [
                    scenario(
                        "AQDQVAN · 无 credit charge",
                        ["预期：敏感字段隐藏/脱敏"],
                    ),
                    scenario(
                        "AQDQVAN · 有 credit charge",
                        ["预期：与询价页可见性一致"],
                    ),
                    scenario(
                        "AQDQ · user uf 受限",
                        ["预期：字段按 uf 限制"],
                    ),
                    scenario("越权对比", ["预期：低权限不可见高权限字段"]),
                ],
            ),
            module(
                "4. 边界异常",
                [
                    scenario("无 Best Price", ["预期：友好空态"]),
                    scenario("弱网", ["预期：Loading / 超时重试"]),
                ],
            ),
            module(
                "5. 回归",
                [
                    scenario("General Info", ["预期：步骤条等无错位"]),
                    scenario("参数表", ["预期：Underlying/Coupon 表正常"]),
                ],
            ),
        ],
    )


if __name__ == "__main__":
    write_xmind(OUTPUT, build_tree())
    print(f"Written: {OUTPUT}")
