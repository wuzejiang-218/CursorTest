from __future__ import annotations

from typing import Any

from financial_agent_poc.models import StepResult, TestCase


class ApiRunner:
    """Simulated API layer for PoC (swap with real HTTP client)."""

    def run(self, step: dict[str, Any], case: TestCase) -> StepResult:
        action = step.get("action")
        observed: dict[str, Any] = {"http_status": 200}

        if action == "credit_apply":
            observed.update({"biz_code": "OK", "credit_status": "APPROVED"})
        elif action == "risk_decide":
            observed.update({"decision": "PASS", "rule_version": "BASELINE-POC"})
        elif action == "disburse_validate":
            observed.update({"order_status": "READY", "amount_le_credit": True})
        else:
            return StepResult(
                step_id=str(step.get("id")),
                executor="api",
                ok=False,
                detail={"error": f"unknown action {action}", "observed": {}},
            )

        return StepResult(
            step_id=str(step.get("id")),
            executor="api",
            ok=True,
            detail={"action": action, "observed": observed},
        )
