from pathlib import Path

from financial_agent_poc.pipeline import run_pipeline


def test_run_pipeline_smoke(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    req = root / "examples" / "requirements" / "sample.md"
    bundle = run_pipeline(req, tmp_path)
    assert bundle["overall_pass"] is True
    assert len(bundle["cases"]) >= 1
