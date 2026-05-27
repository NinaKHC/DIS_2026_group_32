import os
import sys
from pathlib import Path

import streamlit as st
from sqlalchemy import create_engine, inspect


st.set_page_config(
    page_title="Jewel Heist Database",
    layout="wide",
    initial_sidebar_state="collapsed",
)


project_root = Path(__file__).resolve().parent


def add_code_path(*folder_names: str) -> None:
    """
    Adds the first existing '<folder>/Code' path to sys.path.
    This makes imports work even if folders have slightly different capitalization.
    """

    for folder_name in folder_names:
        code_path = project_root / folder_name / "Code"
        if code_path.exists():
            sys.path.append(str(code_path))
            return

    # Fallback: add the first option, so possible import errors point somewhere useful.
    sys.path.append(str(project_root / folder_names[0] / "Code"))


# IMPORTANT:
# These must be added before importing from start_screen, main_menu, case_overview, exit_screen.
add_code_path("Start Screen", "start_screen", "Start screen")
add_code_path("Main Menu", "Main menu", "main_menu")
add_code_path("Case Overview", "case_overview")
add_code_path("Exit Funktion", "Exit Function", "exit_function")


from start_screen import show_start_screen
from main_menu import show_main_menu
from case_overview import show_case_overview
from exit_screen import show_exit_screen


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/streamlit_db",
)


def go_to_page(page_name: str) -> None:
    st.session_state["page"] = page_name
    st.rerun()


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


def show_placeholder_page(title: str) -> None:
    st.title(title)
    st.write("This page has not been implemented yet.")

    if st.button("Back to Main Menu"):
        go_to_page("main_menu")


VALID_PAGES = {
    "start_screen",
    "main_menu",
    "case_overview",
    "crime_scene",
    "witnesses",
    "suspects",
    "evidence",
    "stolen_items",
    "locations",
    "timeline",
    "surveillance_media",
    "access_logs",
    "notes_connections",
    "arrest_suspect",
    "database",
    "exit",
}

page_from_url = st.query_params.get("page")

if page_from_url in VALID_PAGES:
    st.session_state["page"] = page_from_url
    st.query_params.clear()
    st.rerun()

if "page" not in st.session_state:
    st.session_state["page"] = "start_screen"



page = st.session_state["page"]

if page == "start_screen":
    show_start_screen()

elif page == "main_menu":
    show_main_menu()

elif page == "case_overview":
    show_case_overview()

elif page == "crime_scene":
    show_placeholder_page("Crime Scene")

elif page == "witnesses":
    show_placeholder_page("Witnesses")

elif page == "suspects":
    show_placeholder_page("Suspects")

elif page == "evidence":
    show_placeholder_page("Evidence")

elif page == "stolen_items":
    show_placeholder_page("Stolen Items")

elif page == "locations":
    show_placeholder_page("Locations")

elif page == "timeline":
    show_placeholder_page("Timeline")

elif page == "surveillance_media":
    show_placeholder_page("Surveillance & Media")

elif page == "access_logs":
    show_placeholder_page("Access Logs")

elif page == "notes_connections":
    show_placeholder_page("Notes / Connections")

elif page == "arrest_suspect":
    show_placeholder_page("Arrest the Suspect")

elif page == "database":
    show_database_page()

elif page == "exit":
    show_exit_screen()

else:
    st.session_state["page"] = "start_screen"
    st.rerun()
