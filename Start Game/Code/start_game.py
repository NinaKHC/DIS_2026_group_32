from __future__ import annotations

import sys
from pathlib import Path
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[2]

WITNESS_OVERVIEW_CODE_DIR = PROJECT_ROOT / "Witness file" / "Code"
CHAR_RANDOMIZER_CODE_DIR = PROJECT_ROOT / "Char Randomizer" / "Code"
SUSPECT_SELECTER_CODE_DIR = PROJECT_ROOT / "Suspect selecter" / "Code"
DATABASE_CODE_DIR = PROJECT_ROOT / "Database" / "Code"


def _add_project_import_paths() -> None:
    for path in [
        WITNESS_OVERVIEW_CODE_DIR,
        CHAR_RANDOMIZER_CODE_DIR,
        SUSPECT_SELECTER_CODE_DIR,
        DATABASE_CODE_DIR,
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
    setup_untruthful_characters,
    reset_guilty_suspect,
    reset_untruthful_characters,
)

try:
    from database_helpers import (
        get_persons,
        reset_guilty_suspect_flags,
        reset_truthfull_flags,
        set_guilty_suspect_flag,
        set_untruthful_flags,
    )
except ImportError:
    def get_persons(fallback: list[dict] | None = None) -> list[dict]:
        return fallback or []

    def reset_guilty_suspect_flags() -> None:
        return None

    def reset_truthfull_flags() -> None:
        return None

    def set_guilty_suspect_flag(person_id: int) -> None:
        return None

    def set_untruthful_flags(person_ids: list[int]) -> None:
        return None


GAME_STARTED_KEY = "game_started"
PAGE_KEY = "page"
GAME_NUMBER_KEY = "game_number"
CHARACTERS_PER_GAME = 25


def start_new_game(start_page: str = "witnesses") -> None:
    reset_current_game_state(keep_page=True)
    reset_guilty_suspect_flags()
    reset_truthfull_flags()

    all_persons = [
        {**person, "is_suspect": False, "truthfull": True}
        for person in get_persons(PERSONS)
    ]

    selected_characters = setup_random_characters(
        all_persons,
        number_of_characters=CHARACTERS_PER_GAME,
    )
    guilty_suspect = setup_guilty_suspect(selected_characters)
    untruthful_ids = setup_untruthful_characters(selected_characters)
    guilty_id = guilty_suspect.get("id")

    if guilty_id is not None:
        set_guilty_suspect_flag(int(guilty_id))
    set_untruthful_flags([int(person_id) for person_id in untruthful_ids])

    st.session_state[GAME_STARTED_KEY] = True
    st.session_state[PAGE_KEY] = start_page
    st.session_state[GAME_NUMBER_KEY] = st.session_state.get(GAME_NUMBER_KEY, 0) + 1


def continue_game(default_page: str = "witnesses") -> None:
    if not is_game_started():
        return

    if st.session_state.get(PAGE_KEY) in [None, "", "start_screen"]:
        st.session_state[PAGE_KEY] = default_page


def is_game_started() -> bool:
    return bool(st.session_state.get(GAME_STARTED_KEY, False))


def reset_current_game_state(keep_page: bool = False) -> None:
    reset_selected_characters()
    reset_guilty_suspect()
    reset_untruthful_characters()

    keys_to_remove = [
        GAME_STARTED_KEY,
        "wo_suspicious",
        "wo_selected",
        "suspect_index",
        "witness_index",
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
