from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

import streamlit as st
from sqlalchemy import create_engine, text


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SQL_FILE_PATH = PROJECT_ROOT / "database.sql"

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/streamlit_db",
)
SHOW_DATABASE_ERRORS = os.getenv("SHOW_DATABASE_ERRORS", "").lower() in {"1", "true", "yes"}


@st.cache_resource
def _engine():
    return create_engine(DATABASE_URL)


def _handle_database_error(context: str, error: Exception) -> None:
    errors = st.session_state.setdefault("_database_errors", [])
    errors.append(f"{context}: {error}")
    st.session_state["_database_errors"] = errors[-5:]

    if SHOW_DATABASE_ERRORS:
        st.warning(f"Database unavailable: {context}")


def _format_time(value: Any) -> str:
    return value.strftime("%H:%M") if value else ""


def _format_date(value: Any) -> str:
    return value.strftime("%d/%m/%Y") if value else ""


def _format_sql_date_text(value: str) -> str:
    match = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", str(value or "").strip())
    if not match:
        return str(value or "")

    year, month, day = match.groups()
    return f"{day}/{month}/{year}"


def _clean_label(value: Any) -> str:
    text_value = str(value or "").strip()
    text_value = re.sub(r"(?<=[a-z])(?=brown|grey|green|blonde)", " ", text_value, flags=re.I)

    replacements = {
        "grey brown": "grey-brown",
        "silver grey": "silver-grey",
        "black grey": "black-grey",
        "dark brown": "dark brown",
        "medium brown": "medium brown",
        "light brown": "light brown",
    }
    for old, new in replacements.items():
        text_value = text_value.replace(old, new)

    return text_value[:1].upper() + text_value[1:] if text_value else ""


def _extract_alibi_text(value: str | None) -> str:
    return re.split(r"\bStatement:\s*", value or "", maxsplit=1)[0].strip()


def _read_sql_seed_file() -> str:
    if not SQL_FILE_PATH.exists():
        return ""
    return SQL_FILE_PATH.read_text(encoding="utf-8")


def _parse_insert_blocks(table_name: str) -> list[str]:
    sql_text = _read_sql_seed_file()
    if not sql_text:
        return []

    pattern = rf"INSERT\s+INTO\s+{re.escape(table_name)}(?:\s*\([^)]*\))?\s+VALUES\s*\((.*?)\);"
    return re.findall(pattern, sql_text, flags=re.IGNORECASE | re.DOTALL)


def _split_sql_values(block: str) -> list[str]:
    values: list[str] = []
    current: list[str] = []
    in_string = False
    index = 0

    while index < len(block):
        char = block[index]
        next_char = block[index + 1] if index + 1 < len(block) else ""

        if char == "'" and next_char == "'":
            current.append("'")
            index += 2
            continue

        if char == "'":
            in_string = not in_string
            index += 1
            continue

        if char == "," and not in_string:
            values.append("".join(current).strip())
            current = []
            index += 1
            continue

        current.append(char)
        index += 1

    values.append("".join(current).strip())
    return [value if value.upper() != "NULL" else "" for value in values]


def _parse_persons_from_sql_file() -> list[dict]:
    persons: dict[int, dict] = {}

    for block in _parse_insert_blocks("Person"):
        values = _split_sql_values(block)
        if len(values) < 11:
            continue

        person_id = int(values[0])
        persons[person_id] = {
            "id": person_id,
            "name": values[1],
            "gender": _clean_label(values[2]),
            "hair": _clean_label(values[3]),
            "eyes": _clean_label(values[4]),
            "skin": _clean_label(values[5]),
            "clothing": values[6],
            "role": _clean_label(values[7]),
            "age": values[8],
            "date_of_birth": _format_sql_date_text(values[9]),
            "is_suspect": values[10].upper() == "TRUE",
            "truthfull": values[11].upper() == "TRUE" if len(values) > 11 else True,
            "arrived": "",
            "left": "",
            "works_here": False,
            "statement": "",
            "alibi": "",
        }

    for block in _parse_insert_blocks("Presence"):
        values = _split_sql_values(block)
        if len(values) < 5:
            continue

        person = persons.get(int(values[1]))
        if person:
            person["arrived"] = values[2].split(" ")[-1][:5]
            person["left"] = values[3].split(" ")[-1][:5]
            person["works_here"] = values[4].upper() == "TRUE"

    for block in _parse_insert_blocks("Statement"):
        values = _split_sql_values(block)
        if len(values) < 4:
            continue

        person = persons.get(int(values[1]))
        if person:
            person["statement"] = values[3]

    for block in _parse_insert_blocks("Alibi"):
        values = _split_sql_values(block)
        if len(values) < 2:
            continue

        person = persons.get(int(values[0]))
        if person:
            person["alibi"] = _extract_alibi_text(values[1])

    return [persons[person_id] for person_id in sorted(persons)]


