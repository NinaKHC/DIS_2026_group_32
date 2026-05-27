import base64
from pathlib import Path

from PIL import Image
import streamlit as st
import streamlit.components.v1 as components


IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp")


def image_to_base64(image_path: Path) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


def find_first_image(assets_dir: Path) -> Path:
    for image_path in sorted(assets_dir.iterdir()):
        if image_path.suffix.lower() in IMAGE_EXTENSIONS:
            return image_path
    raise FileNotFoundError(f"No image file found in: {assets_dir}")


def show_main_menu() -> None:
    feature_dir = Path(__file__).resolve().parents[1]
    assets_dir = feature_dir / "Assets"

    try:
        background_path = find_first_image(assets_dir)
    except FileNotFoundError as error:
        st.error(str(error))
        st.stop()

    background_b64 = image_to_base64(background_path)

    with Image.open(background_path) as img:
        image_width, image_height = img.size
    aspect_ratio = image_width / image_height

    st.markdown(
        """
        <style>
        html, body, .stApp {
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
            background-color: #5a3218 !important;
        }

        [data-testid="stHeader"] {
            background: rgba(0, 0, 0, 0) !important;
            height: 0rem !important;
        }

        [data-testid="stToolbar"],
        [data-testid="stDecoration"] {
            display: none !important;
        }

        .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
            height: 100vh !important;
            overflow: hidden !important;
        }

        section.main,
        div[data-testid="stAppViewContainer"],
        div[data-testid="stVerticalBlock"] {
            overflow: hidden !important;
        }

        iframe {
            width: 100vw !important;
            height: 100vh !important;
            display: block !important;
            border: none !important;
        }

        .element-container:has(iframe) {
            width: 100vw !important;
            height: 100vh !important;
            overflow: hidden !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
        html, body {{
            margin: 0;
            padding: 0;
            width: 100vw;
            height: 100vh;
            overflow: hidden;
            background-color: #5a3218;
        }}

        .mm-page {{
            width: 100vw;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #5a3218;
        }}

        .menu-stage {{
            position: relative;
            width: min(100vw, calc(100vh * {aspect_ratio}));
            height: min(100vh, calc(100vw / {aspect_ratio}));
            background-image: url("data:image/png;base64,{background_b64}");
            background-size: contain;
            background-position: center;
            background-repeat: no-repeat;
        }}

        .case-click-zone {{
            position: absolute;
            display: block;
            background: transparent;
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

        .zone-case-overview     {{ left: 26.0%; top:  6.3%; width: 10.0%; height: 26.6%; }}
        .zone-crime-scene       {{ left: 39.2%; top:  5.4%; width:  9.9%; height: 25.8%; }}
        .zone-witnesses         {{ left: 53.1%; top:  6.3%; width:  8.1%; height: 23.3%; }}
        .zone-suspects          {{ left: 66.4%; top:  8.0%; width: 10.5%; height: 21.6%; }}
        .zone-evidence          {{ left: 13.8%; top: 40.0%; width:  9.0%; height: 18.3%; }}
        .zone-stolen-items      {{ left: 27.6%; top: 35.9%; width: 11.8%; height: 22.9%; }}
        .zone-locations         {{ left: 44.2%; top: 35.3%; width: 15.6%; height: 21.5%; }}
        .zone-timeline          {{ left: 64.0%; top: 35.9%; width:  9.9%; height: 22.9%; }}
        .zone-surveillance-media{{ left: 15.1%; top: 65.5%; width: 13.1%; height: 15.6%; }}
        .zone-access-logs       {{ left: 32.1%; top: 63.5%; width: 10.7%; height: 28.2%; }}
        .zone-notes-connections  {{ left: 47.9%; top: 61.9%; width: 12.2%; height: 30.7%; }}
        .zone-arrest-suspect    {{ left: 83.7%; top: 36.5%; width:  6.6%; height: 27.1%; }}
        .zone-exit-main-menu    {{ left: 67.7%; top: 67.5%; width:  8.2%; height: 22.8%; }}
        </style>
    </head>
    <body>
        <div class="mm-page">
            <div class="menu-stage">
                <div class="case-click-zone zone-case-overview"      onclick="navigate('mm_case_overview')"      role="button" aria-label="Case Overview"></div>
                <div class="case-click-zone zone-crime-scene"        onclick="navigate('mm_crime_scene')"        role="button" aria-label="Crime Scene"></div>
                <div class="case-click-zone zone-witnesses"          onclick="navigate('mm_witnesses')"          role="button" aria-label="Witnesses"></div>
                <div class="case-click-zone zone-suspects"           onclick="navigate('mm_suspects')"           role="button" aria-label="Suspects"></div>
                <div class="case-click-zone zone-evidence"           onclick="navigate('mm_evidence')"           role="button" aria-label="Evidence"></div>
                <div class="case-click-zone zone-stolen-items"       onclick="navigate('mm_stolen_items')"       role="button" aria-label="Stolen Items"></div>
                <div class="case-click-zone zone-locations"          onclick="navigate('mm_locations')"          role="button" aria-label="Locations"></div>
                <div class="case-click-zone zone-timeline"           onclick="navigate('mm_timeline')"           role="button" aria-label="Timeline"></div>
                <div class="case-click-zone zone-surveillance-media" onclick="navigate('mm_surveillance_media')" role="button" aria-label="Surveillance and Media"></div>
                <div class="case-click-zone zone-access-logs"        onclick="navigate('mm_access_logs')"        role="button" aria-label="Access Logs"></div>
                <div class="case-click-zone zone-notes-connections"  onclick="navigate('mm_notes_connections')"  role="button" aria-label="Notes and Connections"></div>
                <div class="case-click-zone zone-arrest-suspect"     onclick="navigate('mm_arrest_suspect')"     role="button" aria-label="Arrest the Suspect"></div>
                <div class="case-click-zone zone-exit-main-menu"     onclick="navigate('mm_start_screen')"       role="button" aria-label="Exit to Start Screen"></div>
            </div>
        </div>

        <script>
        function navigate(page) {{
            var buttons = window.parent.document.querySelectorAll('button');
            for (var i = 0; i < buttons.length; i++) {{
                if (buttons[i].innerText.trim() === page) {{
                    buttons[i].click();
                    return;
                }}
            }}
        }}
        </script>
    </body>
    </html>
    """

    components.html(html, height=1, scrolling=False)

    destinations = [
        ("mm_case_overview",      "case_overview"),
        ("mm_crime_scene",        "crime_scene"),
        ("mm_witnesses",          "witnesses"),
        ("mm_suspects",           "suspects"),
        ("mm_evidence",           "evidence"),
        ("mm_stolen_items",       "stolen_items"),
        ("mm_locations",          "locations"),
        ("mm_timeline",           "timeline"),
        ("mm_surveillance_media", "surveillance_media"),
        ("mm_access_logs",        "access_logs"),
        ("mm_notes_connections",  "notes_connections"),
        ("mm_arrest_suspect",     "arrest_suspect"),
        ("mm_start_screen",       "start_screen"),
    ]

    cols = st.columns(len(destinations))
    for col, (btn_text, page) in zip(cols, destinations):
        with col:
            if st.button(btn_text, key=f"mm_hidden_{btn_text}"):
                st.session_state["page"] = page
                st.rerun()


# Bagudkompatibilitet
def show_case_overview() -> None:
    show_main_menu()
