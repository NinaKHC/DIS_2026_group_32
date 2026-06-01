r"""
start_game.py

Central controller for starting, checking, and resetting a game session.

Place this file here:
C:/Users/Bruger/Downloads/DIS/Projekt/DIS_2026_group_32/Start Game/Code/start_game.py
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[2]

WITNESS_OVERVIEW_CODE_DIR = PROJECT_ROOT / "Witness file" / "Code"
CHAR_RANDOMIZER_CODE_DIR = PROJECT_ROOT / "Char Randomizer" / "Code"
SUSPECT_SELECTER_CODE_DIR = PROJECT_ROOT / "Suspect selecter" / "Code"


def _add_project_import_paths() -> None:
    for path in [
        WITNESS_OVERVIEW_CODE_DIR,
        CHAR_RANDOMIZER_CODE_DIR,
        SUSPECT_SELECTER_CODE_DIR,
    ]:
        path_string = str(path)
        if path_string not in sys.path:
            sys.path.append(path_string)


_add_project_import_paths()

from witness_overview import PERSONS
from Random_char_selector import (
    setup_random_characters,
    get_selected_characters,
    reset_selected_characters,
)
from Is_Suspect import (
    setup_guilty_suspect,
    get_guilty_suspect,
    is_guilty_suspect,
    reset_guilty_suspect,
)


GAME_STARTED_KEY = "game_started"
PAGE_KEY = "page"
GAME_NUMBER_KEY = "game_number"


def start_new_game(start_page: str = "witnesses") -> None:
    """
    Starts a completely new game.
    """
    reset_current_game_state(keep_page=True)

    selected_characters = setup_random_characters(
        PERSONS,
        number_of_characters=10,
    )
    guilty_suspect = setup_guilty_suspect(selected_characters)

    st.session_state[GAME_STARTED_KEY] = True
    st.session_state[PAGE_KEY] = start_page
    st.session_state[GAME_NUMBER_KEY] = st.session_state.get(GAME_NUMBER_KEY, 0) + 1

    # Debug values. Remove later if you do not need them.
    st.session_state["debug_selected_character_ids"] = [
        character.get("id")
        for character in selected_characters
    ]
    st.session_state["debug_selected_character_names"] = [
        character.get("name", "")
        for character in selected_characters
    ]
    st.session_state["debug_guilty_suspect_id"] = guilty_suspect.get("id")
    st.session_state["debug_guilty_suspect_name"] = guilty_suspect.get("name", "")


def continue_game(default_page: str = "witnesses") -> None:
    """
    Sends the player back into an already started game.
    """
    if not is_game_started():
        return

    if st.session_state.get(PAGE_KEY) in [None, "", "start_screen"]:
        st.session_state[PAGE_KEY] = default_page


def is_game_started() -> bool:
    return bool(st.session_state.get(GAME_STARTED_KEY, False))


def get_game_characters() -> list[dict[str, Any]]:
    return get_selected_characters()


def get_current_guilty_suspect() -> dict[str, Any] | None:
    return get_guilty_suspect()


def check_guess(character: dict[str, Any]) -> bool:
    return is_guilty_suspect(character)


def _character_photo_path(character: dict[str, Any] | None) -> str | None:
    if not character:
        return None

    character_id = character.get("id")
    if character_id is None:
        return character.get("photo")

    photo_path = PROJECT_ROOT / "Characters" / f"Char_{character_id}.png"
    if photo_path.exists():
        return str(photo_path)

    return character.get("photo")


def go_to_win_or_lose_page(character: dict[str, Any]) -> None:
    guilty = get_guilty_suspect()
    is_correct = check_guess(character)

    st.session_state["result_is_correct"] = is_correct
    st.session_state["result_arrested_name"] = character.get("name", character.get("full_name", ""))
    st.session_state["result_arrested_photo"] = _character_photo_path(character)
    st.session_state["result_guilty_name"] = (
        guilty.get("name", guilty.get("full_name", "")) if guilty else ""
    )
    st.session_state["result_guilty_photo"] = _character_photo_path(guilty)
    st.session_state[PAGE_KEY] = "you_win" if is_correct else "you_lose"


def reset_current_game_state(keep_page: bool = False) -> None:
    reset_selected_characters()
    reset_guilty_suspect()

    keys_to_remove = [
        GAME_STARTED_KEY,
        "wo_suspicious",
        "wo_selected",
        "suspect_index",
        "witness_index",
        "debug_selected_character_ids",
        "debug_selected_character_names",
        "debug_guilty_suspect_id",
        "debug_guilty_suspect_name",
        "result_is_correct",
        "result_arrested_name",
        "result_arrested_photo",
        "result_guilty_name",
        "result_guilty_photo",
        "ar_view",
        "ar_selected",
    ]

    for key in keys_to_remove:
        st.session_state.pop(key, None)

    if not keep_page:
        st.session_state[PAGE_KEY] = "start_screen"


def show_debug_game_state() -> None:
    st.write("Game started:", is_game_started())
    st.write("Selected character IDs:", st.session_state.get("debug_selected_character_ids", []))
    st.write("Selected character names:", st.session_state.get("debug_selected_character_names", []))
    st.write("Guilty suspect ID:", st.session_state.get("debug_guilty_suspect_id"))
    st.write("Guilty suspect name:", st.session_state.get("debug_guilty_suspect_name"))
