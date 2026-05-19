from __future__ import annotations

from typing import Any

from financial_agent_poc.models import StepResult, TestCase


class UiRunner:
    """Placeholder UI executor (PoC: no real browser)."""

    def run(self, step: dict[str, Any], case: TestCase) -> StepResult:
        return StepResult(
            step_id=str(step.get("id")),
            executor="ui",
            ok=True,
            detail={"action": step.get("action"), "observed": {}},
        )
