from __future__ import annotations

from typing import Any

from financial_agent_poc.models import StepResult, TestCase


class DataValidator:
    """Stub DB row check; extend with read-only SQL in pilot phase."""

    def run(self, step: dict[str, Any], case: TestCase) -> StepResult:
        action = step.get("action")
        if action == "row_exists":
            return StepResult(
                step_id=str(step.get("id")),
                executor="data",
                ok=True,
                detail={"action": action, "observed": {}},
            )
        return StepResult(
            step_id=str(step.get("id")),
            executor="data",
            ok=False,
            detail={"error": f"unknown action {action}", "observed": {}},
        )