def _parse_stolen_items_from_sql_file() -> list[dict]:
    items = []

    for block in _parse_insert_blocks("Item_stolen"):
        values = _split_sql_values(block)
        if len(values) < 4:
            continue

        item_id = int(values[0])
        items.append({
            "item_id": item_id,
            "description": values[1],
            "time_stolen": values[3].split(" ")[-1][:5],
            "image_filename": f"item{item_id}.png",
        })

    return items


def _parse_access_logs_from_sql_file() -> list[dict]:
    persons = _parse_persons_from_sql_file()
    return [
        {
            "person_id": person["id"],
            "person": person["name"],
            "role": person["role"],
            "arrived": person["arrived"],
            "left": person["left"],
            "works_here": "Yes" if person["works_here"] else "No",
        }
        for person in sorted(persons, key=lambda person: person["arrived"])
    ]


def _parse_timeline_events_from_sql_file() -> list[dict]:
    persons = _parse_persons_from_sql_file()
    events: list[dict] = []

    for person in persons:
        if person["arrived"]:
            events.append({
                "name": person["name"],
                "time": person["arrived"],
                "type": "arrival",
            })
        if person["left"]:
            events.append({
                "name": person["name"],
                "time": person["left"],
                "type": "departure",
            })

    return sorted(events, key=lambda event: event["time"])


def _parse_map_markers_from_sql_file() -> list[dict]:
    markers = []

    for block in _parse_insert_blocks("Map_marker"):
        values = _split_sql_values(block)
        if len(values) < 5:
            continue

        markers.append({
            "id": int(values[0]),
            "name": values[1],
            "x": float(values[2]),
            "y": float(values[3]),
            "color": values[4] or "#cc2200",
            "person_id": int(values[5]) if len(values) > 5 and values[5] else None,
        })

    return markers


PERSONS_QUERY = text("""
    SELECT
        p.person_id,
        p.name,
        p.gender,
        p.hair_color,
        p.eye_color,
        p.skin_color,
        p.clothing,
        p.role,
        p.age,
        p.date_of_birth,
        p.is_suspect,
        p.truthfull,
        pr.arrived_at,
        pr.left_at,
        pr.was_working,
        s.statement_text,
        a.formatted_alibi
    FROM Person p
    LEFT JOIN Presence pr ON pr.person_id = p.person_id
    LEFT JOIN Statement s ON s.person_id = p.person_id
    LEFT JOIN Alibi a ON a.person_id = p.person_id
    ORDER BY p.person_id
""")


def _person_from_database_row(row: Any) -> dict:
    (
        person_id,
        name,
        gender,
        hair_color,
        eye_color,
        skin_color,
        clothing,
        role,
        age,
        date_of_birth,
        is_suspect,
        truthfull,
        arrived_at,
        left_at,
        was_working,
        statement_text,
        formatted_alibi,
    ) = row

    return {
        "id": person_id,
        "name": name or "",
        "gender": _clean_label(gender),
        "hair": _clean_label(hair_color),
        "eyes": _clean_label(eye_color),
        "skin": _clean_label(skin_color),
        "clothing": clothing or "",
        "role": _clean_label(role),
        "age": str(age or ""),
        "date_of_birth": _format_date(date_of_birth),
        "is_suspect": bool(is_suspect),
        "truthfull": bool(truthfull),
        "arrived": _format_time(arrived_at),
        "left": _format_time(left_at),
        "works_here": bool(was_working),
        "statement": statement_text or "",
        "alibi": _extract_alibi_text(formatted_alibi),
    }


@st.cache_data(ttl=60)
def fetch_persons_from_database() -> list[dict]:
    with _engine().connect() as connection:
        rows = connection.execute(PERSONS_QUERY).fetchall()
    return [_person_from_database_row(row) for row in rows]


def get_persons(fallback: list[dict] | None = None) -> list[dict]:
    try:
        persons = fetch_persons_from_database()
        if persons:
            return persons
    except Exception as error:
        _handle_database_error("fetch persons", error)

    persons = _parse_persons_from_sql_file()
    if persons:
        return persons

    return fallback or []


@st.cache_data(ttl=60)
def fetch_stolen_items_from_database(limit: int | None = None) -> list[dict]:
    query = text("""
        SELECT item_id, description, time_of_crime
        FROM Item_stolen
        ORDER BY item_id
    """)

    with _engine().connect() as connection:
        rows = connection.execute(query).fetchall()

    items = [
        {
            "item_id": item_id,
            "description": description or "",
            "time_stolen": _format_time(time_of_crime),
            "image_filename": f"item{item_id}.png",
        }
        for item_id, description, time_of_crime in rows
    ]
    return items[:limit] if limit else items


