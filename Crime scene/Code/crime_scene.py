import base64
import sys
import re
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

project_root = Path(__file__).resolve().parents[2]
back_button_code_dir = project_root / "Back to main menu" / "Code"
screen_arrows_code_dir = project_root / "Screen arrows" / "Code"

if str(back_button_code_dir) not in sys.path:
    sys.path.append(str(back_button_code_dir))

if str(screen_arrows_code_dir) not in sys.path:
    sys.path.append(str(screen_arrows_code_dir))

from back_to_main_menu import get_back_button_css, get_back_button_html, render_back_button_streamlit
from screen_arrows import screen_arrow_css, make_screen_arrow_button


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


def image_to_base64(image_path: Path) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


def natural_sort_key(path: Path):
    parts = re.split(r"(\d+)", path.stem.lower())
    return [int(part) if part.isdigit() else part for part in parts]


def find_background_image(assets_dir: Path) -> Path:
    image_files = [
        file_path
        for file_path in assets_dir.iterdir()
        if file_path.is_file()
        and file_path.suffix.lower() in IMAGE_EXTENSIONS
    ]

    for file_path in image_files:
        name = file_path.stem.lower()

        if "screen" in name or "background" in name:
            return file_path

    raise FileNotFoundError(
        f"No crime scene background image found in: {assets_dir}"
    )


def find_crime_scene_pictures(
    assets_dir: Path,
    background_path: Path
) -> list[Path]:
    image_files = [
        file_path
        for file_path in assets_dir.iterdir()
        if file_path.is_file()
        and file_path.suffix.lower() in IMAGE_EXTENSIONS
        and file_path.resolve() != background_path.resolve()
    ]

    crime_scene_pictures = []

    for file_path in image_files:
        name = file_path.stem.lower()

        is_picture = (
            "picture" in name
            or "photo" in name
            or "crime scene picture" in name
            or "crime_scene_picture" in name
            or "crime-scene-picture" in name
        )

        if is_picture:
            crime_scene_pictures.append(file_path)

    if not crime_scene_pictures:
        crime_scene_pictures = image_files

    return sorted(crime_scene_pictures, key=natural_sort_key)


