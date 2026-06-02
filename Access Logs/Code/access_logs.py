import base64
import html
import math
import os
import sys
from pathlib import Path

from PIL import Image
import streamlit as st
import streamlit.components.v1 as components
from sqlalchemy import create_engine, text


project_root = Path(__file__).resolve().parents[2]
back_button_code_dir = project_root / "Back to main menu" / "Code"
screen_arrows_code_dir = project_root / "Screen arrows" / "Code"
witness_file_code_dir = project_root / "Witness file" / "Code"

if str(back_button_code_dir) not in sys.path:
    sys.path.append(str(back_button_code_dir))
if str(screen_arrows_code_dir) not in sys.path:
    sys.path.append(str(screen_arrows_code_dir))
if str(witness_file_code_dir) not in sys.path:
    sys.path.append(str(witness_file_code_dir))

from back_to_main_menu import get_back_button_css, get_back_button_html, render_back_button_streamlit
from screen_arrows import screen_arrow_css, make_screen_arrow_button


ASSETS_DIR = Path(__file__).resolve().parents[1] / "Assets"

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/streamlit_db",
)


def fetch_presence_data() -> list[dict]:
    """
    Fetch presence data from the Presence table and join with Person table.
    Returns a list of dictionaries with person name, arrival time, departure time, and work status.
    """
    try:
        return fetch_presence_data_from_database()
    except Exception:
        return fetch_presence_data_from_local_persons()


def fetch_presence_data_from_database() -> list[dict]:
    engine = create_engine(DATABASE_URL)

    with engine.connect() as connection:
        query = text("""
            SELECT
                p.person_id,
                p.name,
                p.role,
                pr.arrived_at,
                pr.left_at,
                pr.was_working
            FROM Presence pr
            JOIN Person p ON pr.person_id = p.person_id
            ORDER BY pr.arrived_at ASC
        """)

        rows = connection.execute(query).fetchall()

    access_log = []
    for row in rows:
        person_id, name, role, arrived_at, left_at, was_working = row
        arrived_time = arrived_at.strftime("%H:%M") if arrived_at else ""
        left_time = left_at.strftime("%H:%M") if left_at else ""

        access_log.append({
            "person_id": person_id,
            "person": name,
            "role": role,
            "arrived": arrived_time,
            "left": left_time,
            "works_here": "Yes" if was_working else "No",
        })

    return access_log


def fetch_presence_data_from_local_persons() -> list[dict]:
    try:
        from witness_overview import PERSONS
    except ImportError:
        return []

    def looks_like_employee(role: str) -> bool:
        role_lower = role.lower()
        return "employee" in role_lower or role_lower in {"investigator", "watchmaker"}

    return [
        {
            "person_id": person.get("id", ""),
            "person": person.get("name", ""),
            "role": person.get("role", ""),
            "arrived": person.get("arrived", ""),
            "left": person.get("left", ""),
            "works_here": "Yes" if looks_like_employee(person.get("role", "")) else "No",
        }
        for person in PERSONS
    ]


# ── Adgangslog ────────────────────────────────────────────────────────────────
# Will be populated from the database when show_access_logs() is called
ACCESS_LOG: list[dict] = []

# ── Tabel-layout på billedet (i % af billedets bredde/højde) ─────────────────
# Juster x-værdierne hvis teksten ikke lander på de korrekte kolonner.
ROWS_PER_PAGE = 10

TABLE = {
    "x_person":    25.5,   # venstre kant af "Person"-kolonnen
    "x_role":      39.5,   # venstre kant af "Role"-kolonnen
    "x_arrived":   51.0,   # venstre kant af "Arrived"-kolonnen
    "x_left":      59.0,   # venstre kant af "Left"-kolonnen
    "x_working":   67.0,   # venstre kant af "Working"-kolonnen
    "y_header":    32.2,   # top af kolonneoverskrifterne (%)
    "y_first":     36.5,   # top af første datarække (%)
    "row_h":        4.3,   # højde pr. række (%)
}
# ─────────────────────────────────────────────────────────────────────────────


def image_to_base64(image_path: Path) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def get_aspect_ratio(image_path: Path) -> float:
    with Image.open(image_path) as img:
        w, h = img.size
    return w / h


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


def show_access_logs() -> None:
    global ACCESS_LOG
    
    # Fetch data from database if not already loaded
    if not ACCESS_LOG:
        ACCESS_LOG = fetch_presence_data()
    
    bg_path = ASSETS_DIR / "Access logs.png"
    if not bg_path.exists():
        st.error(f"Baggrundsbillede ikke fundet: {bg_path}")
        st.stop()

    bg_b64       = image_to_base64(bg_path)
    aspect_ratio = get_aspect_ratio(bg_path)

    total_entries = len(ACCESS_LOG)
    total_pages   = max(1, math.ceil(total_entries / ROWS_PER_PAGE))

    if "al_page" not in st.session_state:
        st.session_state.al_page = 0

    current_page = max(0, min(st.session_state.al_page, total_pages - 1))
    st.session_state.al_page = current_page

    start = current_page * ROWS_PER_PAGE
    page_entries = ACCESS_LOG[start : start + ROWS_PER_PAGE]
    
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
        aria_label="Forrige side",
    ) if show_left else ""

    right_arrow = make_screen_arrow_button(
        direction="right",
        onclick="navigate('next')",
        css_class="al-arrow-right",
        aria_label="Næste side",
    ) if show_right else ""

    counter_text = f"Side {current_page + 1} / {total_pages}" if total_pages > 1 else ""

    st.markdown(_streamlit_chrome_css(), unsafe_allow_html=True)

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
            {back_btn_html}
            <div class="al-stage">
                <img class="al-bg" src="data:image/png;base64,{bg_b64}" alt="Access Logs">
                {header_html}
                {rows_html}
                {left_arrow}
                {right_arrow}
                {f'<div class="al-counter">{counter_text}</div>' if counter_text else ""}
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