def get_stolen_items(fallback: list[dict] | None = None, limit: int | None = None) -> list[dict]:
    try:
        items = fetch_stolen_items_from_database(limit=limit)
        if items:
            return items
    except Exception as error:
        _handle_database_error("fetch stolen items", error)

    items = _parse_stolen_items_from_sql_file()
    if items:
        return items[:limit] if limit else items

    return fallback or []


@st.cache_data(ttl=60)
def fetch_evidence_items_from_database() -> list[dict]:
    query = text("""
        SELECT evidence_id, name, description, image_filename
        FROM Evidence
        ORDER BY evidence_id
    """)

    with _engine().connect() as connection:
        rows = connection.execute(query).fetchall()

    return [
        {
            "id": evidence_id,
            "name": name or "",
            "description": description or "",
            "image_filename": image_filename or "",
        }
        for evidence_id, name, description, image_filename in rows
    ]


def get_evidence_items(fallback: list[dict] | None = None) -> list[dict]:
    try:
        evidence = fetch_evidence_items_from_database()
        if evidence:
            return evidence
    except Exception as error:
        _handle_database_error("fetch evidence items", error)

    return fallback or []


@st.cache_data(ttl=60)
def fetch_access_logs_from_database() -> list[dict]:
    query = text("""
        SELECT person_id, person, role, arrived_at, left_at, was_working
        FROM Access_log_view
        ORDER BY arrived_at
    """)

    with _engine().connect() as connection:
        rows = connection.execute(query).fetchall()

    return [
        {
            "person_id": person_id,
            "person": person or "",
            "role": _clean_label(role),
            "arrived": _format_time(arrived_at),
            "left": _format_time(left_at),
            "works_here": "Yes" if was_working else "No",
        }
        for person_id, person, role, arrived_at, left_at, was_working in rows
    ]


def get_access_logs(fallback: list[dict] | None = None) -> list[dict]:
    try:
        access_logs = fetch_access_logs_from_database()
        if access_logs:
            return access_logs
    except Exception as error:
        _handle_database_error("fetch access logs", error)

    access_logs = _parse_access_logs_from_sql_file()
    if access_logs:
        return access_logs

    return fallback or []


@st.cache_data(ttl=60)
def fetch_timeline_events_from_database() -> list[dict]:
    query = text("""
        SELECT name, event_time, event_type
        FROM Timeline_event_view
        WHERE event_time IS NOT NULL
        ORDER BY event_time
    """)

    with _engine().connect() as connection:
        rows = connection.execute(query).fetchall()

    return [
        {
            "name": name or "",
            "time": _format_time(event_time),
            "type": event_type or "event",
        }
        for name, event_time, event_type in rows
    ]


def get_timeline_events(fallback: list[dict] | None = None) -> list[dict]:
    try:
        events = fetch_timeline_events_from_database()
        if events:
            return events
    except Exception as error:
        _handle_database_error("fetch timeline events", error)

    events = _parse_timeline_events_from_sql_file()
    if events:
        return events

    return fallback or []


@st.cache_data(ttl=60)
def fetch_map_markers_from_database() -> list[dict]:
    query = text("""
        SELECT marker_id, name, x_percent, y_percent, color, person_id
        FROM Map_marker_view
        ORDER BY marker_id
    """)

    with _engine().connect() as connection:
        rows = connection.execute(query).fetchall()

    return [
        {
            "id": marker_id,
            "name": name or "",
            "x": float(x_percent),
            "y": float(y_percent),
            "color": color or "#cc2200",
            "person_id": person_id,
        }
        for marker_id, name, x_percent, y_percent, color, person_id in rows
    ]


def get_map_markers(fallback: list[dict] | None = None) -> list[dict]:
    try:
        markers = fetch_map_markers_from_database()
        if markers:
            return markers
    except Exception as error:
        _handle_database_error("fetch map markers", error)

    markers = _parse_map_markers_from_sql_file()
    if markers:
        return markers

    return fallback or []


CREATE_GAME_STATE_TABLES = [
    """
    CREATE TABLE IF NOT EXISTS Player_suspicion (
        game_id INTEGER,
        person_id INTEGER,
        is_suspicious BOOLEAN NOT NULL DEFAULT FALSE,
        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (game_id, person_id),
        FOREIGN KEY (person_id) REFERENCES Person(person_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Arrest_guess (
        game_id INTEGER PRIMARY KEY,
        person_id INTEGER,
        is_correct BOOLEAN,
        guessed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (person_id) REFERENCES Person(person_id)
    )
    """,
]


