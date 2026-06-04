import base64
from pathlib import Path

from PIL import Image
import streamlit as st
import streamlit.components.v1 as components


IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp")

BACKGROUND_IMAGE_NAME = "Case Overview.png"
PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACK_TO_START_ASSETS_DIR = PROJECT_ROOT / "Back to start" / "Assets"

MENU_BUTTONS = [
    {
        "button_text": "mm_case_overview",
        "page": "case_overview",
        "label": "Case Overview",
        "image": "Case_overview.png",
        "css_class": "btn-case-overview",
    },
    {
        "button_text": "mm_crime_scene",
        "page": "crime_scene",
        "label": "Crime Scene",
        "image": "Crime_scene.png",
        "css_class": "btn-crime-scene",
    },
    {
        "button_text": "mm_witnesses",
        "page": "witnesses",
        "label": "Witness",
        "image": "Witness.png",
        "css_class": "btn-witnesses",
    },
    {
        "button_text": "mm_suspects",
        "page": "suspects",
        "label": "Suspects",
        "image": "Suspects.png",
        "css_class": "btn-suspects",
    },
    {
        "button_text": "mm_stolen_items",
        "page": "stolen_items",
        "label": "Stolen Items",
        "image": "Stolen_items.png",
        "css_class": "btn-stolen-items",
    },
    {
        "button_text": "mm_locations",
        "page": "locations",
        "label": "Map",
        "image": "Map.png",
        "css_class": "btn-locations",
    },
    {
        "button_text": "mm_access_logs",
        "page": "access_logs",
        "label": "Access Logs",
        "image": "Access_logs.png",
        "css_class": "btn-access-logs",
    },
    {
        "button_text": "mm_replay_intro",
        "page": "intro",
        "label": "Replay Intro",
        "image": "Replay_intro.png",
        "css_class": "btn-replay-intro",
    },
    {
        "button_text": "mm_arrest_suspect",
        "page": "arrest_suspect",
        "label": "Arrest the Suspect",
        "image": "Arrest_the_suspect.png",
        "css_class": "btn-arrest-suspect",
    },
    {
        "button_text": "mm_start_screen",
        "page": "start_screen",
        "label": "Exit to Start",
        "image": "Exit_to_start.png",
        "css_class": "btn-exit-main-menu",
    },
]


def image_to_base64(image_path: Path) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


def get_image_aspect_ratio(image_path: Path) -> float:
    with Image.open(image_path) as img:
        image_width, image_height = img.size
    return image_width / image_height


def find_first_image(assets_dir: Path) -> Path:
    for image_path in sorted(assets_dir.iterdir()):
        if image_path.suffix.lower() in IMAGE_EXTENSIONS:
            return image_path
    raise FileNotFoundError(f"No image file found in: {assets_dir}")


def find_background_image(assets_dir: Path) -> Path:
    background_path = assets_dir / BACKGROUND_IMAGE_NAME
    if background_path.exists():
        return background_path
    return find_first_image(assets_dir)


def build_menu_buttons_html(assets_dir: Path) -> str:
    buttons_html = []

    for button in MENU_BUTTONS:
        image_path = assets_dir / button["image"]
        if not image_path.exists():
            image_path = BACK_TO_START_ASSETS_DIR / button["image"]
        if not image_path.exists():
            continue

        image_b64 = image_to_base64(image_path)
        buttons_html.append(
            f"""
            <button
                class="menu-image-button {button['css_class']}"
                onclick="navigate('{button['button_text']}')"
                aria-label="{button['label']}">
                <img src="data:image/png;base64,{image_b64}" alt="{button['label']}">
            </button>
            """
        )

    return "\n".join(buttons_html)


def show_main_menu() -> None:
    feature_dir = Path(__file__).resolve().parents[1]
    assets_dir = feature_dir / "Assets"

    try:
        background_path = find_background_image(assets_dir)
    except FileNotFoundError as error:
        st.error(str(error))
        st.stop()

    background_b64 = image_to_base64(background_path)
    menu_buttons_html = build_menu_buttons_html(assets_dir)

    aspect_ratio = get_image_aspect_ratio(background_path)

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

        .menu-image-button {{
            position: absolute;
            background: transparent;
            border: 0;
            padding: 0;
            margin: 0;
            cursor: pointer;
            z-index: 4;
            filter: drop-shadow(0 1.2vh 1.2vh rgba(0, 0, 0, 0.34));
            transition: transform 0.16s ease, filter 0.16s ease;
        }}

        .menu-image-button:hover {{
            transform: translateY(-0.8%) scale(1.035);
            filter: drop-shadow(0 1.5vh 1.4vh rgba(0, 0, 0, 0.42)) brightness(1.06);
        }}

        .menu-image-button img {{
            width: 100%;
            height: 100%;
            object-fit: contain;
            display: block;
            user-select: none;
            pointer-events: none;
        }}

        .btn-case-overview {{ left: 18.5%; top: 35.5%; width: 15.5%; height: 27.5%; }}
        .btn-crime-scene   {{ left: 38.8%; top: 35.8%; width: 14.0%; height: 24.9%; }}
        .btn-witnesses     {{ left: 28.0%; top: 7.8%; width: 14.0%; height: 24.9%; }}
        .btn-suspects      {{ left: 45.2%; top: 7.8%; width: 14.0%; height: 24.9%; }}
        .btn-stolen-items  {{ left: 28.5%; top: 60.0%; width: 17.5%; height: 25.5%; }}
        .btn-locations     {{ left: 45.0%; top: 70.0%; width: 17.5%; height: 25.5%; }}
        .btn-access-logs   {{ left: 59.3%; top: 36.0%; width: 12.4%; height: 31.0%; }}
        .btn-replay-intro  {{ left: 60.0%; top: 10.0%; width: 15.5%; height: 23.0%; }}
        .btn-arrest-suspect {{ left: 76.5%; top: 32.0%; width: 20.0%; height: 30.5%; }}
        .btn-exit-main-menu  {{ left: 62.8%; top: 66.2%; width: 15.5%; height: 23.0%; }}
        </style>
    </head>
    <body>
        <div class="mm-page">
            <div class="menu-stage">
                {menu_buttons_html}
            </div>
        </div>

        <script>
        let navigationPending = false;
        function navigate(page) {{
            if (navigationPending) return;
            navigationPending = true;

            let attempts = 0;
            const clickWhenReady = function() {{
                attempts += 1;
                var buttons = window.parent.document.querySelectorAll('button');
                for (var i = 0; i < buttons.length; i++) {{
                    if (buttons[i].innerText.trim() === page && !buttons[i].disabled) {{
                        buttons[i].click();
                        return;
                    }}
                }}

                if (attempts < 20) {{
                    window.setTimeout(clickWhenReady, 75);
                }} else {{
                    navigationPending = false;
                }}
            }};

            window.setTimeout(clickWhenReady, 120);
        }}
        </script>
    </body>
    </html>
    """

    components.html(html, height=1, scrolling=False)

    destinations = [(button["button_text"], button["page"]) for button in MENU_BUTTONS]

    cols = st.columns(len(destinations))
    for col, (btn_text, page) in zip(cols, destinations):
        with col:
            if st.button(btn_text, key=f"mm_hidden_{btn_text}"):
                if btn_text == "mm_replay_intro":
                    st.session_state["intro_seen"] = True
                st.session_state["page"] = page
                st.rerun()


def show_case_overview() -> None:
    show_main_menu()
