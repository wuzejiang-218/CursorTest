# -*- coding: utf-8 -*-
"""Shared XMind Zen writer for test-cases/ (no TC-* ids in node titles)."""

from __future__ import annotations

import json
import uuid
import zipfile
from pathlib import Path
from typing import Iterable


def _id() -> str:
    return str(uuid.uuid4()).replace("-", "")[:24]


def topic(title: str, children: list[dict] | None = None) -> dict:
    node: dict = {"id": _id(), "title": title}
    if children:
        node["children"] = {"attached": children}
    return node


def scenario(name: str, points: Iterable[str]) -> dict:
    """One test scenario with bullet points (前置/步骤/预期)."""
    return topic(name, [topic(p) for p in points])


def module(name: str, scenarios: list[dict]) -> dict:
    return topic(name, scenarios)


def sheet(root_title: str, sheet_title: str, modules: list[dict]) -> list[dict]:
    return [
        {
            "id": _id(),
            "class": "sheet",
            "title": sheet_title,
            "rootTopic": {
                "id": _id(),
                "class": "topic",
                "title": root_title,
                "structureClass": "org.xmind.ui.map.unbalanced",
                "children": {"attached": modules},
            },
        }
    ]


def write_xmind(path: Path, content: list[dict]) -> None:
    metadata = {
        "creator": {"name": "test-cases", "version": "2.0"},
        "activeSheetId": content[0]["id"],
    }
    manifest = {"file-entries": {"content.json": {}, "metadata.json": {}}}
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("content.json", json.dumps(content, ensure_ascii=False, indent=2))
        zf.writestr("metadata.json", json.dumps(metadata, ensure_ascii=False, indent=2))
        zf.writestr("manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))
