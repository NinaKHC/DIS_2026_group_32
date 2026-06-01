from __future__ import annotations

import re
from datetime import date
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE_SQL_PATH = PROJECT_ROOT / "database.sql"


def _format_display_date(raw_date: str) -> str:
    try:
        parsed = date.fromisoformat(raw_date)
    except ValueError:
        return raw_date
    return parsed.strftime("%d/%m/%Y")


def _load_birth_details_from_sql() -> dict[int, dict[str, str]]:
    if not DATABASE_SQL_PATH.exists():
        return {}

    sql = DATABASE_SQL_PATH.read_text(encoding="utf-8")
    details: dict[int, dict[str, str]] = {}

    for match in re.finditer(r"INSERT\s+INTO\s+Person\s+VALUES\s*\((.*?)\);", sql, re.DOTALL | re.IGNORECASE):
        block = match.group(1)
        person_id_match = re.match(r"\s*(\d+)\s*,", block)
        birth_match = re.search(
            r",\s*(\d+)\s*,\s*'(\d{4}-\d{2}-\d{2})'\s*,\s*(TRUE|FALSE)\s*$",
            block,
            re.IGNORECASE,
        )

        if not person_id_match or not birth_match:
            continue

        person_id = int(person_id_match.group(1))
        details[person_id] = {
            "age": birth_match.group(1),
            "date_of_birth": _format_display_date(birth_match.group(2)),
        }

    return details


PERSON_BIRTH_DETAILS = _load_birth_details_from_sql()


def get_person_birth_details(person_id: int | None) -> dict[str, str]:
    if person_id is None:
        return {"age": "", "date_of_birth": ""}
    return PERSON_BIRTH_DETAILS.get(person_id, {"age": "", "date_of_birth": ""})
