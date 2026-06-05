import sys
from pathlib import Path
import random

import streamlit as st
import streamlit.components.v1 as components

from sqlalchemy import text


shared_code_dir = Path(__file__).resolve().parents[2] / "Shared" / "Code"
if str(shared_code_dir) not in sys.path:
    sys.path.append(str(shared_code_dir))

from path_helpers import PROJECT_ROOT, add_code_paths, assets_dir, code_dir
from ui_helpers import cached_image_to_base64, get_aspect_ratio, navigate_script, streamlit_chrome_css


witness_button_code_dir = code_dir("Witness shortcut")

add_code_paths(
    code_dir("Back to main menu"),
    code_dir("Picture Frame"),
    code_dir("Char Randomizer"),
    code_dir("Suspect selecter"),
    code_dir("Database"),
)
if str(witness_button_code_dir) in sys.path:
    sys.path.remove(str(witness_button_code_dir))
sys.path.insert(0, str(witness_button_code_dir))

sys.modules.pop("witness_button", None)

from back_to_main_menu import get_back_button_css, get_back_button_html, render_back_button_streamlit
from picture_frame import get_picture_frame_css, get_picture_frame_html
from witness_button import (
    get_witness_file_button_css,
    get_witness_file_button_html,
    get_witness_green_button_css,
    get_witness_overview_button_css,
    get_witness_overview_button_html,
    get_witness_red_button_css,
    get_witness_red_button_html,
    get_witness_search_button_html,
    render_witness_file_button_streamlit,
    render_witness_overview_button_streamlit,
    render_witness_red_button_streamlit,
    render_witness_search_button_streamlit,
)


try:
    from Random_char_selector import get_selected_characters
except ImportError:
    def get_selected_characters() -> list[dict]:
        return []

try:
    from Is_Suspect import get_guilty_suspect
except ImportError:
    def get_guilty_suspect() -> dict | None:
        return None

try:
    from database_helpers import (
        get_in_game_persons,
        get_persons,
        get_stolen_items,
        get_suspicious_person_ids,
        set_suspicious_flag,
        get_person
    )
except ImportError:
    def get_persons(fallback: list[dict] | None = None) -> list[dict]:
        return fallback or []

    def get_in_game_persons(fallback: list[dict] | None = None) -> list[dict]:
        return fallback or []

    def get_stolen_items(fallback: list[dict] | None = None, limit: int | None = None) -> list[dict]:
        return fallback or []

    def get_suspicious_person_ids(game_id: int) -> set[int]:
        return set()

    def set_suspicious_flag(game_id: int, person_id: int, is_suspicious: bool) -> None:
        return None

ASSETS_DIR = assets_dir(__file__)
CHARS_DIR = PROJECT_ROOT / "Characters"
BG_FILENAME = "Witness overview.png"
    
def _save_suspicious_flag(person_id: int, is_suspicious: bool) -> None:
    set_suspicious_flag(
        st.session_state.get("game_number", 0),
        person_id,
        is_suspicious,
    )


PERSONS = get_persons([])

LAYOUT = {
    "photo_left": 11.0, "photo_top": 4.5, "photo_w": 42.0, "photo_h": 46.0,
    "stmt_left": 56.0, "stmt_top": 15.9, "stmt_w": 21.5, "stmt_h": 20.0,
    "list_left": 19.5, "list_top": 52.5, "list_w": 27.5, "list_h": 34.0,
    "attr_x": 57.0,
    "attr_ys":  [45.7, 53.15, 60.6, 68.05, 75.5, 82.95],
    "attr_row_h": 5.7,
}


def _case_details() -> tuple[str, str]:
    stolen_items = get_stolen_items(limit=1)
    if not stolen_items:
        return "stolen jewelry", "12:30"

    item = stolen_items[0]
    return item.get("description", "stolen jewelry"), item.get("time_stolen", "12:30")


def get_current_game_persons() -> list[dict]:
    selected_characters = get_selected_characters()
    if selected_characters:
        return selected_characters
    in_game_persons = get_in_game_persons([])
    if in_game_persons:
        return in_game_persons
    return PERSONS

def _display_value(value: object) -> str:
    return str(value or "").strip()


def _statement_clothing_hint(clothing: object, witness_id: int | None, target_id: int | None) -> str:
    clothing_items = [
        item.strip()
        for item in str(clothing or "").split(",")
        if item.strip()
    ]
    if not clothing_items:
        return ""

    seed = f"{witness_id or 0}:{target_id or 0}:{'|'.join(clothing_items)}"
    picker = random.Random(seed)
    count = min(len(clothing_items), picker.randint(1, 3))
    return ", ".join(picker.sample(clothing_items, count))


