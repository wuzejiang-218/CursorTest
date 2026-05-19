from __future__ import annotations

from typing import Any, Optional

from financial_agent_poc.executors.api_runner import ApiRunner
from financial_agent_poc.executors.data_validator import DataValidator
from financial_agent_poc.executors.ui_runner import UiRunner
from financial_agent_poc.models import StepResult, TestCase


class SchedulerAgent:
    def __init__(
        self,
        api: Optional[ApiRunner] = None,
        ui: Optional[UiRunner] = None,
        data: Optional[DataValidator] = None,
    ) -> None:
        self._api = api or ApiRunner()
        self._ui = ui or UiRunner()
        self._data = data or DataValidator()

    def run_case(self, case: TestCase) -> list[StepResult]:
        results: list[StepResult] = []
        for step in case.steps:
            ex = step.get("executor")
            if ex == "api":
                results.append(self._api.run(step, case))
            elif ex == "ui":
                results.append(self._ui.run(step, case))
            elif ex == "data":
                results.append(self._data.run(step, case))
            else:
                results.append(
                    StepResult(
                        step_id=str(step.get("id")),
                        executor="unknown",
                        ok=False,
                        detail={"error": f"unknown executor {ex}"},
                    )
                )
        return results
