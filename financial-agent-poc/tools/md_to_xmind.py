#!/usr/bin/env python3
"""Convert Phase1 testcase Markdown to XMind 8 compatible .xmind (ZIP + content.xml)."""

from __future__ import annotations

import argparse
import re
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape


NS_CONTENT = "urn:xmind:xmap:xmlns:content:2.0"
NS_MANIFEST = "urn:xmind:xmap:xmlns:manifest:1.0"
NS_META = "urn:xmind:xmap:xmlns:meta:2.0"


def _next_id(counter: list[int]) -> str:
    counter[0] += 1
    return f"id-{counter[0]}"


def _strip_md_title(s: str) -> str:
    s = s.strip()
    s = re.sub(r"^#+\s*", "", s)
    return s.strip()


def parse_markdown(md_text: str, _counter: list[int]) -> tuple[str, list[dict]]:
    """Return root title and tree of {title, children, level}."""
    lines = md_text.splitlines()
    root_title = "Mind Map"
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("# ") and not line.startswith("##"):
            root_title = _strip_md_title(line)
            i += 1
            break
        i += 1

    # Skip intro blockquotes until ---
    while i < len(lines):
        if lines[i].strip().startswith("---"):
            i += 1
            break
        i += 1

    root = {"title": root_title, "children": [], "level": 0}
    stack: list[dict] = [root]
    current_case: dict | None = None

    def flush_case() -> None:
        nonlocal current_case
        current_case = None

    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip()

        if line.strip() == "---":
            i += 1
            flush_case()
            continue

        if not line.strip():
            i += 1
            continue

        if line.startswith(">") or line.startswith("|"):
            i += 1
            continue

        if line.startswith("#### "):
            flush_case()
            title = _strip_md_title(line)
            node = {"title": title, "children": [], "level": 4}
            while stack[-1]["level"] >= 4:
                stack.pop()
            stack[-1]["children"].append(node)
            stack.append(node)
            current_case = node
            i += 1
            continue

        if line.startswith("### "):
            flush_case()
            title = _strip_md_title(line)
            node = {"title": title, "children": [], "level": 3}
            while stack[-1]["level"] >= 3:
                stack.pop()
            stack[-1]["children"].append(node)
            stack.append(node)
            i += 1                                  
            continue

        if line.startswith("## "):
            flush_case()
            title = _strip_md_title(line)
            node = {"title": title, "children": [], "level": 2}
            while stack[-1]["level"] >= 2:
                stack.pop()
            stack[-1]["children"].append(node)
            stack.append(node)
            i += 1
            continue

        # Bullet under #### -> detail child
        if current_case and line.startswith("- "):
            detail = line[2:].strip()
            detail = re.sub(r"\*\*(.+?)\*\*", r"\1", detail)
            current_case["children"].append({"title": detail, "children": [], "level": 5})
            i += 1
            continue

        i += 1

    return root_title, root["children"]


def topic_xml(node: dict, counter: list[int]) -> str:
    tid = _next_id(counter)
    title = escape(node["title"])
    parts = [f'<topic id="{tid}"><title>{title}</title>']
    if node.get("children"):
        parts.append('<children><topics type="attached">')
        for ch in node["children"]:
            parts.append(topic_xml(ch, counter))
        parts.append("</topics></children>")
    parts.append("</topic>")
    return "".join(parts)


def build_content_xml(root_title: str, branches: list[dict], counter: list[int]) -> str:
    root_tid = _next_id(counter)
    sheet_id = _next_id(counter)
    inner_children = ""
    if branches:
        inner_children = '<children><topics type="attached">'
        for b in branches:
            inner_children += topic_xml(b, counter)
        inner_children += "</topics></children>"

    root_title_e = escape(root_title)
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<xmap-content xmlns="urn:xmind:xmap:xmlns:content:2.0" xmlns:fo="http://www.w3.org/1999/XSL/Format" modified-by="md_to_xmind" version="2.0">
  <sheet id="{sheet_id}">
    <topic id="{root_tid}" structure-class="org.xmind.ui.map.unbalanced">
      <title>{root_title_e}</title>
      {inner_children}
    </topic>
  </sheet>
</xmap-content>
"""


def build_manifest() -> str:
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<manifest xmlns="{NS_MANIFEST}">
  <file-entry full-path="content.xml" media-type="text/xml"/>
  <file-entry full-path="meta.xml" media-type="text/xml"/>
  <file-entry full-path="META-INF/manifest.xml" media-type="text/xml"/>
</manifest>
"""


def build_meta() -> str:
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<meta xmlns="{NS_META}" version="2.0">
  <Author><Name>financial-agent-poc</Name></Author>
</meta>
"""


def write_xmind(out_path: Path, content_xml: str) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("content.xml", content_xml.encode("utf-8"))
        z.writestr("meta.xml", build_meta().encode("utf-8"))
        z.writestr("META-INF/manifest.xml", build_manifest().encode("utf-8"))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", "-i", type=Path, required=True)
    ap.add_argument("--output", "-o", type=Path, required=True)
    args = ap.parse_args()

    md = args.input.read_text(encoding="utf-8")
    counter = [0]
    root_title, branches = parse_markdown(md, counter)
    counter = [0]
    xml_content = build_content_xml(root_title, branches, counter)
    write_xmind(args.output, xml_content)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
