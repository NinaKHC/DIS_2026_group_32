from __future__ import annotations

import random
from typing import Any

import streamlit as st


SELECTED_CHARACTERS_KEY = "selected_random_characters"


def setup_random_characters(
    characters: list[dict[str, Any]],
    number_of_characters: int = 25,
) -> list[dict[str, Any]]:
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
    return st.session_state.get(SELECTED_CHARACTERS_KEY, [])


def reset_selected_characters() -> None:
    st.session_state.pop(SELECTED_CHARACTERS_KEY, None)
