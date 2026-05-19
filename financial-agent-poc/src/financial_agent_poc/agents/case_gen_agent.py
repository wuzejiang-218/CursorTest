from __future__ import annotations

from typing import Any

from financial_agent_poc.models import FlowId, RequirementModel, TestCase


class CaseGenAgent:
    PROMPT_VERSION = "casegen-v1-template"

    def generate(self, req: RequirementModel) -> list[TestCase]:
        cases: list[TestCase] = []
        for flow in req.flows:
            cases.extend(self._cases_for_flow(flow, req))
        return cases

    def _cases_for_flow(self, flow: FlowId, req: RequirementModel) -> list[TestCase]:
        if flow == "F1":
            return [
                TestCase(
                    id="F1-CREDIT-HAPPY",
                    flow="F1",
                    title="授信进件成功路径",
                    steps=[
                        {"id": "api_apply", "executor": "api", "action": "credit_apply"},
                        {"id": "data_check", "executor": "data", "action": "row_exists"},
                    ],
                    expected={"http_status": 200, "biz_code": "OK", "credit_status": "APPROVED"},
                )
            ]
        if flow == "F2":
            return [
                TestCase(
                    id="F2-RISK-DECISION",
                    flow="F2",
                    title="风控决策码与规则版本",
                    steps=[
                        {"id": "api_risk", "executor": "api", "action": "risk_decide"},
                    ],
                    expected={"http_status": 200, "decision": "PASS", "rule_version": "BASELINE-POC"},
                )
            ]
        return [
            TestCase(
                id="F3-DISBURSE-CHECK",
                flow="F3",
                title="放款前状态与额度校验",
                steps=[
                    {"id": "ui_login", "executor": "ui", "action": "noop_check"},
                    {"id": "api_disburse", "executor": "api", "action": "disburse_validate"},
                ],
                expected={"http_status": 200, "order_status": "READY", "amount_le_credit": True},
            )
        ]

    def to_trace(self, cases: list[TestCase]) -> dict[str, Any]:
        return {
            "agent": "CaseGenAgent",
            "prompt_version": self.PROMPT_VERSION,
            "case_ids": [c.id for c in cases],
        }
