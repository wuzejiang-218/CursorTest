from __future__ import annotations

import re
from typing import Any, Optional

from financial_agent_poc.compliance.governance import load_governance


def desensitize_text(text: str, governance: Optional[dict[str, Any]] = None) -> str:
    gov = governance if governance is not None else load_governance()
    cfg = (gov.get("desensitization") or {}) if gov else {}
    if not cfg.get("enabled", True):
        return text
    patterns = cfg.get("patterns") or _default_patterns()
    out = text
    for p in patterns:
        rx = p.get("regex")
        rep = p.get("replacement", "***")
        if rx:
            out = re.sub(rx, rep, out)
    return out


def _default_patterns() -> list[dict[str, str]]:
    return [
        {
            "name": "id_card_cn",
            "regex": r"\b[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[0-9Xx]\b",
            "replacement": "***ID18***",
        },
        {
            "name": "mobile_cn",
            "regex": r"\b1[3-9]\d{9}\b",
            "replacement": "***MOBILE***",
        },
    ]
