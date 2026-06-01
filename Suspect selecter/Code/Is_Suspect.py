"""
Is_Suspect.py

This file selects 1 guilty suspect from the 10 random characters.

Expected use:
    from Is_Suspect import setup_guilty_suspect, get_guilty_suspect, is_guilty_suspect

    guilty = setup_guilty_suspect(selected_characters)

The guilty suspect is stored in st.session_state so it does not change every time
Streamlit reruns the page.
"""

from __future__ import annotations

import random
from typing import Any

import streamlit as st


GUILTY_SUSPECT_KEY = "guilty_suspect"


def setup_guilty_suspect(
    selected_characters: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Selects one guilty suspect from the selected random characters.

    This function only selects a new guilty suspect if no guilty suspect already exists.
    That means the guilty suspect stays the same while the game is running.

    Args:
        selected_characters:
            The 10 random characters selected by Random_char_selector.py.

    Returns:
        The guilty suspect.
    """
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
    """
    Returns the currently selected guilty suspect.

    Returns None if setup_guilty_suspect has not been called yet.
    """
    return st.session_state.get(GUILTY_SUSPECT_KEY)


def is_guilty_suspect(character: dict[str, Any]) -> bool:
    """
    Checks whether a given character is the guilty suspect.

    The comparison uses the character "id" if possible.
    If there is no id, it falls back to comparing the whole dictionary.
    """
    guilty_suspect = get_guilty_suspect()

    if guilty_suspect is None:
        return False

    character_id = character.get("id")
    guilty_id = guilty_suspect.get("id")

    if character_id is not None and guilty_id is not None:
        return character_id == guilty_id

    return character == guilty_suspect


def reset_guilty_suspect() -> None:
    """
    Removes the guilty suspect from session_state.

    Call this when starting a new game.
    """
    st.session_state.pop(GUILTY_SUSPECT_KEY, None)
