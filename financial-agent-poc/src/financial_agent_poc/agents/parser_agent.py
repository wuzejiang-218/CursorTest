from __future__ import annotations

import re
from typing import Any

from financial_agent_poc.models import FlowId, RequirementModel


class ParserAgent:
    """Deterministic PoC parser (replace with LLM + schema validation later)."""

    PROMPT_VERSION = "parser-v1-rules"

    def parse(self, markdown_text: str) -> RequirementModel:
        text = markdown_text
        flows: list[FlowId] = []
        if re.search(r"\bF1\b|授信", text):
            flows.append("F1")
        if re.search(r"\bF2\b|风控", text):
            flows.append("F2")
        if re.search(r"\bF3\b|放款", text):
            flows.append("F3")
        if not flows:
            flows = ["F1", "F2", "F3"]

        env_m = re.search(r"环境[：:]\s*`?(\w+)`?", text)
        environment = env_m.group(1) if env_m else "integration"

        user_m = re.search(r"测试用户[：:]\s*`?([\w-]+)`?", text)
        actor = user_m.group(1) if user_m else "POC_USER"

        exp_m = re.search(r"##\s*期望(.+)", text, re.S)
        expectations_summary = (exp_m.group(1).strip()[:500] if exp_m else "").strip()

        return RequirementModel(
            raw_text=text,
            flows=flows,
            environment=environment,
            actor=actor,
            expectations_summary=expectations_summary,
        )

    def to_trace(self, req: RequirementModel) -> dict[str, Any]:
        return {
            "agent": "ParserAgent",
            "prompt_version": self.PROMPT_VERSION,
            "output": {
                "flows": req.flows,
                "environment": req.environment,
                "actor": req.actor,
            },
        }
