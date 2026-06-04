import importlib.util
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import streamlit as st
from sqlalchemy import create_engine, inspect


st.set_page_config(
    page_title="Jewel Heist Database",
    layout="wide",
    initial_sidebar_state="collapsed",
)


PROJECT_ROOT = Path(__file__).resolve().parent


@dataclass(frozen=True)
class PageConfig:
    key: str
    title: str
    folder_names: tuple[str, ...]
    module_names: tuple[str, ...]
    function_names: tuple[str, ...]


PAGE_CONFIGS: dict[str, PageConfig] = {
    "start_screen": PageConfig(
        key="start_screen",
        title="Start Screen",
        folder_names=("Start Screen", "Start screen", "start_screen"),
        module_names=("start_screen.py",),
        function_names=("show_start_screen",),
    ),

    "intro": PageConfig(
        key="intro",
        title="Intro",
        folder_names=("Intro", "intro"),
        module_names=("intro.py",),
        function_names=("show_intro",),
    ),

    "main_menu": PageConfig(
        key="main_menu",
        title="Main Menu",
        folder_names=("Main Menu", "Main menu", "main_menu"),
        module_names=("main_menu.py",),
        function_names=("show_main_menu",),
    ),

    "case_overview": PageConfig(
        key="case_overview",
        title="Case Overview",
        folder_names=("Case Overview", "case_overview"),
        module_names=("case_overview.py",),
        function_names=("show_case_overview",),
    ),

    "crime_scene": PageConfig(
        key="crime_scene",
        title="Crime Scene",
        folder_names=("Crime scene", "Crime Scene", "crime_scene"),
        module_names=("crime_scene.py",),
        function_names=("show_crime_scene",),
    ),

    "witnesses": PageConfig(
        key="witnesses",
        title="Witnesses",
        folder_names=("Witness file", "Witness File", "Witnesses", "witnesses"),
        module_names=("witness_overview.py", "witness_file.py", "witnesses.py"),
        function_names=("show_witness_overview", "show_witnesses", "show_witness_file"),
    ),

    "witness_file": PageConfig(
        key="witness_file",
        title="Witness File",
        folder_names=("Witness file", "Witness File", "Witnesses", "witnesses"),
        module_names=("witness_file.py", "witnesses.py"),
        function_names=("show_witnesses", "show_witness_file"),
    ),

    "witness_search": PageConfig(
        key="witness_search",
        title="Witness Search",
        folder_names=("Witness file", "Witness File", "Witnesses", "witnesses"),
        module_names=("witness_search.py",),
        function_names=("show_witness_search",),
    ),

    "suspects": PageConfig(
        key="suspects",
        title="Suspects",
        folder_names=("Suspects", "suspects"),
        module_names=("suspects.py",),
        function_names=("show_suspects",),
    ),

    "evidence": PageConfig(
        key="evidence",
        title="Evidence",
        folder_names=("Evidens", "Evidence", "evidence"),
        module_names=("evidence.py", "evidens.py"),
        function_names=("show_evidence", "show_evidens"),
    ),

    "stolen_items": PageConfig(
        key="stolen_items",
        title="Stolen Items",
        folder_names=("Stolen items", "Stolen Items", "stolen_items"),
        module_names=("stolen_items.py",),
        function_names=("show_stolen_items",),
    ),

    "locations": PageConfig(
        key="locations",
        title="Locations",
        folder_names=("Map", "Locations", "locations", "map"),
        module_names=("map.py", "locations.py"),
        function_names=("show_locations", "show_map"),
    ),

    "timeline": PageConfig(
        key="timeline",
        title="Timeline",
        folder_names=("Timeline", "timeline"),
        module_names=("timeline.py",),
        function_names=("show_timeline",),
    ),

    "surveillance_media": PageConfig(
        key="surveillance_media",
        title="Surveillance & Media",
        folder_names=("Surveillance", "Surveillance Media", "surveillance_media"),
        module_names=("surveillance.py", "surveillance_media.py"),
        function_names=("show_surveillance_media", "show_surveillance"),
    ),

    "access_logs": PageConfig(
        key="access_logs",
        title="Access Logs",
        folder_names=("Access Logs", "access_logs"),
        module_names=("access_logs.py",),
        function_names=("show_access_logs",),
    ),

    "notes_connections": PageConfig(
        key="notes_connections",
        title="Notes / Connections",
        folder_names=("Notes Connections", "Notes and Connections", "notes_connections"),
        module_names=("notes_connections.py",),
        function_names=("show_notes_connections",),
    ),

    "arrest_suspect": PageConfig(
        key="arrest_suspect",
        title="Arrest the Suspect",
        folder_names=("Arrest person", "Arrest Person", "Arrest Suspect", "arrest_suspect"),
        module_names=("arrest_person.py", "arrest_suspect.py"),
        function_names=("show_arrest_suspect", "show_arrest_person"),
    ),

    "you_win": PageConfig(
        key="you_win",
        title="You Win",
        folder_names=("YouWin", "you_win"),
        module_names=("you_win.py",),
        function_names=("show_you_win",),
    ),

    "you_lose": PageConfig(
        key="you_lose",
        title="You Lose",
        folder_names=("YouLose", "you_lose"),
        module_names=("you_lose.py",),
        function_names=("show_you_lose",),
    ),

    "characters": PageConfig(
        key="characters",
        title="Characters",
        folder_names=("Characters", "characters"),
        module_names=("characters.py",),
        function_names=("show_characters",),
    ),

    "exit": PageConfig(
        key="exit",
        title="Exit",
        folder_names=("Exit Funktion", "Exit Function", "exit_function"),
        module_names=("exit_screen.py", "exit_function.py"),
        function_names=("show_exit_screen", "show_exit_function"),
    ),
}


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/streamlit_db",
)


