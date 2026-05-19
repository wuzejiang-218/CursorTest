from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from financial_agent_poc.compliance.governance import load_governance


def _hash_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


class AuditLogger:
    def __init__(self, run_id: str, base_dir: Optional[Path] = None) -> None:
        self.run_id = run_id
        root = Path(__file__).resolve().parents[3]
        self.base_dir = base_dir or (root / "reports" / "audit")
        self.gov = load_governance()
        self._enabled = (self.gov.get("audit") or {}).get("enabled", True)
        self._pii_hashes = (self.gov.get("audit") or {}).get("log_pii_hashes_only", True)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self._path = self.base_dir / f"{run_id}.jsonl"

    def log(self, event: str, payload: dict[str, Any]) -> None:
        if not self._enabled:
            return
        body = dict(payload)
        if self._pii_hashes and "raw_text" in body:
            body["raw_text_sha256"] = _hash_text(str(body.pop("raw_text")))
        record = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "run_id": self.run_id,
            "event": event,
            "payload": body,
        }
        with self._path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
