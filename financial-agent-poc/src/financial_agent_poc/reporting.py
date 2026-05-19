from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_reports(out_dir: Path, run_id: str, bundle: dict[str, Any]) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / f"run-{run_id}.json"
    md_path = out_dir / f"run-{run_id}.md"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(bundle, f, ensure_ascii=False, indent=2)

    cases = bundle.get("cases", [])
    lines = [
        f"# Test agent run `{run_id}`",
        "",
        f"- Overall: **{'PASS' if bundle.get('overall_pass') else 'FAIL'}**",
        f"- Trace version: `{bundle.get('trace_version')}`",
        "",
        "## Cases",
        "",
    ]
    for c in cases:
        status = "PASS" if c.get("pass") else "FAIL"
        lines.append(f"- **{c.get('case_id')}**: {status}")
        if c.get("mismatches"):
            for m in c["mismatches"]:
                lines.append(f"  - mismatch: {m}")
    lines.append("")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, md_path
