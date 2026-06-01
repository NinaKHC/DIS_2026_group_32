"""
Random_char_selector.py

This file selects 10 random characters from all available characters.

Expected use:
    from Random_char_selector import setup_random_characters, get_selected_characters, reset_selected_characters

    setup_random_characters(PERSONS)
    selected = get_selected_characters()

The selection is stored in st.session_state so it does not change every time
Streamlit reruns the page.
"""

from __future__ import annotations

import random
from typing import Any

import streamlit as st


SELECTED_CHARACTERS_KEY = "selected_random_characters"


def setup_random_characters(
    characters: list[dict[str, Any]],
    number_of_characters: int = 10,
) -> list[dict[str, Any]]:
    """
    Selects number_of_characters random characters and stores them in Streamlit session_state.

    This function only selects new characters if no selection already exists.
    That means the selected 10 characters stay the same while the game is running.

    Args:
        characters:
            A list of all possible character dictionaries.
            Each character should preferably have a unique "id".
        number_of_characters:
            How many characters should be selected. Default is 10.

    Returns:
        The selected characters.
    """
    if len(characters) < number_of_characters:
        raise ValueError(
            f"Cannot select {number_of_characters} characters from only {len(characters)} characters."
        )

    if SELECTED_CHARACTERS_KEY not in st.session_state:
        st.session_state[SELECTED_CHARACTERS_KEY] = random.sample(
            characters,
            number_of_characters,
        )

    return st.session_state[SELECTED_CHARACTERS_KEY]


def get_selected_characters() -> list[dict[str, Any]]:
    """
    Returns the currently selected random characters.

    Returns an empty list if setup_random_characters has not been called yet.
    """
    return st.session_state.get(SELECTED_CHARACTERS_KEY, [])


def reset_selected_characters() -> None:
    """
    Removes the selected characters from session_state.

    Call this when starting a new game.
    """
    st.session_state.pop(SELECTED_CHARACTERS_KEY, None)
