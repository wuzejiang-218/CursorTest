from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Optional


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Financial test agent PoC runner")
    sub = p.add_subparsers(dest="cmd", required=True)

    run_p = sub.add_parser("run", help="Run minimal agent loop on a requirements markdown file")
    run_p.add_argument("--requirements", "-r", type=Path, required=True)
    run_p.add_argument("--out", type=Path, default=None, help="Report output directory")

    ds_p = sub.add_parser("desensitize", help="Print redacted text (stdin or --text)")
    ds_p.add_argument("--text", type=str, default="")

    args = p.parse_args(argv)
    if args.cmd == "run":
        from financial_agent_poc.pipeline import run_pipeline

        bundle = run_pipeline(args.requirements, args.out)
        print(f"run_id={bundle['run_id']} overall_pass={bundle['overall_pass']}")
        return 0 if bundle["overall_pass"] else 1
    if args.cmd == "desensitize":
        from financial_agent_poc.compliance.desensitize import desensitize_text

        text = args.text or sys.stdin.read()
        sys.stdout.write(desensitize_text(text))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
