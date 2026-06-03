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
    code_dir("Screen arrows"),
    code_dir("Database"),
)

from back_to_main_menu import get_back_button_css, get_back_button_html, render_back_button_streamlit
from screen_arrows import screen_arrow_css, make_screen_arrow_button
from database_helpers import get_evidence_items
from ui_helpers import get_aspect_ratio, image_to_base64, navigate_script, streamlit_chrome_css


ASSETS_DIR = assets_dir(__file__)

DEFAULT_EVIDENCE = [
    {
        "name": "Evidence 1",
        "description": "Shovel found at the crime scene",
        "image_filename": "Evidens 1.png",
    },
]

EVIDENCE = get_evidence_items(DEFAULT_EVIDENCE)

BOX_POSITIONS = [
    (14.0, 8.0, 17.0, 38.0),
    (33.0, 8.0, 17.0, 38.0),
    (52.0, 8.0, 17.0, 38.0),
    (71.0, 8.0, 17.0, 38.0),
    (14.0, 54.0, 17.0, 40.0),
    (33.0, 54.0, 17.0, 40.0),
    (52.0, 54.0, 17.0, 40.0),
    (71.0, 54.0, 17.0, 40.0),
]


def _render_overview(back_btn_html: str, back_btn_css: str) -> None:
    bg_path = ASSETS_DIR / "Evidens display.png"
    if not bg_path.exists():
        st.error(f"Background image not found: {bg_path}")
        st.stop()

    bg_b64 = image_to_base64(bg_path)
    aspect_ratio = get_aspect_ratio(bg_path)

    boxes_html = ""
    for i, (left, top, width, height) in enumerate(BOX_POSITIONS):
        if i >= len(EVIDENCE):
            break
        item = EVIDENCE[i]
        img_path = ASSETS_DIR / item["image_filename"]
        if not img_path.exists():
            continue
        thumb_b64 = image_to_base64(img_path)
        boxes_html += f"""
        <div
            class="ev-box"
            style="left:{left}%;top:{top}%;width:{width}%;height:{height}%;"
            onclick="navigate('ev_click_{i}')"
            title="{item['name']}"
            role="button"
            aria-label="{item['name']}">
            <img src="data:image/png;base64,{thumb_b64}" alt="{item['name']}">
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
            background: #3a1f0f;
        }}

        .ev-page {{
            width: 100vw; height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #3a1f0f;
        }}

        .ev-stage {{
            position: relative;
            width: min(100vw, calc(100vh * {aspect_ratio}));
            aspect-ratio: {aspect_ratio};
        }}

        .ev-bg {{
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            object-fit: contain;
            z-index: 1;
            pointer-events: none;
            user-select: none;
        }}

        .ev-box {{
            position: absolute;
            z-index: 5;
            cursor: pointer;
            transition: filter 0.15s ease, transform 0.12s ease;
        }}

        .ev-box:hover {{
            filter: brightness(1.18);
            transform: scale(1.03);
        }}

        .ev-box img {{
            width: 100%;
            height: 100%;
            object-fit: contain;
            padding: 8%;
            box-sizing: border-box;
            pointer-events: none;
            user-select: none;
        }}

        {back_btn_css}
        </style>
    </head>
    <body>
        <div class="ev-page">
            <div class="ev-stage">
                {back_btn_html}
                <img class="ev-bg" src="data:image/png;base64,{bg_b64}" alt="Evidence display">
                {boxes_html}
            </div>
        </div>
        {navigate_script()}
    </body>
    </html>
    """

    components.html(html, height=1, scrolling=False)


