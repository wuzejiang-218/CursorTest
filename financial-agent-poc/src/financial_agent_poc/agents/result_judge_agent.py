from __future__ import annotations

from typing import Any

from financial_agent_poc.models import StepResult, TestCase


class ResultJudgeAgent:
    PROMPT_VERSION = "judge-v1-deterministic"

    def judge(self, case: TestCase, step_results: list[StepResult]) -> dict[str, Any]:
        all_ok = all(r.ok for r in step_results)
        merged: dict[str, Any] = {}
        for r in step_results:
            merged.update(r.detail.get("observed", {}))

        expected = case.expected
        mismatches: list[str] = []

        def expect_key(key: str, comparator=None) -> None:
            if key not in expected:
                return
            exp = expected[key]
            got = merged.get(key)
            if comparator:
                if not comparator(got, exp):
                    mismatches.append(f"{key}: expected {exp!r}, got {got!r}")
            elif got != exp:
                mismatches.append(f"{key}: expected {exp!r}, got {got!r}")

        expect_key("http_status")
        expect_key("biz_code")
        expect_key("credit_status")
        expect_key("decision")
        expect_key("rule_version")
        expect_key("order_status")

        if "amount_le_credit" in expected:
            if merged.get("amount_le_credit") is not True:
                mismatches.append("amount_le_credit: expected True")

        pass_fail = all_ok and not mismatches
        return {
            "case_id": case.id,
            "pass": pass_fail,
            "expected": expected,
            "observed": merged,
            "mismatches": mismatches,
            "step_results": [
                {"step_id": r.step_id, "executor": r.executor, "ok": r.ok, "detail": r.detail} for r in step_results
            ],
            "agent": "ResultJudgeAgent",
            "prompt_version": self.PROMPT_VERSION,
        }
