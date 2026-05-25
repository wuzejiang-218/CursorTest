# -*- coding: utf-8 -*-
"""Generate XMind for FCN Order Type sharing (semantic titles, no TC-* ids)."""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from _xmind_common import module, scenario, sheet, write_xmind  # noqa: E402

OUTPUT = Path(__file__).with_name("FCN-OrderType-分享-测试用例.xmind")


def build_tree() -> list[dict]:
    return sheet(
        "v3.61 · FCN 分享 Order Type\n(EasyConnect · Web + App)",
        "v3.61 FCN Order Type 分享",
        [
            module(
                "1. 产品详情 UI",
                [
                    scenario(
                        "Limit Price 展示",
                        [
                            "前置：已登录；存在 Limit 类型 FCN",
                            "步骤：打开详情/卡片",
                            "预期：展示 Order Type=Limit Price",
                            "预期：展示标的 @ 价格；主金额正常",
                        ],
                    ),
                    scenario(
                        "Market Price 展示",
                        [
                            "步骤：打开 Market 类型产品详情",
                            "预期：Order Type=Market Price",
                            "预期：无 Limit 专属标的@价格行",
                        ],
                    ),
                ],
            ),
            module(
                "2. Web 分享",
                [
                    scenario(
                        "Web 分享 · Limit",
                        [
                            "步骤：详情页 Web 分享",
                            "预期：含 Order Type=Limit Price 与标的@价格",
                            "预期：与详情一致",
                        ],
                    ),
                    scenario(
                        "Web 分享 · Market",
                        ["步骤：Market 产品 Web 分享", "预期：Order Type=Market Price"],
                    ),
                    scenario(
                        "分享字段完整性",
                        ["预期：原有 Coupon/Tenor 等仍在", "预期：Order Type 位置正确"],
                    ),
                ],
            ),
            module(
                "3. App 分享",
                [
                    scenario(
                        "App 分享 · Limit / Market",
                        [
                            "步骤：iOS/Android 分享",
                            "预期：卡片含正确 Order Type",
                        ],
                    ),
                    scenario(
                        "App 与 Web 一致",
                        ["步骤：同一产品分别 Web/App 分享", "预期：文案与数值一致"],
                    ),
                ],
            ),
            module(
                "4. 数据一致性",
                [
                    scenario(
                        "详情与分享一致",
                        ["步骤：记录详情后分享", "预期：逐字段一致"],
                    ),
                    scenario(
                        "改单后刷新",
                        ["步骤：改下单方式后重新分享", "预期：展示最新 Order Type"],
                    ),
                ],
            ),
            module(
                "5. 边界与异常",
                [
                    scenario("无 orderType", ["预期：不崩溃；占位或隐藏"]),
                    scenario("多标的 Limit", ["预期：换行/省略符合设计"]),
                    scenario("长文案", ["预期：卡片无截断重叠"]),
                ],
            ),
            module(
                "6. 国际化",
                [
                    scenario("英文", ["预期：Order Type / Limit / Market Price"]),
                    scenario("中文", ["预期：订单类型/限价/市价翻译正确"]),
                ],
            ),
            module(
                "7. 回归",
                [
                    scenario(
                        "募集与渠道",
                        [
                            "预期：进度条/Underlying 无回归",
                            "预期：复制链接/海报均含新字段",
                        ],
                    ),
                ],
            ),
        ],
    )


if __name__ == "__main__":
    write_xmind(OUTPUT, build_tree())
    print(f"Written: {OUTPUT}")
