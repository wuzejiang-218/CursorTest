from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


FlowId = Literal["F1", "F2", "F3"]


@dataclass
class RequirementModel:
    """Structured output of ParserAgent."""

    raw_text: str
    flows: list[FlowId]
    environment: str
    actor: str
    expectations_summary: str


@dataclass
class TestCase:
    id: str
    flow: FlowId
    title: str
    steps: list[dict[str, Any]]
    expected: dict[str, Any]


@dataclass
class StepResult:
    step_id: str
    executor: str
    ok: bool
    detail: dict[str, Any]


@dataclass
class RunReport:
    run_id: str
    cases: list[dict[str, Any]] = field(default_factory=list)
    overall_pass: bool = True
    trace_version: str = "poc-0.1"