def _statement_for_person(person: dict | None) -> str:
    if person is None:
        return ""

    guilty = get_guilty_suspect()
    if not guilty:
        guilty = next(
            (candidate for candidate in get_selected_characters() if candidate.get("is_suspect")),
            None,
        )
    template = person.get("statement", "")
    if not guilty or not template:
        return person.get("statement", "")

    clue_target = guilty
    if person.get("truthfull") is False:
        candidates = [
            candidate
            for candidate in get_current_game_persons()
            if candidate.get("id") != guilty.get("id")
        ]
        if candidates:
            clue_target = candidates[person.get("id", 0) % len(candidates)]

    stolen_item, crime_time = _case_details()

    replacements = {
        "{{culprit_hair_color}}": _display_value(clue_target.get("hair")).lower(),
        "{{culprit_eye_color}}": _display_value(clue_target.get("eyes")).lower(),
        "{{culprit_skin_color}}": _display_value(clue_target.get("skin")).lower(),
        "{{culprit_clothing}}": _statement_clothing_hint(
            clue_target.get("clothing"),
            person.get("id"),
            clue_target.get("id"),
        ).lower(),
        "{{culprit_gender}}": _display_value(clue_target.get("gender")).lower(),
        "{{crime_time}}": crime_time,
        "{{stolen_item}}": stolen_item,
    }

    statement = template
    for placeholder, value in replacements.items():
        statement = statement.replace(placeholder, value)
    return statement


def get_witness_statement(person: dict | None) -> str:
    return _statement_for_person(person)


def _build_list_html(selected_id: int, suspicious_ids: set, persons: list[dict]) -> str:
    header = (
        f'<div class="wo-row wo-header">'
        f'<span class="wo-name">Name</span>'
        f'<span class="wo-role">Role</span>'
        f'<span class="wo-check-header">Suspect</span>'
        f'</div>'
    )
    rows = ""
    for p in persons:
        sel_cls  = "wo-selected"   if p["id"] == selected_id  else ""
        susp_cls = "wo-suspicious" if p["id"] in suspicious_ids else ""
        check    = "X"              if p["id"] in suspicious_ids else ""
        rows += (
            f'<div class="wo-row {sel_cls} {susp_cls}" '
            f'onclick="selectPerson({p["id"]})">'
            f'<span class="wo-name">{p["name"]}</span>'
            f'<span class="wo-role">{p["role"]}</span>'
            f'<span class="wo-check" onclick="event.stopPropagation();toggleSusp({p["id"]})">{check}</span>'
            f'</div>'
        )
    return header + rows



def _build_statement_html(person: dict | None) -> str:
    if person is None:
        return ""
    stmt = _statement_for_person(person).replace("<", "&lt;").replace(">", "&gt;")
    l = LAYOUT
    return (
        f'<div style="position:absolute;left:{l["stmt_left"]}%;top:{l["stmt_top"]}%;'
        f'width:{l["stmt_w"]}%;height:{l["stmt_h"]}%;z-index:8;overflow:hidden;'
        f'font-family:Georgia,serif;font-size:clamp(7px,0.72vw,11px);'
        f'color:#2a1a0a;'
        f'line-height:2.6vh;word-break:break-word;'
        f'transform:rotate(-0.5deg);transform-origin:left top;'
        f'white-space:pre-wrap;">{stmt}</div>'
    )


def _build_attrs_html(person: dict | None) -> str:
    if person is None:
        return ""
    attrs = [
        "2026-05-12",
        "Maison Aurora Jewelry",
        f"{person.get('arrived','-')} - {person.get('left','-')}",
        person.get("role", ""),
        f"{person.get('hair','')} hair - {person.get('eyes','')} eyes - {person.get('skin','')} skin",
        person.get("clothing", ""),
    ]
    l = LAYOUT
    x    = l["attr_x"]
    rh   = l["attr_row_h"]
    html = ""
    for text, y in zip(attrs, l["attr_ys"]):
        safe = text.replace("<", "&lt;").replace(">", "&gt;")
        html += (
            f'<div style="position:absolute;left:{x}%;top:{y}%;'
            f'width:25%;max-height:{rh}%;z-index:8;pointer-events:none;overflow:hidden;'
            f'font-family:Georgia,serif;font-size:clamp(7px,0.68vw,10.5px);'
            f'color:#2a1a0a;font-weight:600;'
            f'line-height:1.18;word-break:break-word;white-space:normal;">'
            f'{safe}</div>'
        )
    return html


