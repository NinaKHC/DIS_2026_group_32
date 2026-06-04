import sys
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


shared_code_dir = Path(__file__).resolve().parents[2] / "Shared" / "Code"

if str(shared_code_dir) not in sys.path:
    sys.path.append(str(shared_code_dir))

from path_helpers import add_code_paths, assets_dir, code_dir

add_code_paths(
    code_dir("Back to main menu"),
    code_dir("Database"),
)

from back_to_main_menu import get_back_button_css, get_back_button_html, render_back_button_streamlit
from database_helpers import get_map_markers
from ui_helpers import get_aspect_ratio, image_to_base64, navigate_script, streamlit_chrome_css


ASSETS_DIR = assets_dir(__file__)

LOCATIONS: list[dict] = [
]


def _build_markers_html(locations: list[dict]) -> str:
    html = ""
    for loc in locations:
        x = loc.get("x", 50)
        y = loc.get("y", 50)
        name = loc.get("name", "")
        color = loc.get("color", "#cc2200")
        html += f"""
        <div
            class="map-marker"
            style="left:{x}%;top:{y}%;--marker-color:{color};"
            title="{name}"
            aria-label="{name}">
            <div class="map-marker-dot"></div>
            {f'<div class="map-marker-label">{name}</div>' if name else ""}
        </div>
        """
    return html


def show_map() -> None:
    map_path = ASSETS_DIR / "city map.png"
    if not map_path.exists():
        st.error(f"Map image not found: {map_path}")
        st.stop()

    map_b64 = image_to_base64(map_path)
    aspect_ratio = get_aspect_ratio(map_path)

    back_btn_html = get_back_button_html(btn_key="map_back")
    back_btn_css = get_back_button_css(left="1.0%", top="1.5%", width="10%")

    markers_html = _build_markers_html(get_map_markers(LOCATIONS))

    st.markdown(
        streamlit_chrome_css(),
        unsafe_allow_html=True,
    )

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
        html, body {{
            margin: 0; padding: 0;
            width: 100vw; height: 100vh;
            overflow: hidden;
            background: #2a1a0a;
        }}

        .map-page {{
            width: 100vw; height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #2a1a0a;
        }}

        .map-stage {{
            position: relative;
            width: min(100vw, calc(100vh * {aspect_ratio}));
            aspect-ratio: {aspect_ratio};
        }}

        .map-img {{
            position: absolute;
            inset: 0;
            width: 100%; height: 100%;
            object-fit: contain;
            z-index: 1;
            user-select: none;
            pointer-events: none;
        }}

        .map-marker {{
            position: absolute;
            z-index: 10;
            transform: translate(-50%, -50%);
            cursor: default;
        }}

        .map-marker-dot {{
            width: clamp(8px, 1.2vw, 18px);
            height: clamp(8px, 1.2vw, 18px);
            background: var(--marker-color, #cc2200);
            border: 2px solid #fff;
            border-radius: 50%;
            box-shadow: 0 0 6px rgba(0,0,0,0.6);
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }}

        .map-marker:hover .map-marker-dot {{
            transform: scale(1.4);
            box-shadow: 0 0 10px rgba(204,34,0,0.7);
        }}

        .map-marker-label {{
            position: absolute;
            bottom: calc(100% + 6px);
            left: 50%;
            transform: translateX(-50%);
            background: rgba(30, 15, 5, 0.88);
            color: #f4dfaa;
            font-family: Georgia, serif;
            font-size: clamp(9px, 0.85vw, 14px);
            white-space: nowrap;
            padding: 0.2em 0.6em;
            border-radius: 4px;
            border: 1px solid rgba(244,223,170,0.4);
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.15s ease;
        }}

        .map-marker:hover .map-marker-label {{
            opacity: 1;
        }}

        {back_btn_css}
        </style>
    </head>
    <body>
        <div class="map-page">
            <div class="map-stage">
                {back_btn_html}
                <img class="map-img" src="data:image/png;base64,{map_b64}" alt="City map">
                {markers_html}
            </div>
        </div>

        {navigate_script()}
    </body>
    </html>
    """

    components.html(html, height=1, scrolling=False)

    render_back_button_streamlit(btn_key="map_back", target_page="main_menu")


def show_locations() -> None:
    show_map()