def go_to_page(page_name: str) -> None:
    st.session_state["page"] = page_name
    st.rerun()


def find_page_module(config: PageConfig) -> Path | None:
    for folder_name in config.folder_names:
        code_dir = PROJECT_ROOT / folder_name / "Code"

        for module_name in config.module_names:
            module_path = code_dir / module_name

            if module_path.exists():
                return module_path

    return None


def load_page_function(config: PageConfig) -> Callable[[], None] | None:
    module_path = find_page_module(config)

    if module_path is None:
        return None

    module_id = f"dynamic_page_{config.key}"

    spec = importlib.util.spec_from_file_location(module_id, module_path)

    if spec is None or spec.loader is None:
        return None

    module = importlib.util.module_from_spec(spec)

    code_dir = str(module_path.parent)

    if code_dir not in sys.path:
        sys.path.insert(0, code_dir)

    spec.loader.exec_module(module)

    for function_name in config.function_names:
        page_function = getattr(module, function_name, None)

        if callable(page_function):
            return page_function

    return None


def show_database_page() -> None:
    st.title("Database Overview")

    try:
        engine = create_engine(DATABASE_URL)

        with engine.connect():
            st.success("Connected to PostgreSQL database!")

            inspector = inspect(engine)
            tables = inspector.get_table_names()

            st.subheader("Database Tables")

            if tables:
                st.write(f"Found {len(tables)} table(s): {', '.join(tables)}")
            else:
                st.info("No tables found in the database yet.")

    except Exception as error:
        st.error(f"Failed to connect to database: {error}")

    if st.button("Back to Main Menu"):
        go_to_page("main_menu")


def show_missing_page(config: PageConfig) -> None:
    st.title(config.title)
    st.info("This page is not available.")

    if st.button("Back to Main Menu"):
        go_to_page("main_menu")


def show_page(page_name: str) -> None:
    if page_name == "database":
        show_database_page()
        return

    config = PAGE_CONFIGS.get(page_name)

    if config is None:
        st.session_state["page"] = "start_screen"
        st.rerun()
        return

    page_function = load_page_function(config)

    if page_function is None:
        show_missing_page(config)
        return

    page_function()


VALID_PAGES = set(PAGE_CONFIGS.keys()) | {"database"}


page_from_url = st.query_params.get("page")

if page_from_url in VALID_PAGES:
    st.session_state["page"] = page_from_url
    st.query_params.clear()
    st.rerun()


if "page" not in st.session_state:
    st.session_state["page"] = "start_screen"


show_page(st.session_state["page"])
