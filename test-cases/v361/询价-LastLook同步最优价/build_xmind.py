# -*- coding: utf-8 -*-
"""Generate XMind for Last Look sync best price (semantic titles, no TC-* ids)."""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from _xmind_common import module, scenario, sheet, write_xmind  # noqa: E402

OUTPUT = Path(__file__).with_name("询价-LastLook同步最优价-测试用例.xmind")


def build_tree() -> list[dict]:
    return sheet(
        "v3.61 · 询价 Last Look\n同步最优价",
        "v3.61 Last Look",
        [
            module(
                "1. 机构配置",
                [
                    scenario(
                        "Automatic + FCN + 5min 触发",
                        ["步骤：配置 Matched Issuer、自动条件", "预期：保存成功"],
                    ),
                    scenario(
                        "Manual + 授权用户",
                        ["步骤：Mode=Manual，选 U1", "预期：仅 U1 可发起"],
                    ),
                    scenario(
                        "价差阈值 10bp",
                        ["步骤：配置 Difference Value", "预期：超阈值不自动触发"],
                    ),
                    scenario("授权为空拒绝发起", ["预期：提示配置 Setting"]),
                ],
            ),
            module(
                "2. Issuer 配置",
                [
                    scenario(
                        "Buyside 行 + 邮件确认",
                        ["步骤：CAI HK 行 + Reply Mode", "预期：双向匹配成功"],
                    ),
                    scenario(
                        "无 Buyside 行",
                        ["预期：不创建；提示不匹配"],
                    ),
                    scenario(
                        "Reply Automatic",
                        ["预期：自动确认改价"],
                    ),
                    scenario(
                        "Price Validity 过期",
                        ["预期：不可确认"],
                    ),
                ],
            ),
            module(
                "3. 发起与拦截",
                [
                    scenario("非最优可发起", ["预期：待确认"]),
                    scenario("最优不可发起", ["预期：拒绝"]),
                    scenario("重复发起拦截", ["预期：仅一条有效申请"]),
                    scenario("新回复使原申请失效", ["预期：可按新回复再评估"]),
                ],
            ),
            module(
                "4. 手动 / 自动发起",
                [
                    scenario("U1 手动发起成功", ["预期：trigger_mode=manual"]),
                    scenario("U2 未授权拒绝", ["预期：拒绝"]),
                    scenario("满 5min 自动创建", ["预期：trigger_mode=automatic"]),
                    scenario("20min 未确认失效", ["预期：已失效"]),
                ],
            ),
            module(
                "5. Issuer 确认",
                [
                    scenario("邮件确认改价", ["预期：最优价更新"]),
                    scenario("邮件拒绝", ["预期：价格不变"]),
                    scenario("确认时跟最新最优价", ["预期：审计快照差异"]),
                    scenario("机构不可代确认", ["预期：拒绝"]),
                ],
            ),
            module(
                "6. 状态与失效",
                [
                    scenario("超过 Validity 失效", ["预期：已失效"]),
                    scenario("询价关闭", ["预期：待确认全部失效"]),
                    scenario("已确认不可再发起", ["预期：拒绝"]),
                    scenario("并发确认一致", ["预期：无脏数据"]),
                ],
            ),
            module(
                "7. 端到端",
                [
                    scenario(
                        "手动发起 → 邮件确认",
                        ["步骤：双端配置→询价→回复→发起→确认", "预期：全链路成功"],
                    ),
                    scenario(
                        "自动发起 → 自动确认",
                        ["预期：automatic 全链路"],
                    ),
                    scenario("配置不匹配", ["预期：失败提示"]),
                ],
            ),
            module(
                "8. Lastlook UI",
                [
                    scenario("比价展示", ["预期：各 Issuer vs 最优"]),
                    scenario("申请状态与 trigger_mode", ["预期：展示正确"]),
                    scenario("Reply Mode 摘要", ["预期：与配置一致"]),
                ],
            ),
        ],
    )


if __name__ == "__main__":
    write_xmind(OUTPUT, build_tree())
    print(f"Written: {OUTPUT}")
