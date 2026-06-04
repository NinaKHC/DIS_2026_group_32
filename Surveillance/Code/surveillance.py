import base64
import sys
from pathlib import Path

from PIL import Image
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


ASSETS_DIR = Path(__file__).resolve().parents[1] / "Assets"

SURVEILLANCE = [
    {"label": "Camera 1", "image_filename": None},
    {"label": "Camera 2", "image_filename": None},
    {"label": "Camera 3", "image_filename": None},
    {"label": "Camera 4", "image_filename": None},
    {"label": "Camera 5", "image_filename": None},
]

SLOT_POSITIONS = [
    (33.0, 8.0, 26.5, 44.0),
    (62.0, 8.0, 26.5, 42.0),
    (31.0, 56.0, 17.5, 36.0),
    (51.0, 56.0, 17.5, 36.0),
    (70.5, 56.0, 17.5, 36.0),
]


def image_to_base64(image_path: Path) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def get_aspect_ratio(image_path: Path) -> float:
    with Image.open(image_path) as img:
        w, h = img.size
    return w / h


def _streamlit_chrome_css() -> str:
    return """
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
    """


def _navigate_js() -> str:
    return """
    <script>
    let navigationPending = false;
    function navigate(page) {
        if (navigationPending) return;
        navigationPending = true;

        let attempts = 0;
        const clickWhenReady = function() {
            attempts += 1;
            var buttons = window.parent.document.querySelectorAll('button');
            for (var i = 0; i < buttons.length; i++) {
                if (buttons[i].innerText.trim() === page && !buttons[i].disabled) {
                    buttons[i].click();
                    return;
                }
            }

            if (attempts < 20) {
                window.setTimeout(clickWhenReady, 75);
            } else {
                navigationPending = false;
            }
        };

        window.setTimeout(clickWhenReady, 120);
    }
    </script>
    """