UPSERT_SUSPICION_QUERY = text("""
    INSERT INTO Player_suspicion (game_id, person_id, is_suspicious)
    VALUES (:game_id, :person_id, :is_suspicious)
    ON CONFLICT (game_id, person_id)
    DO UPDATE SET
        is_suspicious = EXCLUDED.is_suspicious,
        updated_at = CURRENT_TIMESTAMP
""")


GET_SUSPICIOUS_IDS_QUERY = text("""
    SELECT person_id
    FROM Player_suspicion
    WHERE game_id = :game_id
      AND is_suspicious = TRUE
    ORDER BY person_id
""")


UPSERT_ARREST_GUESS_QUERY = text("""
    INSERT INTO Arrest_guess (game_id, person_id, is_correct)
    VALUES (:game_id, :person_id, :is_correct)
    ON CONFLICT (game_id)
    DO UPDATE SET
        person_id = EXCLUDED.person_id,
        is_correct = EXCLUDED.is_correct,
        guessed_at = CURRENT_TIMESTAMP
""")


RESET_GUILTY_SUSPECT_QUERY = text("""
    UPDATE Person
    SET is_suspect = FALSE
""")


SET_GUILTY_SUSPECT_QUERY = text("""
    UPDATE Person
    SET is_suspect = CASE
        WHEN person_id = :person_id THEN TRUE
        ELSE FALSE
    END
""")


RESET_TRUTHFULL_FLAGS_QUERY = text("""
    UPDATE Person
    SET truthfull = TRUE
""")


SET_UNTRUTHFUL_FLAGS_QUERY = text("""
    UPDATE Person
    SET truthfull = CASE
        WHEN person_id = ANY(:person_ids) THEN FALSE
        ELSE TRUE
    END
""")


def ensure_game_tables() -> None:
    with _engine().begin() as connection:
        for statement in CREATE_GAME_STATE_TABLES:
            connection.execute(text(statement))


def set_suspicious_flag(game_id: int, person_id: int, is_suspicious: bool) -> None:
    try:
        ensure_game_tables()
        with _engine().begin() as connection:
            connection.execute(UPSERT_SUSPICION_QUERY, {
                "game_id": game_id,
                "person_id": person_id,
                "is_suspicious": is_suspicious,
            })
    except Exception as error:
        _handle_database_error("save suspicious flag", error)


def get_suspicious_person_ids(game_id: int) -> set[int]:
    try:
        ensure_game_tables()
        with _engine().connect() as connection:
            rows = connection.execute(GET_SUSPICIOUS_IDS_QUERY, {"game_id": game_id}).fetchall()
        return {int(row[0]) for row in rows}
    except Exception as error:
        _handle_database_error("fetch suspicious flags", error)
        return set()


def reset_guilty_suspect_flags() -> None:
    try:
        with _engine().begin() as connection:
            connection.execute(RESET_GUILTY_SUSPECT_QUERY)
        fetch_persons_from_database.clear()
    except Exception as error:
        _handle_database_error("reset guilty suspect flags", error)


def set_guilty_suspect_flag(person_id: int) -> None:
    try:
        with _engine().begin() as connection:
            connection.execute(SET_GUILTY_SUSPECT_QUERY, {"person_id": person_id})
        fetch_persons_from_database.clear()
    except Exception as error:
        _handle_database_error("set guilty suspect flag", error)


def reset_truthfull_flags() -> None:
    try:
        with _engine().begin() as connection:
            connection.execute(RESET_TRUTHFULL_FLAGS_QUERY)
        fetch_persons_from_database.clear()
    except Exception as error:
        _handle_database_error("reset truthfull flags", error)


def set_untruthful_flags(person_ids: list[int]) -> None:
    try:
        with _engine().begin() as connection:
            if person_ids:
                connection.execute(SET_UNTRUTHFUL_FLAGS_QUERY, {"person_ids": person_ids})
            else:
                connection.execute(RESET_TRUTHFULL_FLAGS_QUERY)
        fetch_persons_from_database.clear()
    except Exception as error:
        _handle_database_error("set untruthful flags", error)


def save_arrest_guess(game_id: int, person_id: int, is_correct: bool) -> None:
    try:
        ensure_game_tables()
        with _engine().begin() as connection:
            connection.execute(UPSERT_ARREST_GUESS_QUERY, {
                "game_id": game_id,
                "person_id": person_id,
                "is_correct": is_correct,
            })
    except Exception as error:
        _handle_database_error("save arrest guess", error)
