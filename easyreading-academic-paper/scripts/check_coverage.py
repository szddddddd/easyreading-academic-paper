#!/usr/bin/env python3
"""Check that every paper-map unit is represented in the generated article."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


FINAL_STATUSES = {"covered", "unavailable", "not-applicable"}
ALL_STATUSES = FINAL_STATUSES | {"pending"}
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9-]*$")
SOURCE_ID_RE = re.compile(
    r"""data-source-id\s*=\s*["']([^"']+)["']""", re.IGNORECASE
)


def validate(paper_map: dict[str, Any], article: str) -> tuple[list[str], list[str], Counter]:
    errors: list[str] = []
    warnings: list[str] = []
    counts: Counter = Counter()

    paper = paper_map.get("paper")
    if not isinstance(paper, dict):
        errors.append("top-level 'paper' must be an object")
    else:
        for field in ("title", "source"):
            if not str(paper.get(field, "")).strip():
                errors.append(f"paper.{field} is required")

    units = paper_map.get("units")
    if not isinstance(units, list) or not units:
        errors.append("top-level 'units' must be a non-empty list")
        return errors, warnings, counts

    article_ids = set(SOURCE_ID_RE.findall(article))
    seen_ids: set[str] = set()

    for index, unit in enumerate(units):
        label = f"units[{index}]"
        if not isinstance(unit, dict):
            errors.append(f"{label} must be an object")
            continue

        unit_id = str(unit.get("id", "")).strip()
        kind = str(unit.get("kind", "")).strip()
        source_ref = str(unit.get("source_ref", "")).strip()
        status = str(unit.get("status", "")).strip()
        notes = str(unit.get("notes", "")).strip()

        if not unit_id:
            errors.append(f"{label}.id is required")
        elif not ID_RE.fullmatch(unit_id):
            errors.append(
                f"{label}.id '{unit_id}' must contain only letters, digits, and hyphens"
            )
        elif unit_id in seen_ids:
            errors.append(f"duplicate unit id: {unit_id}")
        else:
            seen_ids.add(unit_id)

        if not kind:
            errors.append(f"{label}.kind is required")
        if not source_ref:
            errors.append(f"{label}.source_ref is required")
        if status not in ALL_STATUSES:
            errors.append(
                f"{label}.status '{status}' must be one of {sorted(ALL_STATUSES)}"
            )
        elif status == "pending":
            errors.append(f"{unit_id or label} is still pending")
        else:
            counts[status] += 1

        if status in {"unavailable", "not-applicable"} and not notes:
            errors.append(f"{unit_id or label} with status '{status}' requires notes")

        if unit_id and unit_id not in article_ids:
            errors.append(
                f"{unit_id} has no matching data-source-id in the article"
            )

    extra_ids = sorted(article_ids - seen_ids)
    if extra_ids:
        preview = ", ".join(extra_ids[:10])
        suffix = " ..." if len(extra_ids) > 10 else ""
        warnings.append(
            f"article contains {len(extra_ids)} data-source-id value(s) absent from map: "
            f"{preview}{suffix}"
        )

    if "<html" not in article.lower():
        warnings.append("article does not appear to be a complete HTML document")

    counts["total"] = len(units)
    counts["article_ids"] = len(article_ids)
    return errors, warnings, counts


def run_self_test() -> int:
    good_map = {
        "paper": {"title": "Demo", "source": "local.pdf"},
        "units": [
            {
                "id": "sec-1",
                "kind": "section",
                "source_ref": "Section 1",
                "status": "covered",
                "notes": "",
            },
            {
                "id": "supp-a",
                "kind": "supplement",
                "source_ref": "Supplement A",
                "status": "unavailable",
                "notes": "The supplementary file was not published.",
            },
        ],
    }
    good_html = (
        '<html><section data-source-id="sec-1"></section>'
        '<section data-source-id="supp-a"></section></html>'
    )
    errors, _, _ = validate(good_map, good_html)
    if errors:
        print("self-test failed on valid fixture:", *errors, sep="\n- ")
        return 1

    bad_map = {
        "paper": {"title": "", "source": ""},
        "units": [
            {
                "id": "bad id",
                "kind": "",
                "source_ref": "",
                "status": "pending",
                "notes": "",
            }
        ],
    }
    errors, _, _ = validate(bad_map, "<html></html>")
    if len(errors) < 5:
        print("self-test failed to detect invalid fixture")
        return 1

    print("self-test passed")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate paper-map coverage against an HTML article."
    )
    parser.add_argument("paper_map", nargs="?", type=Path)
    parser.add_argument("article", nargs="?", type=Path)
    parser.add_argument(
        "--self-test", action="store_true", help="run built-in tests and exit"
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.self_test:
        return run_self_test()
    if args.paper_map is None or args.article is None:
        print("error: paper_map and article are required", file=sys.stderr)
        return 2

    try:
        paper_map = json.loads(args.paper_map.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: cannot read paper map: {exc}", file=sys.stderr)
        return 2

    try:
        article = args.article.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"error: cannot read article: {exc}", file=sys.stderr)
        return 2

    if not isinstance(paper_map, dict):
        print("error: paper map root must be a JSON object", file=sys.stderr)
        return 2

    errors, warnings, counts = validate(paper_map, article)
    print(
        "coverage:",
        f"total={counts['total']}",
        f"covered={counts['covered']}",
        f"unavailable={counts['unavailable']}",
        f"not-applicable={counts['not-applicable']}",
        f"article-ids={counts['article_ids']}",
    )
    for warning in warnings:
        print(f"warning: {warning}")
    for error in errors:
        print(f"error: {error}", file=sys.stderr)

    if errors:
        print(f"FAILED with {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("PASS: every paper-map unit is represented in the article")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