def _render_overview(back_btn_html: str, back_btn_css: str) -> None:
    bg_path = ASSETS_DIR / "Surveillance folder.png"
    if not bg_path.exists():
        st.error(f"Background image not found: {bg_path}")
        st.stop()

    bg_b64 = image_to_base64(bg_path)
    aspect_ratio = get_aspect_ratio(bg_path)

    slots_html = ""
    for i, (left, top, width, height) in enumerate(SLOT_POSITIONS):
        item = SURVEILLANCE[i] if i < len(SURVEILLANCE) else None
        if item is None:
            continue

        thumb_html = ""
        if item.get("image_filename"):
            img_path = ASSETS_DIR / item["image_filename"]
            if img_path.exists():
                b64 = image_to_base64(img_path)
                thumb_html = f'<img src="data:image/png;base64,{b64}" alt="{item["label"]}">'

        label = item.get("label", "")
        slots_html += f"""
        <div
            class="sv-slot"
            style="left:{left}%;top:{top}%;width:{width}%;height:{height}%;"
            onclick="navigate('sv_click_{i}')"
            title="{label}"
            role="button"
            aria-label="{label}">
            {thumb_html}
        </div>
        """

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

        .sv-page {{
            width: 100vw; height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #2a1a0a;
        }}

        .sv-stage {{
            position: relative;
            width: min(100vw, calc(100vh * {aspect_ratio}));
            aspect-ratio: {aspect_ratio};
        }}

        .sv-bg {{
            position: absolute;
            inset: 0; width: 100%; height: 100%;
            object-fit: contain;
            z-index: 1;
            pointer-events: none;
            user-select: none;
        }}

        .sv-slot {{
            position: absolute;
            z-index: 5;
            cursor: pointer;
            transition: filter 0.15s ease, transform 0.12s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }}

        .sv-slot:hover {{
            filter: brightness(1.2);
            transform: scale(1.02);
        }}

        .sv-slot img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            pointer-events: none;
            user-select: none;
        }}

        {back_btn_css}
        </style>
    </head>
    <body>
        <div class="sv-page">
            <div class="sv-stage">
                {back_btn_html}
                <img class="sv-bg" src="data:image/png;base64,{bg_b64}" alt="Surveillance folder">
                {slots_html}
            </div>
        </div>
        {_navigate_js()}
    </body>
    </html>
    """

    components.html(html, height=1, scrolling=False)


def _render_zoom(
    back_btn_html: str,
    back_btn_css: str,
    current_index: int,
    num_items: int,
) -> None:
    bg_path = ASSETS_DIR / "Surveillance folder.png"
    bg_b64 = image_to_base64(bg_path)
    aspect_ratio = get_aspect_ratio(bg_path)

    item = SURVEILLANCE[current_index]
    label = item.get("label", "")

    zoom_img_html = ""
    if item.get("image_filename"):
        img_path = ASSETS_DIR / item["image_filename"]
        if img_path.exists():
            b64 = image_to_base64(img_path)
            zoom_img_html = f'<img class="sv-zoom-img" src="data:image/png;base64,{b64}" alt="{label}">'

    left_arrow = make_screen_arrow_button(
        direction="left",
        onclick="navigate('prev')",
        css_class="sv-arrow-left",
        aria_label="Previous image",
    )
    right_arrow = make_screen_arrow_button(
        direction="right",
        onclick="navigate('next')",
        css_class="sv-arrow-right",
        aria_label="Next image",
    )

    counter_text = f"{current_index + 1} / {num_items}"

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

        .sv-page {{
            width: 100vw; height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #2a1a0a;
        }}

        .sv-stage {{
            position: relative;
            width: min(100vw, calc(100vh * {aspect_ratio}));
            aspect-ratio: {aspect_ratio};
        }}

        .sv-bg {{
            position: absolute;
            inset: 0; width: 100%; height: 100%;
            object-fit: contain;
            z-index: 1;
            pointer-events: none;
            user-select: none;
            filter: brightness(0.25);
        }}

        .sv-overlay {{
            position: absolute;
            inset: 0;
            background: rgba(0,0,0,0.55);
            z-index: 2;
        }}

        .sv-zoom-img {{
            position: absolute;
            left: 10%;
            top: 8%;
            width: 80%;
            height: 75%;
            object-fit: contain;
            z-index: 10;
            border: 3px solid rgba(255,255,255,0.25);
            border-radius: 4px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.7);
        }}

        .sv-zoom-label {{
            position: absolute;
            left: 50%;
            bottom: 9%;
            transform: translateX(-50%);
            z-index: 15;
            font-family: Georgia, serif;
            font-size: clamp(12px, 1.2vw, 20px);
            color: #f4dfaa;
            font-weight: bold;
            white-space: nowrap;
            text-shadow: 0 1px 4px rgba(0,0,0,0.8);
        }}

        .sv-back-overview {{
            position: absolute;
            right: 2%;
            top: 2.5%;
            z-index: 20;
            cursor: pointer;
            font-family: Georgia, serif;
            font-size: clamp(11px, 1vw, 17px);
            color: #f4dfaa;
            background: rgba(40, 20, 5, 0.85);
            border: 2px solid rgba(244,223,170,0.5);
            border-radius: 8px;
            padding: 0.3em 0.8em;
            transition: filter 0.15s ease;
            user-select: none;
        }}

        .sv-back-overview:hover {{
            filter: brightness(1.2);
        }}

        .sv-counter {{
            position: absolute;
            left: 50%;
            bottom: 3%;
            transform: translateX(-50%);
            z-index: 20;
            color: #f4dfaa;
            background: rgba(0,0,0,0.55);
            padding: 0.25rem 0.75rem;
            border-radius: 999px;
            font-size: clamp(12px, 0.85vw, 18px);
            font-weight: 800;
            letter-spacing: 0.04em;
        }}

        {back_btn_css}

        {screen_arrow_css()}

        .sv-arrow-left {{
            left: 1.0%;
            top: 30%;
            width: 7%;
            height: 38%;
        }}

        .sv-arrow-right {{
            right: 1.0%;
            top: 30%;
            width: 7%;
            height: 38%;
        }}
        </style>
    </head>
    <body>
        <div class="sv-page">
            <div class="sv-stage">
                {back_btn_html}
                <img class="sv-bg" src="data:image/png;base64,{bg_b64}" alt="Surveillance folder">
                <div class="sv-overlay"></div>

                {zoom_img_html}

                <div class="sv-zoom-label">{label}</div>

                <div
                    class="sv-back-overview"
                    onclick="navigate('sv_overview')"
                    role="button"
                    aria-label="Back to overview">
                    ← Overview
                </div>

                {left_arrow}
                {right_arrow}

                <div class="sv-counter">{counter_text}</div>
            </div>
        </div>
        {_navigate_js()}
    </body>
    </html>
    """

    components.html(html, height=1, scrolling=False)


def show_surveillance_media() -> None:
    if "sv_mode" not in st.session_state:
        st.session_state.sv_mode = "overview"
    if "sv_index" not in st.session_state:
        st.session_state.sv_index = 0

    num_items = len(SURVEILLANCE)
    current_index = st.session_state.sv_index % max(num_items, 1)
    st.session_state.sv_index = current_index
    mode = st.session_state.sv_mode

    back_btn_html = get_back_button_html(btn_key="sv_back")
    back_btn_css  = get_back_button_css(left="1.0%", top="1.5%", width="10%")

    st.markdown(_streamlit_chrome_css(), unsafe_allow_html=True)

    if mode == "overview":
        _render_overview(back_btn_html, back_btn_css)
    else:
        _render_zoom(back_btn_html, back_btn_css, current_index, num_items)

    render_back_button_streamlit(btn_key="sv_back", target_page="main_menu")

    if st.button("sv_overview", key="sv_hidden_overview"):
        st.session_state.sv_mode = "overview"
        st.rerun()

    sv_click_cols = st.columns(max(num_items, 1))
    for i, col in enumerate(sv_click_cols):
        if i < num_items:
            with col:
                if st.button(f"sv_click_{i}", key=f"sv_hidden_click_{i}"):
                    st.session_state.sv_index = i
                    st.session_state.sv_mode = "zoom"
                    st.rerun()

    col_prev, col_next = st.columns(2)
    with col_prev:
        if st.button("prev", key="sv_prev"):
            st.session_state.sv_index = (current_index - 1) % num_items
            st.rerun()
    with col_next:
        if st.button("next", key="sv_next"):
            st.session_state.sv_index = (current_index + 1) % num_items
            st.rerun()


def show_surveillance() -> None:
    show_surveillance_media()