def show_witness_overview() -> None:
    bg_path = ASSETS_DIR / BG_FILENAME
    if not bg_path.exists():
        st.error(
            f"Background image not found: {bg_path}\n\n"
            f"Save the image as **{BG_FILENAME}** in:\n`{ASSETS_DIR}`"
        )
        st.stop()

    bg_b64 = cached_image_to_base64(bg_path)
    aspect = get_aspect_ratio(bg_path)

    game_persons = get_current_game_persons()
    game_person_ids = {p["id"] for p in game_persons}

    if "wo_selected" not in st.session_state:
        st.session_state.wo_selected = game_persons[0]["id"]

    if "wo_suspicious" not in st.session_state:
        st.session_state.wo_suspicious = get_suspicious_person_ids(
            st.session_state.get("game_number", 0)
        )

    if st.session_state.wo_selected not in game_person_ids:
        st.session_state.wo_selected = game_persons[0]["id"]

    st.session_state.wo_suspicious = set(st.session_state.wo_suspicious) & game_person_ids

    selected_id    = st.session_state.wo_selected
    suspicious_ids = st.session_state.wo_suspicious
    person         = get_person(game_persons, selected_id)

    l = LAYOUT
    list_rows = _build_list_html(selected_id, suspicious_ids, game_persons)
    stmt_html = _build_statement_html(person)
    attrs_html = _build_attrs_html(person)

    if person:
        zoom_path     = CHARS_DIR / f"Char_zoom_{person['id']}.png"
        standard_path = CHARS_DIR / f"Char_{person['id']}.png"
        char_path = zoom_path if zoom_path.exists() else standard_path
    else:
        char_path = None
    frame_css  = get_picture_frame_css(
        css_class="wo-frame",
        left=f"{l['photo_left']}%",
        top=f"{l['photo_top']}%",
        width=f"{l['photo_w']}%",
        height=f"{l['photo_h']}%",
        photo_fit="contain",
    )
    frame_html = get_picture_frame_html(
        photo_path=char_path if char_path and char_path.exists() else None,
        css_class="wo-frame",
        alt=person.get("name", "") if person else "",
    )

    back_btn_html = get_back_button_html(btn_key="wo_back")
    back_btn_css  = get_back_button_css(left="1.0%", top="1.0%", width="9%")
    witness_tab_html = get_witness_overview_button_html(btn_key="wo_tab_overview")
    witness_tab_css = get_witness_overview_button_css(
        css_class="witness-overview-tab",
        top="27.7%",
        selected=True,
    )
    witness_file_tab_html = get_witness_file_button_html(btn_key="wo_tab_file")
    witness_file_tab_css = get_witness_file_button_css(
        css_class="witness-file-tab",
        top="46.8%",
        selected=False,
    )
    witness_red_tab_html = get_witness_red_button_html(btn_key="wo_tab_suspects")
    witness_red_tab_css = get_witness_red_button_css(
        css_class="witness-red-tab",
        top="7.6%",
    )
    witness_green_tab_html = get_witness_search_button_html(
        btn_key="wo_tab_search",
        css_class="witness-green-tab",
        label="Witness Search",
    )
    witness_green_tab_css = get_witness_green_button_css(
        css_class="witness-green-tab",
        top="68.3%",
    )

    st.markdown(streamlit_chrome_css(), unsafe_allow_html=True)

    html = f"""
    <!DOCTYPE html><html><head>
    <style>
    html,body{{margin:0;padding:0;width:100vw;height:100vh;overflow:hidden;background:#2a1a0a;}}

    .wo-page{{width:100vw;height:100vh;display:flex;justify-content:center;align-items:center;background:#2a1a0a;overflow:hidden;}}

    .wo-stage{{
        position:relative;
        width: min(100vw, calc(100vh * {aspect}));
        height: min(100vh, calc(100vw / {aspect}));
    }}

    .wo-bg{{position:absolute;inset:0;width:100%;height:100%;object-fit:fill;z-index:1;pointer-events:none;user-select:none;}}

    .wo-list{{
        position:absolute;
        left:{LAYOUT["list_left"]}%;top:{LAYOUT["list_top"]}%;
        width:{LAYOUT["list_w"]}%;height:{LAYOUT["list_h"]}%;
        z-index:10;
        overflow-y:auto;
        overflow-x:hidden;
        scrollbar-width:thin;
        scrollbar-color:rgba(100,60,20,0.3) transparent;
        padding-right:10px;
        box-sizing:border-box;
        border-top: 1px solid rgba(110, 70, 25, 0.4);
    }}
    .wo-list::-webkit-scrollbar{{width:3px;}}
    .wo-list::-webkit-scrollbar-thumb{{background:rgba(100,60,20,0.35);border-radius:2px;}}

    .wo-row{{
        display:flex;align-items:center;
        padding:0 1%;
        cursor:pointer;
        height:3.8vh;
        border-bottom: 1px solid rgba(110, 70, 25, 0.35);
        transition:background 0.12s ease;
        box-sizing:border-box;
    }}
    .wo-row:hover{{background:rgba(180,120,40,0.15);}}
    .wo-header{{background:rgba(110,70,25,0.5)!important;cursor:default;border-bottom:2px solid rgba(110,70,25,0.8);padding:0.5% 1%;}}
    .wo-header:hover{{background:rgba(110,70,25,0.5)!important;}}
    .wo-header .wo-name,.wo-header .wo-role,.wo-header .wo-check-header{{font-weight:700;color:#1a0e07;font-style:normal;}}
    .wo-check-header{{width:1.3em;height:1.3em;display:flex;align-items:center;justify-content:center;font-size:clamp(6px,0.7vw,11px);color:#8B5E3C;font-weight:bold;flex-shrink:0;background:transparent;border:none;}}
    .wo-selected{{background:rgba(180,120,40,0.28)!important;}}
    .wo-suspicious .wo-name{{color:#8B2020;font-weight:700;}}

    .wo-name{{
        width:52%;
        flex-shrink:0;
        font-family:Georgia,serif;
        font-size:clamp(7px,0.76vw,12px);
        color:#2a1a0a;
        white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
    }}
    .wo-role{{
        flex:1;
        font-family:Georgia,serif;
        font-size:clamp(6px,0.63vw,10px);
        color:#5a3a18;
        font-style:italic;
        white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
    }}
    .wo-check{{
        width:1.3em;height:1.3em;
        border:1.5px solid #8B5E3C;
        border-radius:3px;
        display:flex;align-items:center;justify-content:center;
        font-size:clamp(6px,0.7vw,11px);
        color:#8B2020;font-weight:bold;
        cursor:pointer;flex-shrink:0;
        background:rgba(255,245,220,0.6);
        transition:background 0.12s ease;
    }}
    .wo-check:hover{{background:rgba(255,200,100,0.5);}}

    {back_btn_css}

    {frame_css}

    {witness_tab_css}

    {witness_file_tab_css}

    {witness_red_tab_css}

    {witness_green_tab_css}
    </style></head>
    <body>
    <div class="wo-page">
        <div class="wo-stage">
            {back_btn_html}

            <img class="wo-bg" src="data:image/png;base64,{bg_b64}" alt="Witness overview">

            {frame_html}

            {stmt_html}

            {attrs_html}

            {witness_tab_html}

            {witness_file_tab_html}

            {witness_red_tab_html}
            {witness_green_tab_html}

            <div class="wo-list">{list_rows}</div>

        </div>
    </div>

    {navigate_script()}
    <script>
    function selectPerson(id) {{ navigate('wo_sel_' + id); }}
    function toggleSusp(id)   {{ navigate('wo_tog_' + id); }}
    </script>
    </body></html>
    """

    components.html(html, height=1, scrolling=False)

    render_back_button_streamlit(btn_key="wo_back", target_page="main_menu")
    render_witness_overview_button_streamlit(btn_key="wo_tab_overview", target_page="witnesses")
    render_witness_file_button_streamlit(btn_key="wo_tab_file", target_page="witness_file")
    render_witness_red_button_streamlit(btn_key="wo_tab_suspects", target_page="suspects")
    render_witness_search_button_streamlit(btn_key="wo_tab_search", target_page="witness_search")

    sel_cols = st.columns(len(game_persons))
    for col, p in zip(sel_cols, game_persons):
        with col:
            if st.button(f"wo_sel_{p['id']}", key=f"wo_hidden_sel_{p['id']}"):
                st.session_state.wo_selected = p["id"]
                st.rerun()

    tog_cols = st.columns(len(game_persons))
    for col, p in zip(tog_cols, game_persons):
        with col:
            if st.button(f"wo_tog_{p['id']}", key=f"wo_hidden_tog_{p['id']}"):
                susp = set(st.session_state.wo_suspicious)
                if p["id"] in susp:
                    susp.discard(p["id"])
                    _save_suspicious_flag(p["id"], False)
                else:
                    susp.add(p["id"])
                    _save_suspicious_flag(p["id"], True)
                st.session_state.wo_suspicious = susp & game_person_ids
                st.rerun()
