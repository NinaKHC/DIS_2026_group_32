import base64
from pathlib import Path

import streamlit as st


IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp")


def image_to_base64(image_path: Path) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


def find_first_image(assets_dir: Path) -> Path:

    for image_path in sorted(assets_dir.iterdir()):
        if image_path.suffix.lower() in IMAGE_EXTENSIONS:
            return image_path

    raise FileNotFoundError(f"No image file found in: {assets_dir}")


def set_main_menu_background(image_path: Path) -> None:
    encoded_image = image_to_base64(image_path)

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_image}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-color: #5a3218;
        }}

        [data-testid="stHeader"] {{
            background: rgba(0, 0, 0, 0);
        }}

        [data-testid="stToolbar"] {{
            display: none;
        }}

        .block-container {{
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 0rem;
            padding-right: 0rem;
            max-width: 100%;
        }}

        .case-click-zone {{
            position: fixed;
            display: block;
            z-index: 9999;
            background: transparent;
            text-decoration: none;
            cursor: pointer;
            border-radius: 12px;
        }}

        .case-click-zone::after {{
            content: "";
            position: absolute;
            inset: 0;
            border: 3px solid rgba(255, 210, 122, 0.65);
            background: rgba(255, 210, 122, 0.10);
            border-radius: 14px;
            opacity: 0;
            transition: opacity 0.15s ease;
            pointer-events: none;
        }}

        .case-click-zone:hover::after {{
            opacity: 1;
        }}

        /* Dine manuelt justerede klikfelter */
        .zone-case-overview {{
            left: 26.0vw;
            top: 6.3vh;
            width: 10.0vw;
            height: 26.6vh;
        }}

        .zone-crime-scene {{
            left: 39.2vw;
            top: 5.4vh;
            width: 9.9vw;
            height: 25.8vh;
        }}

        .zone-witnesses {{
            left: 53.1vw;
            top: 6.3vh;
            width: 8.1vw;
            height: 23.3vh;
        }}

        .zone-suspects {{
            left: 66.4vw;
            top: 8.0vh;
            width: 10.5vw;
            height: 21.6vh;
        }}

        .zone-evidence {{
            left: 13.8vw;
            top: 40vh;
            width: 9vw;
            height: 18.3vh;
        }}

        .zone-stolen-items {{
            left: 27.6vw;
            top: 35.9vh;
            width: 11.8vw;
            height: 22.9vh;
        }}

        .zone-locations {{
            left: 44.2vw;
            top: 35.3vh;
            width: 15.6vw;
            height: 21.5vh;
        }}

        .zone-timeline {{
            left: 64vw;
            top: 35.9vh;
            width: 9.9vw;
            height: 22.9vh;
        }}

        .zone-surveillance-media {{
            left: 15.1vw;
            top: 65.5vh;
            width: 13.1vw;
            height: 15.6vh;
        }}

        .zone-access-logs {{
            left: 32.1vw;
            top: 63.5vh;
            width: 10.7vw;
            height: 28.2vh;
        }}

        .zone-notes-connections {{
            left: 47.9vw;
            top: 61.9vh;
            width: 12.2vw;
            height: 30.7vh;
        }}

        .zone-arrest-suspect {{
            left: 83.7vw;
            top: 36.5vh;
            width: 6.6vw;
            height: 27.1vh;
        }}

        .zone-exit-main-menu {{
            left: 67.7vw;
            top: 67.5vh;
            width: 8.2vw;
            height: 22.8vh;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def handle_main_menu_navigation() -> None:
    page_from_url = st.query_params.get("page")

    if page_from_url:
        st.session_state["page"] = page_from_url
        st.query_params.clear()
        st.rerun()


def show_main_menu() -> None:
    # Denne fil ligger i: Main Menu / Code / main_menu.py
    # Derfor er parents[1] selve Main Menu-mappen.
    feature_dir = Path(__file__).resolve().parents[1]
    assets_dir = feature_dir / "Assets"

    try:
        background_path = find_first_image(assets_dir)
    except FileNotFoundError as error:
        st.error(str(error))
        st.stop()

    set_main_menu_background(background_path)
    handle_main_menu_navigation()

    st.markdown(
        """
        <a class="case-click-zone zone-case-overview" href="?page=case_overview" aria-label="Case Overview"></a>

        <a class="case-click-zone zone-crime-scene" href="?page=crime_scene" aria-label="Crime Scene"></a>

        <a class="case-click-zone zone-witnesses" href="?page=witnesses" aria-label="Witnesses"></a>

        <a class="case-click-zone zone-suspects" href="?page=suspects" aria-label="Suspects"></a>

        <a class="case-click-zone zone-evidence" href="?page=evidence" aria-label="Evidence"></a>

        <a class="case-click-zone zone-stolen-items" href="?page=stolen_items" aria-label="Stolen Items"></a>

        <a class="case-click-zone zone-locations" href="?page=locations" aria-label="Locations"></a>

        <a class="case-click-zone zone-timeline" href="?page=timeline" aria-label="Timeline"></a>

        <a class="case-click-zone zone-surveillance-media" href="?page=surveillance_media" aria-label="Surveillance and Media"></a>

        <a class="case-click-zone zone-access-logs" href="?page=access_logs" aria-label="Access Logs"></a>

        <a class="case-click-zone zone-notes-connections" href="?page=notes_connections" aria-label="Notes and Connections"></a>

        <a class="case-click-zone zone-arrest-suspect" href="?page=arrest_suspect" aria-label="Arrest the Suspect"></a>

        <a class="case-click-zone zone-exit-main-menu" href="?page=start_screen" aria-label="Exit to Start Screen"></a>
        """,
        unsafe_allow_html=True
    )


# Bagudkompatibilitet, hvis noget gammel kode stadig kalder show_case_overview()
def show_case_overview() -> None:
    show_main_menu()
