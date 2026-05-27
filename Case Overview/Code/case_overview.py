import base64
import sys
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


SUPPORTED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}

project_root = Path(__file__).resolve().parents[2]
back_button_code_dir = project_root / "Back to main menu" / "Code"

if str(back_button_code_dir) not in sys.path:
    sys.path.append(str(back_button_code_dir))

from back_to_main_menu import get_back_button_css, get_back_button_html, render_back_button_streamlit


def image_to_base64(image_path: Path) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


def find_first_asset_image() -> Path:
    case_overview_folder = Path(__file__).resolve().parents[1]
    assets_folder = case_overview_folder / "Assets"

    if not assets_folder.exists():
        raise FileNotFoundError(f"Assets folder not found: {assets_folder}")

    image_files = sorted(
        file_path
        for file_path in assets_folder.iterdir()
        if file_path.is_file()
        and file_path.suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS
    )

    if not image_files:
        raise FileNotFoundError(
            f"No image file found in {assets_folder}."
        )

    return image_files[0]


def show_case_overview() -> None:
    background_path = find_first_asset_image()
    background_b64 = image_to_base64(background_path)

    back_btn_html = get_back_button_html(btn_key="co_back")
    back_btn_css = get_back_button_css(left="1.2%", top="2.0%", width="16%")

    st.markdown(
        """
        <style>
        html, body, .stApp {
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
            background: #1c0f08 !important;
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
            background: #1c0f08;
        }}

        .co-page {{
            width: 100vw;
            height: 100vh;
            background-image: url("data:image/png;base64,{background_b64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            position: relative;
        }}

        {back_btn_css}
        </style>
    </head>
    <body>
        <div class="co-page">
            {back_btn_html}
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

    render_back_button_streamlit(btn_key="co_back", target_page="main_menu")


def show_case_overview_detail() -> None:
    show_case_overview()
