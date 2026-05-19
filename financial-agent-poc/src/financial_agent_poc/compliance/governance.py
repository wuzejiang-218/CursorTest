from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

import yaml


def load_governance(path: Optional[Path] = None) -> dict[str, Any]:
    root = Path(__file__).resolve().parents[3]
    cfg = path or (root / "config" / "governance.yaml")
    if not cfg.exists():
        return {}
    with cfg.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}
