# -*- coding: utf-8 -*-
"""Generate XMind for ELN UF validation (semantic titles, no TC-* ids)."""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from _xmind_common import module, scenario, sheet, write_xmind  # noqa: E402

OUTPUT = Path(__file__).with_name("ELN-询价UF重复校验-测试用例.xmind")


def build_tree() -> list[dict]:
    return sheet(
        "v3.61 · ELN 询价\n除 UF 外条款相同 → 拦截",
        "v3.61 ELN UF 校验",
        [
            module(
                "1. 拦截（P0）",
                [
                    scenario(
                        "仅 UF 不同 · 两行",
                        [
                            "步骤：ELN Tab 填两行，仅 UF 不同",
                            "步骤：Submit",
                            "预期：拦截；英文/中文提示正确",
                            "预期：不提交成功",
                        ],
                    ),
                    scenario(
                        "仅 UF 不同 · 三行",
                        ["步骤：三行仅 UF 不同", "预期：同样拦截"],
                    ),
                    scenario(
                        "改 Strike 后放行",
                        [
                            "步骤：使 Strike 也不同",
                            "预期：不再因本规则拦截",
                        ],
                    ),
                ],
            ),
            module(
                "2. 放行",
                [
                    scenario("UF 也相同", ["预期：非本规则拦截"]),
                    scenario("Strike 不同", ["预期：放行"]),
                    scenario("Gross Margin 不同", ["预期：放行"]),
                    scenario("单行 ELN", ["预期：放行"]),
                ],
            ),
            module(
                "3. 品类范围",
                [
                    scenario("FCN Tab 仅 UF 不同", ["预期：无 ELN 专用提示"]),
                    scenario("切换 Tab 再回 ELN", ["预期：数据保留"]),
                ],
            ),
            module(
                "4. 交互体验",
                [
                    scenario("提示形态", ["预期：Toast/弹窗；可再次 Submit"]),
                    scenario("删至一行", ["预期：不拦截"]),
                ],
            ),
        ],
    )


if __name__ == "__main__":
    write_xmind(OUTPUT, build_tree())
    print(f"Written: {OUTPUT}")
