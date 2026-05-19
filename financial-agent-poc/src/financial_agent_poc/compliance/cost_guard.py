from __future__ import annotations

from dataclasses import dataclass

from financial_agent_poc.compliance.governance import load_governance


@dataclass
class CostGuard:
    """Token budget stand-in: counts characters for PoC."""

    def __init__(self) -> None:
        gov = load_governance()
        mc = gov.get("model_cost") or {}
        self.budget = int(mc.get("token_budget_per_run", 50_000))

    def estimate_tokens(self, text: str) -> int:
        return max(1, len(text) // 4)

    def allow(self, accumulated: int, chunk: str) -> bool:
        return accumulated + self.estimate_tokens(chunk) <= self.budget