def show_crime_scene() -> None:
    back_btn_html = get_back_button_html(btn_key="cs_back")
    back_btn_css = get_back_button_css(left="1.2%", top="2.0%", width="13%")

    feature_dir = Path(__file__).resolve().parents[1]
    assets_dir = feature_dir / "Assets"

    background_path = find_background_image(assets_dir)
    crime_scene_pictures = find_crime_scene_pictures(
        assets_dir,
        background_path
    )

    total_pictures = len(crime_scene_pictures)

    # Use session_state for index instead of query params
    if "crime_scene_index" not in st.session_state:
        st.session_state.crime_scene_index = 0

    current_index = st.session_state.crime_scene_index

    if total_pictures > 0:
        current_index = current_index % total_pictures
        st.session_state.crime_scene_index = current_index
        current_picture_path = crime_scene_pictures[current_index]
        current_picture_b64 = image_to_base64(current_picture_path)

        previous_index = (current_index - 1) % total_pictures
        next_index = (current_index + 1) % total_pictures

        counter_text = f"{current_index + 1} / {total_pictures}"
    else:
        current_picture_b64 = None
        previous_index = 0
        next_index = 0
        counter_text = "0 / 0"

    background_b64 = image_to_base64(background_path)

    if current_picture_b64 is not None:
        picture_html = f"""
        <img
            class="crime-scene-picture"
            src="data:image/png;base64,{current_picture_b64}"
            alt="Crime scene picture"
        >
        """
    else:
        picture_html = """
        <div class="crime-scene-empty-message">
            No crime scene pictures found in Assets.
        </div>
        """

    # Build the arrow buttons — crime_scene.py controls what they do (onclick),
    # screen_arrows.py provides the image and base styling.
    left_arrow_html = make_screen_arrow_button(
        direction="left",
        onclick="navigate('prev')",
        css_class="crime-scene-arrow-left",
        aria_label="Previous crime scene picture",
    )
    right_arrow_html = make_screen_arrow_button(
        direction="right",
        onclick="navigate('next')",
        css_class="crime-scene-arrow-right",
        aria_label="Next crime scene picture",
    )

    st.markdown(
        """
        <style>
        html, body, .stApp {
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
            background: #0d0a07 !important;
        }

        [data-testid="stHeader"] {
            background: rgba(0, 0, 0, 0) !important;
            height: 0rem !important;
        }

        [data-testid="stToolbar"],
        [data-testid="stDecoration"] {
            display: none !important;
        }

        /* Hide the invisible navigation buttons */
        #cs-nav-anchor,
        #cs-nav-anchor + div {
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
            background: #0d0a07;
        }}

        .crime-scene-page {{
            width: 100vw;
            height: 100vh;
            overflow: hidden;
            background: #0d0a07;
            display: flex;
            justify-content: center;
            align-items: center;
        }}

        .crime-scene-stage {{
            position: relative;
            width: min(100vw, calc(100vh * 20 / 9));
            aspect-ratio: 20 / 9;
            overflow: hidden;
        }}

        .crime-scene-bg {{
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            object-fit: contain;
            z-index: 1;
            user-select: none;
            pointer-events: none;
        }}

        .crime-scene-picture {{
            position: absolute;
            left: 20.85%;
            top: 18.2%;
            width: 58.2%;
            height: 57.2%;
            object-fit: contain;
            z-index: 3;
            border-radius: 0.3rem;
            pointer-events: none;
        }}

        .crime-scene-empty-message {{
            position: absolute;
            left: 20.85%;
            top: 20.2%;
            width: 58.2%;
            height: 57.2%;
            z-index: 3;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #3a2a18;
            background: rgba(255, 245, 220, 0.85);
            font-size: clamp(16px, 1.4vw, 28px);
            font-weight: 700;
            text-align: center;
            border-radius: 0.3rem;
            box-sizing: border-box;
            padding: 2rem;
        }}

        {back_btn_css}

        /* Positioning for the crime scene arrows.
           Base button styling (image, hover effect, etc.) comes from screen_arrow_css(). */
        {screen_arrow_css()}

        .crime-scene-arrow-left {{
            left: 1.2%;
            top: 37%;
            width: 13.4%;
            height: 23%;
        }}

        .crime-scene-arrow-right {{
            right: 1.5%;
            top: 37%;
            width: 13.4%;
            height: 23%;
        }}

        .crime-scene-counter {{
            position: absolute;
            left: 50%;
            bottom: 7.7%;
            transform: translateX(-50%);
            z-index: 30;
            color: #f4dfaa;
            background: rgba(0, 0, 0, 0.55);
            padding: 0.3rem 0.8rem;
            border-radius: 999px;
            font-size: clamp(13px, 0.9vw, 20px);
            font-weight: 800;
            letter-spacing: 0.04em;
        }}
        </style>
    </head>

    <body>
        <div class="crime-scene-page">
            {back_btn_html}
            <div class="crime-scene-stage">

                <img
                    class="crime-scene-bg"
                    src="data:image/png;base64,{background_b64}"
                    alt="Crime scene screen"
                >

                {picture_html}

                {left_arrow_html}

                {right_arrow_html}

                <div class="crime-scene-counter">
                    {counter_text}
                </div>

            </div>
        </div>

        <script>
        function navigate(direction) {{
            // Find the hidden Streamlit button in the parent and click it
            const buttons = window.parent.document.querySelectorAll('button');
            for (const btn of buttons) {{
                if (btn.innerText.trim() === direction) {{
                    btn.click();
                    return;
                }}
            }}
        }}
        </script>

    </body>
    </html>
    """

    components.html(
        html,
        height=1,
        scrolling=False,
    )

    render_back_button_streamlit(btn_key="cs_back", target_page="main_menu")

    col_prev, col_next = st.columns(2)
    with col_prev:
        if st.button("prev", key="cs_prev"):
            if total_pictures > 0:
                st.session_state.crime_scene_index = (
                    st.session_state.crime_scene_index - 1
                ) % total_pictures
                st.rerun()
    with col_next:
        if st.button("next", key="cs_next"):
            if total_pictures > 0:
                st.session_state.crime_scene_index = (
                    st.session_state.crime_scene_index + 1
                ) % total_pictures
                st.rerun()