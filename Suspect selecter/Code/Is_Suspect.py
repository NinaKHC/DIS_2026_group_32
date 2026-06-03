from __future__ import annotations

import random
import math
from typing import Any

import streamlit as st


GUILTY_SUSPECT_KEY = "guilty_suspect"
UNTRUTHFUL_PERSON_IDS_KEY = "untruthful_person_ids"


def setup_guilty_suspect(
    selected_characters: list[dict[str, Any]],
) -> dict[str, Any]:
    if not selected_characters:
        raise ValueError("Cannot choose a guilty suspect because selected_characters is empty.")

    if GUILTY_SUSPECT_KEY not in st.session_state:
        st.session_state[GUILTY_SUSPECT_KEY] = random.choice(selected_characters)

    guilty_suspect = st.session_state[GUILTY_SUSPECT_KEY]
    guilty_id = guilty_suspect.get("id")

    for character in selected_characters:
        if guilty_id is not None and character.get("id") is not None:
            character["is_suspect"] = character.get("id") == guilty_id
        else:
            character["is_suspect"] = character == guilty_suspect

    return guilty_suspect


def get_guilty_suspect() -> dict[str, Any] | None:
    return st.session_state.get(GUILTY_SUSPECT_KEY)


def is_guilty_suspect(character: dict[str, Any]) -> bool:
    guilty_suspect = get_guilty_suspect()

    if guilty_suspect is None:
        return False

    character_id = character.get("id")
    guilty_id = guilty_suspect.get("id")

    if character_id is not None and guilty_id is not None:
        return character_id == guilty_id

    return character == guilty_suspect


def setup_untruthful_characters(
    selected_characters: list[dict[str, Any]],
    min_percent: float = 0.15,
    max_percent: float = 0.20,
) -> list[int]:
    if not selected_characters:
        return []

    min_count = max(1, math.ceil(len(selected_characters) * min_percent))
    max_count = max(min_count, math.floor(len(selected_characters) * max_percent))

    if UNTRUTHFUL_PERSON_IDS_KEY not in st.session_state:
        count = random.randint(min_count, max_count)
        selected = random.sample(selected_characters, count)
        st.session_state[UNTRUTHFUL_PERSON_IDS_KEY] = [
            character.get("id")
            for character in selected
            if character.get("id") is not None
        ]

    untruthful_ids = set(st.session_state[UNTRUTHFUL_PERSON_IDS_KEY])
    for character in selected_characters:
        character["truthfull"] = character.get("id") not in untruthful_ids

    return list(st.session_state[UNTRUTHFUL_PERSON_IDS_KEY])


def reset_untruthful_characters() -> None:
    st.session_state.pop(UNTRUTHFUL_PERSON_IDS_KEY, None)


def reset_guilty_suspect() -> None:
    st.session_state.pop(GUILTY_SUSPECT_KEY, None)
