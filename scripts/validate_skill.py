#!/usr/bin/env python3
"""Structural checks for the NMTI skill package (no network)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_REFERENCE = (
    "questions.md",
    "nmti-framework.md",
)

EXPECTED_CODES = (
    "ASPU",
    "ASPH",
    "ASDU",
    "ASDH",
    "ACPU",
    "ACPH",
    "ACDU",
    "ACDH",
    "RSPU",
    "RSPH",
    "RSDU",
    "RSDH",
    "RCPU",
    "RCPH",
    "RCDU",
    "RCDH",
)


def err(msg: str) -> None:
    print(f"error: {msg}", file=sys.stderr)


def slice_after_heading(text: str, heading: str) -> str:
    i = text.find(heading)
    if i == -1:
        return ""
    return text[i:]


def parse_mapping_codes(section: str) -> list[str]:
    codes: list[str] = []
    for line in section.splitlines():
        m = re.match(r"^\|\s*([ARSCPDUH]{4})\s*\|", line.strip())
        if m and m.group(1) not in codes:
            codes.append(m.group(1))
    return codes


def main() -> int:
    skill = ROOT / "SKILL.md"
    if not skill.is_file():
        err("missing SKILL.md at repository root")
        return 1

    ref_dir = ROOT / "reference"
    if not ref_dir.is_dir():
        err("missing reference/ directory")
        return 1

    for name in REQUIRED_REFERENCE:
        p = ref_dir / name
        if not p.is_file():
            err(f"missing reference/{name}")
            return 1

    qs_path = ref_dir / "questions.md"
    qs = qs_path.read_text(encoding="utf-8")

    missing_q = [i for i in range(1, 17) if f"## Q{i}" not in qs]
    if missing_q:
        err(f"questions.md: missing question headings: {missing_q}")
        return 1

    map_section = slice_after_heading(qs, "# 结果映射表")
    if not map_section:
        err("questions.md: missing '# 结果映射表'")
        return 1
    map_block = map_section.split("\n#", 1)[0]
    found = parse_mapping_codes(map_block)
    if found != list(EXPECTED_CODES):
        err(
            "questions.md: 结果映射表 codes mismatch.\n"
            f"  expected: {list(EXPECTED_CODES)}\n"
            f"  found:    {found}"
        )
        return 1

    print("ok: SKILL.md, reference files, Q1–Q16, 结果映射表一致")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
