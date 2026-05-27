import base64
import math
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

# Tilføj stjålne genstande her.
STOLEN_ITEMS = [
    {
        "name": "",
        "image_filename": None,   # filnavn i Assets-mappen, eller None
    },
    # Tilføj flere genstande her...
]

# Side 1 (start page): titel dækker venstre øverste halvdel → 2 slots i bunden til venstre + 4 til højre = 6 slots
START_PAGE_SLOTS = 6
START_PAGE_BOXES = [
    # Venstre side — under titelbanneret
    ( 9.0, 48.0, 14.0, 38.0),   # Slot 0
    (25.5, 48.0, 14.0, 38.0),   # Slot 1
    # Højre side — 2×2 gitter
    (54.5,  5.5, 16.0, 33.0),   # Slot 2
    (73.0,  5.5, 16.0, 33.0),   # Slot 3
    (54.5, 50.0, 16.0, 37.0),   # Slot 4
    (73.0, 50.0, 16.0, 37.0),   # Slot 5
]

# Side 2+ (new page): 8 slots i 2 rækker × 4 kolonner
NEW_PAGE_SLOTS = 8
NEW_PAGE_BOXES = [
    ( 8.0,  4.5, 17.0, 33.0),   # Række 1, Kol 1
    (27.0,  4.5, 17.0, 33.0),   # Række 1, Kol 2
    (54.0,  4.5, 16.5, 33.0),   # Række 1, Kol 3
    (73.0,  4.5, 16.5, 33.0),   # Række 1, Kol 4
    ( 8.0, 47.0, 17.0, 38.0),   # Række 2, Kol 1
    (27.0, 47.0, 17.0, 38.0),   # Række 2, Kol 2
    (54.0, 47.0, 16.5, 38.0),   # Række 2, Kol 3
    (73.0, 47.0, 16.5, 38.0),   # Række 2, Kol 4
]


def image_to_base64(image_path: Path) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def get_aspect_ratio(image_path: Path) -> float:
    with Image.open(image_path) as img:
        w, h = img.size
    return w / h


def _total_pages(num_items: int) -> int:
    if num_items <= START_PAGE_SLOTS:
        return 1
    return 1 + math.ceil((num_items - START_PAGE_SLOTS) / NEW_PAGE_SLOTS)


def _items_on_page(page_index: int, all_items: list) -> list:
    """Returnerer de genstande der vises på den givne albemside (0-indekseret)."""
    if page_index == 0:
        return all_items[:START_PAGE_SLOTS]
    start = START_PAGE_SLOTS + (page_index - 1) * NEW_PAGE_SLOTS
    return all_items[start : start + NEW_PAGE_SLOTS]


def _streamlit_chrome_css() -> str:
    return """
        <style>
        html, body, .stApp {
            margin: 0 !important; padding: 0 !important;
            overflow: hidden !important; background: #3a2010 !important;
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
    function navigate(page) {
        var buttons = window.parent.document.querySelectorAll('button');
        for (var i = 0; i < buttons.length; i++) {
            if (buttons[i].innerText.trim() === page) {
                buttons[i].click();
                return;
            }
        }
    }
    </script>
    """


def _build_slots_html(page_items: list, boxes: list) -> str:
    """Laver HTML for alle billedslots på en albumside."""
    html = ""
    for slot_index, (left, top, width, height) in enumerate(boxes):
        if slot_index >= len(page_items):
            break
        item = page_items[slot_index]
        img_html = ""
        if item.get("image_filename"):
            img_path = ASSETS_DIR / item["image_filename"]
            if img_path.exists():
                b64 = image_to_base64(img_path)
                img_html = f'<img src="data:image/png;base64,{b64}" alt="{item.get("name", "")}">'
        name = item.get("name", "")
        html += f"""
        <div
            class="si-slot"
            style="left:{left}%;top:{top}%;width:{width}%;height:{height}%;"
            title="{name}">
            {img_html}
            {f'<span class="si-slot-label">{name}</span>' if name else ""}
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
        st.error(f"Baggrundsbillede ikke fundet: {bg_path}")
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
        aria_label="Forrige side",
    ) if show_left else ""

    right_arrow = make_screen_arrow_button(
        direction="right",
        onclick="navigate('next')",
        css_class="si-arrow-right",
        aria_label="Næste side",
    ) if show_right else ""

    counter_text = f"Side {page_index + 1} / {total_pages}"

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
            {back_btn_html}
            <div class="si-stage">
                <img class="si-bg" src="data:image/png;base64,{bg_b64}" alt="Stolen items album">
                {slots_html}
                {left_arrow}
                {right_arrow}
                <div class="si-counter">{counter_text}</div>
            </div>
        </div>
        {_navigate_js()}
    </body>
    </html>
    """

    components.html(html, height=1, scrolling=False)


def show_stolen_items() -> None:
    if "si_page" not in st.session_state:
        st.session_state.si_page = 0

    num_items = len(STOLEN_ITEMS)
    total_pages = _total_pages(num_items)
    current_page = max(0, min(st.session_state.si_page, total_pages - 1))
    st.session_state.si_page = current_page

    page_items = _items_on_page(current_page, STOLEN_ITEMS)

    back_btn_html = get_back_button_html(btn_key="si_back")
    back_btn_css = get_back_button_css(left="1.2%", top="2.0%", width="13%")

    st.markdown(_streamlit_chrome_css(), unsafe_allow_html=True)

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
