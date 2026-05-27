import base64
from pathlib import Path
from PIL import Image
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

    with Image.open(image_path) as image:
        image_width, image_height = image.size

    aspect_ratio = image_width / image_height

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: #5a3218;
        }}

        [data-testid="stHeader"] {{
            background: rgba(0, 0, 0, 0);
        }}

        [data-testid="stToolbar"] {{
            display: none;
        }}

        .block-container {{
            padding: 0rem;
            max-width: 100%;
        }}

        /*
        Hele menuen ligger nu i én responsiv container.
        Den bevarer samme format på alle skærme.
        Her antager vi 16:9.
        Hvis dit billede fx er 1920x1080, er 16/9 korrekt.
        */
        .menu-stage {{
            position: fixed;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);

            width: min(100vw, calc(100vh * {aspect_ratio}));
            height: min(100vh, calc(100vw / {aspect_ratio}));

            background-image: url("data:image/png;base64,{encoded_image}");
            background-size: contain;
            background-position: center;
            background-repeat: no-repeat;

            z-index: 1;
        }}

        .case-click-zone {{
            position: absolute;
            display: block;
            z-index: 10;
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

        /*
        Nu er disse procenter relativt til .menu-stage,
        ikke hele skærmen.
        */
        .zone-case-overview {{
            left: 26.0%;
            top: 6.3%;
            width: 10.0%;
            height: 26.6%;
        }}

        .zone-crime-scene {{
            left: 39.2%;
            top: 5.4%;
            width: 9.9%;
            height: 25.8%;
        }}

        .zone-witnesses {{
            left: 53.1%;
            top: 6.3%;
            width: 8.1%;
            height: 23.3%;
        }}

        .zone-suspects {{
            left: 66.4%;
            top: 8.0%;
            width: 10.5%;
            height: 21.6%;
        }}

        .zone-evidence {{
            left: 13.8%;
            top: 40%;
            width: 9%;
            height: 18.3%;
        }}

        .zone-stolen-items {{
            left: 27.6%;
            top: 35.9%;
            width: 11.8%;
            height: 22.9%;
        }}

        .zone-locations {{
            left: 44.2%;
            top: 35.3%;
            width: 15.6%;
            height: 21.5%;
        }}

        .zone-timeline {{
            left: 64%;
            top: 35.9%;
            width: 9.9%;
            height: 22.9%;
        }}

        .zone-surveillance-media {{
            left: 15.1%;
            top: 65.5%;
            width: 13.1%;
            height: 15.6%;
        }}

        .zone-access-logs {{
            left: 32.1%;
            top: 63.5%;
            width: 10.7%;
            height: 28.2%;
        }}

        .zone-notes-connections {{
            left: 47.9%;
            top: 61.9%;
            width: 12.2%;
            height: 30.7%;
        }}

        .zone-arrest-suspect {{
            left: 83.7%;
            top: 36.5%;
            width: 6.6%;
            height: 27.1%;
        }}

        .zone-exit-main-menu {{
            left: 67.7%;
            top: 67.5%;
            width: 8.2%;
            height: 22.8%;
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
    <div class="menu-stage">
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
    </div>
        """,
        unsafe_allow_html=True
    )


# Bagudkompatibilitet, hvis noget gammel kode stadig kalder show_case_overview()
def show_case_overview() -> None:
    show_main_menu()
