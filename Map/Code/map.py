import base64
import sys
from pathlib import Path

from PIL import Image
import streamlit as st
import streamlit.components.v1 as components


project_root = Path(__file__).resolve().parents[2]
back_button_code_dir = project_root / "Back to main menu" / "Code"

if str(back_button_code_dir) not in sys.path:
    sys.path.append(str(back_button_code_dir))

from back_to_main_menu import get_back_button_css, get_back_button_html, render_back_button_streamlit


ASSETS_DIR = Path(__file__).resolve().parents[1] / "Assets"

# ── Lokationer ────────────────────────────────────────────────────────────────
# Tilføj lokationer her (eller byg dem fra SQL og send dem ind som liste).
# x og y er i procent af kortets bredde/højde (0–100).
#
# Eksempel:
#   {"name": "Maison Aurora Jewelry", "x": 50.5, "y": 47.0, "color": "#cc2200"}
#
# Farve er valgfri — udelades den bruges standard rød.
LOCATIONS: list[dict] = [
    # Indsæt lokationer her, fx fra SQL:
    # {"name": "Maison Aurora Jewelry", "x": 50.5, "y": 47.0},
]
# ─────────────────────────────────────────────────────────────────────────────


def image_to_base64(image_path: Path) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def get_aspect_ratio(image_path: Path) -> float:
    with Image.open(image_path) as img:
        w, h = img.size
    return w / h


def _build_markers_html(locations: list[dict]) -> str:
    """Laver HTML for alle markører på kortet."""
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
        st.error(f"Kortbillede ikke fundet: {map_path}")
        st.stop()

    map_b64 = image_to_base64(map_path)
    aspect_ratio = get_aspect_ratio(map_path)

    back_btn_html = get_back_button_html(btn_key="map_back")
    back_btn_css = get_back_button_css(left="1.0%", top="1.5%", width="10%")

    markers_html = _build_markers_html(LOCATIONS)

    st.markdown(
        """
        <style>
        html, body, .stApp {
            margin: 0 !important; padding: 0 !important;
            overflow: hidden !important; background: #2a1a0a !important;
        }
        [data-testid="stHeader"] { background: rgba(0,0,0,0) !important; height: 0rem !important; }
        [data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }
        .block-container { padding: 0 !important; margin: 0 !important; max-width: 100% !important; height: 100vh !important; overflow: hidden !important; }
        section.main, div[data-testid="stAppViewContainer"], div[data-testid="stVerticalBlock"] { overflow: hidden !important; }
        iframe { width: 100vw !important; height: 100vh !important; display: block !important; border: none !important; }
        .element-container:has(iframe) { width: 100vw !important; height: 100vh !important; overflow: hidden !important; }
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

        /* Kortet holder fast aspect ratio og fylder hele viewporten */
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

        /* ── Markører ────────────────────────────────────────── */
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

        /* Tooltip-label vises ved hover */
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
            {back_btn_html}
            <div class="map-stage">
                <img class="map-img" src="data:image/png;base64,{map_b64}" alt="City map">
                {markers_html}
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

    render_back_button_streamlit(btn_key="map_back", target_page="main_menu")


def show_locations() -> None:
    show_map()
