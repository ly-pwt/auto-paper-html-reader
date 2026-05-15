#!/usr/bin/env python3
"""Validate auto-paper-html-reader HTML reports.

This hook is intentionally deterministic: it checks whether the generated HTML
contains the structural pieces required by the skill contract. When it fails,
Codex should edit the report to add the missing substantive content and rerun
this hook until it passes.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


REQUIRED_SECTIONS = [
    "summary",
    "technical-roadmap",
    "contributions",
    "related-work-comparison",
    "writing-logic",
    "critical-analysis",
    "method",
    "experiments",
    "figures",
    "open-questions",
]

OPTIONAL_SECTIONS = [
    "related-work",
    "code-observations",
]

REQUIRED_TOKENS = [
    "大白话",
    "data-plain=",
    "plain-toggle",
    "technical-roadmap",
    "related-work-comparison",
    "writing-logic",
    "logic-timeline",
    "figure-panel",
    "roadmap-step",
]


class ReportParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.classes: set[str] = set()
        self.img_srcs: list[str] = []
        self.tables = 0
        self.data_plain_count = 0
        self.current_section: str | None = None
        self.section_text: dict[str, list[str]] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = {key: value or "" for key, value in attrs}
        if "id" in attrs_dict:
            self.ids.add(attrs_dict["id"])
        if "class" in attrs_dict:
            for cls in attrs_dict["class"].split():
                self.classes.add(cls)
        if tag == "section":
            self.current_section = attrs_dict.get("id")
            if self.current_section:
                self.section_text.setdefault(self.current_section, [])
        if tag == "img":
            self.img_srcs.append(attrs_dict.get("src", ""))
        if tag == "table":
            self.tables += 1
        if "data-plain" in attrs_dict:
            self.data_plain_count += 1

    def handle_endtag(self, tag: str) -> None:
        if tag == "section":
            self.current_section = None

    def handle_data(self, data: str) -> None:
        if self.current_section:
            text = data.strip()
            if text:
                self.section_text.setdefault(self.current_section, []).append(text)


def local_image_exists(html_path: Path, src: str) -> bool:
    parsed = urlparse(src)
    if parsed.scheme or src.startswith("#") or not src:
        return True
    return (html_path.parent / src).exists()


def count_wordsish(text: str) -> int:
    # Chinese text has no spaces, so mix rough CJK chars and word chunks.
    cjk = len(re.findall(r"[\u4e00-\u9fff]", text))
    words = len(re.findall(r"[A-Za-z0-9_+-]+", text))
    return cjk + words


def validate(html_path: Path) -> dict[str, object]:
    html = html_path.read_text(encoding="utf-8")
    parser = ReportParser()
    parser.feed(html)

    missing: list[str] = []
    warnings: list[str] = []

    for section_id in REQUIRED_SECTIONS:
        if section_id not in parser.ids:
            missing.append(f"missing required section: #{section_id}")

    for token in REQUIRED_TOKENS:
        if token not in html:
            missing.append(f"missing required token/class/content marker: {token}")

    min_plain = 12
    if parser.data_plain_count < min_plain:
        missing.append(f"too few plain-language explanations: {parser.data_plain_count} < {min_plain}")

    min_figures = 3
    if len(parser.img_srcs) < min_figures:
        missing.append(f"too few embedded figures/images: {len(parser.img_srcs)} < {min_figures}")

    broken_images = [src for src in parser.img_srcs if not local_image_exists(html_path, src)]
    if broken_images:
        missing.append("broken local image links: " + ", ".join(broken_images))

    if parser.tables < 2:
        missing.append(f"too few comparison/result tables: {parser.tables} < 2")

    section_min_lengths = {
        "technical-roadmap": 250,
        "related-work-comparison": 350,
        "writing-logic": 300,
        "critical-analysis": 250,
        "figures": 350,
    }
    for section_id, min_len in section_min_lengths.items():
        if section_id in parser.ids:
            text = " ".join(parser.section_text.get(section_id, []))
            score = count_wordsish(text)
            if score < min_len:
                missing.append(f"section #{section_id} appears too thin: {score} < {min_len}")

    if "code-observations" not in parser.ids:
        warnings.append("optional section #code-observations missing; acceptable only when no public code was found")
    if "related-work" not in parser.ids:
        warnings.append("optional section #related-work missing; acceptable if related-work-comparison includes citations")

    return {
        "ok": not missing,
        "html": str(html_path),
        "missing": missing,
        "warnings": warnings,
        "stats": {
            "sections": sorted(parser.ids),
            "images": len(parser.img_srcs),
            "tables": parser.tables,
            "plain_language_blocks": parser.data_plain_count,
        },
        "next_action": (
            "Edit the HTML to add the missing sections/content, then rerun this hook."
            if missing
            else "Report satisfies the structural skill contract."
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("html", help="Path to the generated HTML report")
    ap.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = ap.parse_args()

    html_path = Path(args.html)
    if not html_path.exists():
        print(f"ERROR: HTML file not found: {html_path}", file=sys.stderr)
        return 2

    result = validate(html_path)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        status = "PASS" if result["ok"] else "FAIL"
        print(f"[{status}] {html_path}")
        for item in result["missing"]:
            print(f"- MISSING: {item}")
        for item in result["warnings"]:
            print(f"- WARNING: {item}")
        print(f"- STATS: {result['stats']}")
        print(f"- NEXT: {result['next_action']}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