def _render_zoom(
    back_btn_html: str,
    back_btn_css: str,
    current_index: int,
    num_evidence: int,
) -> None:
    bg_path = ASSETS_DIR / "Evidens zoom.png"
    if not bg_path.exists():
        st.error(f"Zoom background image not found: {bg_path}")
        st.stop()

    bg_b64 = image_to_base64(bg_path)
    aspect_ratio = get_aspect_ratio(bg_path)

    item = EVIDENCE[current_index]
    img_path = ASSETS_DIR / item["image_filename"]
    evidence_img_html = ""
    if img_path.exists():
        ev_b64 = image_to_base64(img_path)
        evidence_img_html = f"""
        <img
            class="ev-zoom-img"
            src="data:image/png;base64,{ev_b64}"
            alt="{item['name']}"
        >
        """

    left_arrow = make_screen_arrow_button(
        direction="left",
        onclick="navigate('prev')",
        css_class="ev-arrow-left",
        aria_label="Previous evidence",
    )
    right_arrow = make_screen_arrow_button(
        direction="right",
        onclick="navigate('next')",
        css_class="ev-arrow-right",
        aria_label="Next evidence",
    )

    counter_text = f"{current_index + 1} / {num_evidence}"
    description = item.get("description", "")

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
        html, body {{
            margin: 0; padding: 0;
            width: 100vw; height: 100vh;
            overflow: hidden;
            background: #3a1f0f;
        }}

        .ev-zoom-page {{
            width: 100vw; height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #3a1f0f;
        }}

        .ev-zoom-stage {{
            position: relative;
            width: min(100vw, calc(100vh * {aspect_ratio}));
            aspect-ratio: {aspect_ratio};
        }}

        .ev-zoom-bg {{
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            object-fit: contain;
            z-index: 1;
            pointer-events: none;
            user-select: none;
        }}

        .ev-zoom-img {{
            position: absolute;
            left: 18%;
            top: 6%;
            width: 64%;
            height: 78%;
            object-fit: contain;
            z-index: 5;
            pointer-events: none;
            user-select: none;
        }}

        .ev-zoom-name {{
            position: absolute;
            left: 50%;
            bottom: 11%;
            transform: translateX(-50%);
            z-index: 10;
            font-family: Georgia, serif;
            font-size: clamp(13px, 1.3vw, 24px);
            color: #2a1a0a;
            font-weight: bold;
            white-space: nowrap;
        }}

        .ev-zoom-desc {{
            position: absolute;
            left: 50%;
            bottom: 6.5%;
            transform: translateX(-50%);
            z-index: 10;
            font-family: Georgia, serif;
            font-size: clamp(10px, 0.9vw, 16px);
            color: #3a2a18;
            white-space: nowrap;
            font-style: italic;
        }}

        .ev-back-overview {{
            position: absolute;
            right: 2%;
            top: 2.5%;
            z-index: 20;
            cursor: pointer;
            font-family: Georgia, serif;
            font-size: clamp(11px, 1vw, 17px);
            color: #4a2c0a;
            background: rgba(244, 223, 150, 0.85);
            border: 2px solid #8B5E3C;
            border-radius: 8px;
            padding: 0.3em 0.8em;
            transition: filter 0.15s ease;
            user-select: none;
        }}

        .ev-back-overview:hover {{
            filter: brightness(1.1);
        }}

        .ev-counter {{
            position: absolute;
            left: 50%;
            bottom: 2%;
            transform: translateX(-50%);
            z-index: 30;
            color: #f4dfaa;
            background: rgba(0, 0, 0, 0.55);
            padding: 0.25rem 0.75rem;
            border-radius: 999px;
            font-size: clamp(12px, 0.85vw, 18px);
            font-weight: 800;
            letter-spacing: 0.04em;
        }}

        {back_btn_css}

        {screen_arrow_css()}

        .ev-arrow-left {{
            left: 1.0%;
            top: 35%;
            width: 8%;
            height: 28%;
        }}

        .ev-arrow-right {{
            right: 1.0%;
            top: 35%;
            width: 8%;
            height: 28%;
        }}
        </style>
    </head>
    <body>
        <div class="ev-zoom-page">
            <div class="ev-zoom-stage">
                {back_btn_html}

                <img class="ev-zoom-bg" src="data:image/png;base64,{bg_b64}" alt="Evidence zoom">

                {evidence_img_html}

                <div class="ev-zoom-name">{item['name']}</div>
                <div class="ev-zoom-desc">{description}</div>

                <div
                    class="ev-back-overview"
                    onclick="navigate('ev_overview')"
                    role="button"
                    aria-label="Back to overview">
                    ← Overview
                </div>

                {left_arrow}
                {right_arrow}

                <div class="ev-counter">{counter_text}</div>

            </div>
        </div>
        {navigate_script()}
    </body>
    </html>
    """

    components.html(html, height=1, scrolling=False)


def show_evidence() -> None:
    if "evidence_mode" not in st.session_state:
        st.session_state.evidence_mode = "overview"
    if "evidence_index" not in st.session_state:
        st.session_state.evidence_index = 0

    num_evidence = len(EVIDENCE)
    current_index = (
        st.session_state.evidence_index % num_evidence
        if num_evidence > 0
        else 0
    )
    st.session_state.evidence_index = current_index
    mode = st.session_state.evidence_mode

    back_btn_html = get_back_button_html(btn_key="ev_back")
    back_btn_css = get_back_button_css(left="1.2%", top="2.0%", width="13%")

    st.markdown(streamlit_chrome_css("#3a1f0f"), unsafe_allow_html=True)

    if mode == "overview":
        _render_overview(back_btn_html, back_btn_css)
    else:
        _render_zoom(back_btn_html, back_btn_css, current_index, num_evidence)

    render_back_button_streamlit(btn_key="ev_back", target_page="main_menu")

    if st.button("ev_overview", key="ev_hidden_overview"):
        st.session_state.evidence_mode = "overview"
        st.rerun()

    ev_click_cols = st.columns(max(num_evidence, 1))
    for i, col in enumerate(ev_click_cols):
        if i < num_evidence:
            with col:
                if st.button(f"ev_click_{i}", key=f"ev_hidden_click_{i}"):
                    st.session_state.evidence_index = i
                    st.session_state.evidence_mode = "zoom"
                    st.rerun()

    col_prev, col_next = st.columns(2)
    with col_prev:
        if st.button("prev", key="ev_prev"):
            if num_evidence > 0:
                st.session_state.evidence_index = (current_index - 1) % num_evidence
            st.rerun()
    with col_next:
        if st.button("next", key="ev_next"):
            if num_evidence > 0:
                st.session_state.evidence_index = (current_index + 1) % num_evidence
            st.rerun()


def show_evidens() -> None:
    show_evidence()
