import html
import math
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
from database_helpers import get_access_logs
from ui_helpers import get_aspect_ratio, image_to_base64, navigate_script, streamlit_chrome_css


ASSETS_DIR = assets_dir(__file__)

ROWS_PER_PAGE = 10

TABLE = {
    "x_person":    25.5,
    "x_role":      39.5,
    "x_arrived":   51.0,
    "x_left":      59.0,
    "x_working":   67.0,
    "y_header":    32.2,
    "y_first":     36.5,
    "row_h":        4.3,
}

def _escape(value: object) -> str:
    return html.escape(str(value or ""))


def _build_header_html() -> str:
    header_style = (
        "position:absolute;"
        "font-family:Georgia,serif;"
        "font-size:clamp(8px,0.95vw,15px);"
        "color:#1a0e07;"
        "font-weight:900;"
        "white-space:nowrap;"
        "z-index:10;"
        f"top:{TABLE['y_header']}%;"
    )

    return f"""
    <span style="{header_style}left:{TABLE['x_person']}%;max-width:13%;">Person</span>
    <span style="{header_style}left:{TABLE['x_role']}%;max-width:10%;">Role</span>
    <span style="{header_style}left:{TABLE['x_arrived']}%;max-width:7%;">Arrived</span>
    <span style="{header_style}left:{TABLE['x_left']}%;max-width:7%;">Left</span>
    <span style="{header_style}left:{TABLE['x_working']}%;max-width:9%;">Working</span>
    """


def _build_rows_html(page_entries: list[dict]) -> str:
    html = ""
    for i, entry in enumerate(page_entries):
        y = TABLE["y_first"] + i * TABLE["row_h"]
        person = _escape(entry.get("person", ""))
        role = _escape(entry.get("role", ""))
        arrived = _escape(entry.get("arrived", ""))
        left = _escape(entry.get("left", ""))
        works_here = _escape(entry.get("works_here", entry.get("purchased", "")))

        cell_style = (
            "position:absolute;"
            "font-family:Georgia,serif;"
            "font-size:clamp(8px,0.85vw,14px);"
            "color:#1a0e07;"
            "font-weight:600;"
            "white-space:nowrap;"
            "overflow:hidden;"
            "text-overflow:ellipsis;"
            "z-index:10;"
            f"top:{y}%;"
        )

        html += f"""
        <span style="{cell_style}left:{TABLE['x_person']}%;max-width:13%;">{person}</span>
        <span style="{cell_style}left:{TABLE['x_role']}%;max-width:10%;">{role}</span>
        <span style="{cell_style}left:{TABLE['x_arrived']}%;max-width:7%;">{arrived}</span>
        <span style="{cell_style}left:{TABLE['x_left']}%;max-width:7%;">{left}</span>
        <span style="{cell_style}left:{TABLE['x_working']}%;max-width:9%;">{works_here}</span>
        """
    
    return html


def show_access_logs() -> None:
    bg_path = ASSETS_DIR / "Access logs.png"
    if not bg_path.exists():
        st.error(f"Background image not found: {bg_path}")
        st.stop()

    bg_b64       = image_to_base64(bg_path)
    aspect_ratio = get_aspect_ratio(bg_path)

    access_log = get_access_logs()
    total_entries = len(access_log)
    total_pages   = max(1, math.ceil(total_entries / ROWS_PER_PAGE))

    if "al_page" not in st.session_state:
        st.session_state.al_page = 0

    current_page = max(0, min(st.session_state.al_page, total_pages - 1))
    st.session_state.al_page = current_page

    start = current_page * ROWS_PER_PAGE
    page_entries = access_log[start : start + ROWS_PER_PAGE]
    
    header_html = _build_header_html()
    rows_html = _build_rows_html(page_entries)

    show_left  = current_page > 0
    show_right = current_page < total_pages - 1

    back_btn_html = get_back_button_html(btn_key="al_back")
    back_btn_css  = get_back_button_css(left="1.0%", top="1.5%", width="10%")

    left_arrow = make_screen_arrow_button(
        direction="left",
        onclick="navigate('prev')",
        css_class="al-arrow-left",
        aria_label="Previous page",
    ) if show_left else ""

    right_arrow = make_screen_arrow_button(
        direction="right",
        onclick="navigate('next')",
        css_class="al-arrow-right",
        aria_label="Next page",
    ) if show_right else ""

    counter_text = f"Page {current_page + 1} / {total_pages}" if total_pages > 1 else ""

    st.markdown(streamlit_chrome_css(), unsafe_allow_html=True)

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

        .al-page {{
            width: 100vw; height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #2a1a0a;
        }}

        .al-stage {{
            position: relative;
            width: min(100vw, calc(100vh * {aspect_ratio}));
            aspect-ratio: {aspect_ratio};
        }}

        .al-bg {{
            position: absolute;
            inset: 0; width: 100%; height: 100%;
            object-fit: contain;
            z-index: 1;
            pointer-events: none;
            user-select: none;
        }}

        .al-counter {{
            position: absolute;
            left: 50%;
            bottom: 2%;
            transform: translateX(-50%);
            z-index: 20;
            color: #f4dfaa;
            background: rgba(0,0,0,0.55);
            padding: 0.2rem 0.7rem;
            border-radius: 999px;
            font-size: clamp(11px, 0.8vw, 16px);
            font-weight: 800;
            letter-spacing: 0.04em;
        }}

        {back_btn_css}

        {screen_arrow_css()}

        .al-arrow-left {{
            left: 0.5%;
            top: 35%;
            width: 6%;
            height: 30%;
        }}

        .al-arrow-right {{
            right: 0.5%;
            top: 35%;
            width: 6%;
            height: 30%;
        }}
        </style>
    </head>
    <body>
        <div class="al-page">
            <div class="al-stage">
                {back_btn_html}
                <img class="al-bg" src="data:image/png;base64,{bg_b64}" alt="Access Logs">
                {header_html}
                {rows_html}
                {left_arrow}
                {right_arrow}
                {f'<div class="al-counter">{counter_text}</div>' if counter_text else ""}
            </div>
        </div>

        {navigate_script()}
    </body>
    </html>
    """

    components.html(html, height=1, scrolling=False)

    render_back_button_streamlit(btn_key="al_back", target_page="main_menu")

    col_prev, col_next = st.columns(2)
    with col_prev:
        if st.button("prev", key="al_prev"):
            if current_page > 0:
                st.session_state.al_page = current_page - 1
            st.rerun()
    with col_next:
        if st.button("next", key="al_next"):
            if current_page < total_pages - 1:
                st.session_state.al_page = current_page + 1
            st.rerun()