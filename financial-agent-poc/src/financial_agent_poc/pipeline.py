from __future__ import annotations

import uuid
from pathlib import Path
from typing import Any, Optional

from financial_agent_poc.agents.case_gen_agent import CaseGenAgent
from financial_agent_poc.agents.parser_agent import ParserAgent
from financial_agent_poc.agents.result_judge_agent import ResultJudgeAgent
from financial_agent_poc.agents.scheduler_agent import SchedulerAgent
from financial_agent_poc.compliance.audit import AuditLogger
from financial_agent_poc.compliance.cost_guard import CostGuard
from financial_agent_poc.compliance.desensitize import desensitize_text
from financial_agent_poc.reporting import write_reports


def run_pipeline(requirements_path: Path, out_dir: Optional[Path] = None) -> dict[str, Any]:
    run_id = uuid.uuid4().hex[:12]
    root = Path(__file__).resolve().parents[2]
    reports_dir = out_dir or (root / "reports")
    raw_text = requirements_path.read_text(encoding="utf-8")

    cost = CostGuard()
    if not cost.allow(0, raw_text):
        raise RuntimeError("Input exceeds token_budget_per_run (PoC stand-in: char-based estimate)")

    audit = AuditLogger(run_id)
    audit.log("run_start", {"requirements_path": str(requirements_path)})

    parser = ParserAgent()
    req = parser.parse(raw_text)
    audit.log("parser_done", {"trace": parser.to_trace(req), "raw_text": raw_text})

    gen = CaseGenAgent()
    cases = gen.generate(req)
    audit.log("casegen_done", {"trace": gen.to_trace(cases)})

    scheduler = SchedulerAgent()
    judge = ResultJudgeAgent()

    case_reports: list[dict[str, Any]] = []
    overall = True
    for tc in cases:
        step_results = scheduler.run_case(tc)
        verdict = judge.judge(tc, step_results)
        case_reports.append(verdict)
        overall = overall and bool(verdict.get("pass"))
        audit.log(
            "case_finished",
            {
                "case_id": tc.id,
                "pass": verdict.get("pass"),
                "mismatches": verdict.get("mismatches"),
            },
        )

    bundle: dict[str, Any] = {
        "run_id": run_id,
        "trace_version": "poc-0.1",
        "overall_pass": overall,
        "requirement_summary": {
            "flows": req.flows,
            "environment": req.environment,
            "actor": req.actor,
            "expectations_redacted": desensitize_text(req.expectations_summary or ""),
        },
        "cases": case_reports,
    }
    write_reports(reports_dir, run_id, bundle)
    audit.log("run_end", {"overall_pass": overall, "reports_dir": str(reports_dir)})
    return bundle
