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
from database_helpers import get_stolen_items
from ui_helpers import cached_image_to_base64, get_aspect_ratio, image_to_base64, navigate_script, streamlit_chrome_css


ASSETS_DIR = assets_dir(__file__)


START_PAGE_SLOTS = 6
START_PAGE_BOXES = [
    (15.0, 41.0, 14.0, 38.0),
    (32.0, 39.0, 14.0, 38.0),
    (50.0, 6.0, 16.0, 33.0),
    (68.0, 6.0, 16.0, 33.0),
    (51.0, 42.0, 16.0, 37.0),
    (69.0, 42.0, 16.0, 37.0),
]

NEW_PAGE_SLOTS = 8
NEW_PAGE_BOXES = [
    (8.0, 4.5, 17.0, 33.0),
    (27.0, 4.5, 17.0, 33.0),
    (54.0, 4.5, 16.5, 33.0),
    (73.0, 4.5, 16.5, 33.0),
    (8.0, 47.0, 17.0, 38.0),
    (27.0, 47.0, 17.0, 38.0),
    (54.0, 47.0, 16.5, 38.0),
    (73.0, 47.0, 16.5, 38.0),
]


def _get_stolen_items() -> list[dict]:
    return get_stolen_items(limit=6)


def _total_pages(num_items: int) -> int:
    if num_items <= START_PAGE_SLOTS:
        return 1
    return 1 + math.ceil((num_items - START_PAGE_SLOTS) / NEW_PAGE_SLOTS)


def _items_on_page(page_index: int, all_items: list) -> list:
    if page_index == 0:
        return all_items[:START_PAGE_SLOTS]
    start = START_PAGE_SLOTS + (page_index - 1) * NEW_PAGE_SLOTS
    return all_items[start : start + NEW_PAGE_SLOTS]


def _build_slots_html(page_items: list, boxes: list) -> str:
    html = ""
    for slot_index, (left, top, width, height) in enumerate(boxes):
        if slot_index >= len(page_items):
            break
        item = page_items[slot_index]
        img_html = ""
        if item.get("image_filename"):
            img_path = ASSETS_DIR / item["image_filename"]
            if img_path.exists():
                b64 = cached_image_to_base64(img_path)
                img_html = f'<img src="data:image/png;base64,{b64}" alt="{item.get("description", "")}" style="width:85%;height:70%;object-fit:contain;margin:0 auto;">'
        
        description = item.get("description", "")
        time_stolen = item.get("time_stolen", "")
        
        html += f"""
        <div
            class="si-slot"
            style="left:{left}%;top:{top}%;width:{width}%;height:{height}%;display:flex;flex-direction:column;align-items:center;justify-content:flex-start;padding-top:3%;">
            {img_html}
            <div style="text-align:center;font-size:0.75vw;color:#d4a574;margin-top:2%;width:90%;">
                <div style="font-weight:bold;line-height:1.1;font-size:0.7vw;">{description}</div>
                <div style="font-size:0.6vw;color:#a0826d;margin-top:1%;">Stolen: {time_stolen}</div>
            </div>
        </div>
        """
    return html


def _render_page(
    back_btn_html: str,
    back_btn_css: str,
    page_index: int,
    total_pages: int,
    page_items: list,
) -> None:
    is_start = page_index == 0
    bg_filename = "Stolen items start page.png" if is_start else "Stolen items new page.png"
    bg_path = ASSETS_DIR / bg_filename

    if not bg_path.exists():
        st.error(f"Background image not found: {bg_path}")
        st.stop()

    bg_b64 = image_to_base64(bg_path)
    aspect_ratio = get_aspect_ratio(bg_path)
    boxes = START_PAGE_BOXES if is_start else NEW_PAGE_BOXES
    slots_html = _build_slots_html(page_items, boxes)

    show_left  = page_index > 0
    show_right = page_index < total_pages - 1

    left_arrow = make_screen_arrow_button(
        direction="left",
        onclick="navigate('prev')",
        css_class="si-arrow-left",
        aria_label="Previous page",
    ) if show_left else ""

    right_arrow = make_screen_arrow_button(
        direction="right",
        onclick="navigate('next')",
        css_class="si-arrow-right",
        aria_label="Next page",
    ) if show_right else ""

    counter_text = f"Page {page_index + 1} / {total_pages}"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
        html, body {{
            margin: 0; padding: 0;
            width: 100vw; height: 100vh;
            overflow: hidden;
            background: #3a2010;
        }}

        .si-page {{
            width: 100vw; height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #3a2010;
        }}

        .si-stage {{
            position: relative;
            width: min(100vw, calc(100vh * {aspect_ratio}));
            aspect-ratio: {aspect_ratio};
        }}

        .si-bg {{
            position: absolute;
            inset: 0; width: 100%; height: 100%;
            object-fit: contain;
            z-index: 1;
            pointer-events: none;
            user-select: none;
        }}

        .si-slot {{
            position: absolute;
            z-index: 5;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }}

        .si-slot img {{
            width: 100%;
            height: 88%;
            object-fit: contain;
            pointer-events: none;
            user-select: none;
        }}

        .si-slot-label {{
            display: block;
            width: 100%;
            text-align: center;
            font-family: Georgia, serif;
            font-size: clamp(7px, 0.75vw, 13px);
            color: #2a1a0a;
            font-weight: 600;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            padding: 0 4%;
            box-sizing: border-box;
            margin-top: 2%;
        }}

        .si-counter {{
            position: absolute;
            left: 50%;
            bottom: 1.5%;
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

        .si-arrow-left {{
            left: 0.5%;
            top: 30%;
            width: 7%;
            height: 40%;
        }}

        .si-arrow-right {{
            right: 0.5%;
            top: 30%;
            width: 7%;
            height: 40%;
        }}
        </style>
    </head>
    <body>
        <div class="si-page">
            <div class="si-stage">
                {back_btn_html}
                <img class="si-bg" src="data:image/png;base64,{bg_b64}" alt="Stolen items album">
                {slots_html}
                {left_arrow}
                {right_arrow}
                <div class="si-counter">{counter_text}</div>
            </div>
        </div>
        {navigate_script()}
    </body>
    </html>
    """

    components.html(html, height=1, scrolling=False)


def show_stolen_items() -> None:
    if "si_page" not in st.session_state:
        st.session_state.si_page = 0

    all_items = _get_stolen_items()
    
    num_items = len(all_items)
    total_pages = _total_pages(num_items)
    current_page = max(0, min(st.session_state.si_page, total_pages - 1))
    st.session_state.si_page = current_page

    page_items = _items_on_page(current_page, all_items)

    back_btn_html = get_back_button_html(btn_key="si_back")
    back_btn_css = get_back_button_css(left="1.2%", top="2.0%", width="13%")

    st.markdown(streamlit_chrome_css("#3a2010"), unsafe_allow_html=True)

    _render_page(back_btn_html, back_btn_css, current_page, total_pages, page_items)

    render_back_button_streamlit(btn_key="si_back", target_page="main_menu")

    col_prev, col_next = st.columns(2)
    with col_prev:
        if st.button("prev", key="si_prev"):
            if current_page > 0:
                st.session_state.si_page = current_page - 1
            st.rerun()
    with col_next:
        if st.button("next", key="si_next"):
            if current_page < total_pages - 1:
                st.session_state.si_page = current_page + 1
            st.rerun()
