import html
import sys
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


shared_code_dir = Path(__file__).resolve().parents[2] / "Shared" / "Code"
if str(shared_code_dir) not in sys.path:
    sys.path.append(str(shared_code_dir))

from path_helpers import PROJECT_ROOT, add_code_paths, assets_dir, code_dir
from ui_helpers import (
    cached_image_to_base64,
    get_aspect_ratio,
    robust_navigation_script,
    streamlit_chrome_css,
)


add_code_paths(
    code_dir("Back to main menu"),
    code_dir("Char Randomizer"),
    code_dir("Suspect selecter"),
    code_dir("Database"),
)

from back_to_main_menu import get_back_button_css, get_back_button_html, render_back_button_streamlit

try:
    suspects_dir = code_dir("Suspects")
    if str(suspects_dir) not in sys.path:
        sys.path.append(str(suspects_dir))
    from suspects import SUSPECTS, _person_to_suspect
except ImportError:
    SUSPECTS = []
    _person_to_suspect = None

try:
    from database_helpers import get_suspicious_person_ids, save_arrest_guess
except ImportError:
    def get_suspicious_person_ids(game_id: int) -> set[int]:
        return set()

    def save_arrest_guess(game_id: int, person_id: int, is_correct: bool) -> None:
        return None

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

ASSETS_DIR = assets_dir(__file__)
CHARS_DIR = PROJECT_ROOT / "Characters"
ARROW_ASSETS_DIR = PROJECT_ROOT / "Screen arrows" / "Assets"

LEFT_FILE_IMAGE = ASSETS_DIR / "Arrest_person_file_left.png"
RIGHT_FILE_IMAGE = ASSETS_DIR / "Arrest_person_file_right.png"
CONFIRM_IMAGE = ASSETS_DIR / "Confirm_arrest.png"
LEFT_ARROW_IMAGE = ARROW_ASSETS_DIR / "Arrest_left_arrow.png"
RIGHT_ARROW_IMAGE = ARROW_ASSETS_DIR / "Arrest_right_arrow.png"
SUSPECTS_PER_PAGE = 2

_LEFT = {
    "file_image": LEFT_FILE_IMAGE,
    "file_left": 22.0, "file_top": 13.8, "file_w": 35.6, "file_h": 77.4,
    "photo_left": 30.5, "photo_top": 21.2, "photo_w": 20.8, "photo_h": 30.4,
    "click_x": 22.0, "click_y": 13.8, "click_w": 35.6, "click_h": 77.4,
    "text_fields": {
        "full_name": {"x": 36.1, "y": 54.0, "w": 17.0},
        "occupation": {"x": 36.1, "y": 57.7, "w": 17.0},
        "age": {"x": 32.1, "y": 60.8, "w": 8.0},
        "distinguishing_features": {
            "x": 40.5, "y": 64.2, "w": 7.0, "line_h": 1.8,
            "first_line_chars": 34, "line2_x": 29.1, "line2_y_offset": 3.0, "line2_w": 20.0,
        },
        "alibi": {
            "x": 32.1, "y": 71.6, "w": 17.0, "line_h": 1.8,
            "first_line_chars": 32, "line2_x": 29.1, "line2_y_offset": 3.7, "line2_w": 20.0,
        },
    },
}
_RIGHT = {
    "file_image": RIGHT_FILE_IMAGE,
    "file_left": 50.5, "file_top": 13.8, "file_w": 35.6, "file_h": 77.4,
    "photo_left": 58.0, "photo_top": 21.2, "photo_w": 20.8, "photo_h": 30.4,
    "click_x": 50.5, "click_y": 13.8, "click_w": 35.6, "click_h": 77.4,
    "text_fields": {
        "full_name": {"x": 64.8, "y": 54.0, "w": 17.0},
        "occupation": {"x": 64.8, "y": 57.7, "w": 17.0},
        "age": {"x": 60.8, "y": 60.8, "w": 8.0},
        "distinguishing_features": {
            "x": 69.0, "y": 64.2, "w": 7.0, "line_h": 1.8,
            "first_line_chars": 24, "line2_x": 57.8, "line2_y_offset": 3.0, "line2_w": 20.0,
        },
        "alibi": {
            "x": 60.8, "y": 71.6, "w": 17.0, "line_h": 1.8,
            "first_line_chars": 34, "line2_x": 57.8, "line2_y_offset": 3.7, "line2_w": 20.0,
        },
    },
}


def _asset_data_url(path: Path) -> str:
    if not path.exists():
        return ""
    return f"data:image/png;base64,{cached_image_to_base64(path)}"


def _get_arrest_candidates() -> list[dict]:
    selected_characters = get_selected_characters()
    suspicious_ids = set(st.session_state.get("wo_suspicious", set()))
    if not suspicious_ids:
        suspicious_ids = get_suspicious_person_ids(st.session_state.get("game_number", 0))
        if suspicious_ids:
            st.session_state.wo_suspicious = suspicious_ids

    if selected_characters and _person_to_suspect is not None:
        candidates = selected_characters
        if suspicious_ids:
            candidates = [
                character
                for character in selected_characters
                if character.get("id") in suspicious_ids
            ]
        return [_make_arrest_candidate(character) for character in candidates]

    candidates = SUSPECTS
    if suspicious_ids:
        candidates = [
            suspect
            for suspect in SUSPECTS
            if suspect.get("id") in suspicious_ids
        ]
    return [_make_arrest_candidate(suspect) for suspect in candidates]


def _arrest_photo_path(person_id: int | None, fallback: str | None = None) -> str | None:
    if person_id is not None:
        zoom_path = CHARS_DIR / f"Char_zoom_{person_id}.png"
        standard_path = CHARS_DIR / f"Char_{person_id}.png"
        if zoom_path.exists():
            return str(zoom_path)
        if standard_path.exists():
            return str(standard_path)
    return fallback


def _make_arrest_candidate(character: dict) -> dict:
    if _person_to_suspect is not None and "full_name" not in character:
        candidate = _person_to_suspect(character)
    else:
        candidate = dict(character)

    person_id = candidate.get("id") or character.get("id")
    candidate["photo"] = _arrest_photo_path(person_id, candidate.get("photo"))
    return candidate


def _is_correct_arrest(arrested: dict) -> bool:
    guilty = get_guilty_suspect()
    if guilty:
        arrested_id = arrested.get("id")
        guilty_id = guilty.get("id")
        if arrested_id is not None and guilty_id is not None:
            return arrested_id == guilty_id
        return arrested.get("full_name") == guilty.get("name")

    return bool(arrested.get("is_suspect"))


def _get_guilty_result(candidates: list[dict], arrested: dict) -> tuple[str, str | None]:
    guilty = get_guilty_suspect()
    if guilty:
        guilty_id = guilty.get("id")
        matching_candidate = next(
            (
                candidate
                for candidate in candidates
                if guilty_id is not None and candidate.get("id") == guilty_id
            ),
            None,
        )
        if matching_candidate:
            return matching_candidate.get("full_name", ""), matching_candidate.get("photo")
        return guilty.get("name", ""), _arrest_photo_path(guilty_id, guilty.get("photo"))

    return arrested.get("full_name", ""), arrested.get("photo")


def _split_first_line(text: str, max_chars: int | None) -> tuple[str, str]:
    text = " ".join(text.split())
    if not text:
        return "", ""

    if max_chars is None or len(text) <= max_chars:
        return text, ""

    split_at = text.rfind(" ", 0, max_chars + 1)
    if split_at <= 0:
        split_at = max_chars

    return text[:split_at].strip(), text[split_at:].strip()


def _first_line_char_limit(field: dict) -> int | None:
    width_based_limit = max(6, round(float(field.get("w", 0)) * 3.0))
    manual_limit = field.get("first_line_chars")
    if manual_limit is None:
        return width_based_limit
    return min(int(manual_limit), width_based_limit)


def _card_html(suspect: dict | None, cfg: dict) -> str:
    if suspect is None:
        return ""

    file_url = _asset_data_url(cfg["file_image"])
    if not file_url:
        return ""

    suspect_name = html.escape(suspect.get("full_name", ""))
    selected_class = cfg.get("selected_class", "")

    file_html = (
        f'<button class="ar-file-card {selected_class}" '
        f'style="left:{cfg["click_x"]}%;top:{cfg["click_y"]}%;'
        f'width:{cfg["click_w"]}%;height:{cfg["click_h"]}%;" '
        f'onclick="navigate(\'ar_select_{cfg["index"]}\')" '
        f'aria-label="Select {suspect_name}">'
        f'</button>'
        f'<img class="ar-file-image {selected_class}" '
        f'style="left:{cfg["file_left"]}%;top:{cfg["file_top"]}%;'
        f'width:{cfg["file_w"]}%;height:{cfg["file_h"]}%;" '
        f'src="{file_url}" alt="Suspect file">'
    )

    photo_html = ""
    if suspect.get("photo"):
        p = Path(suspect["photo"])
        if p.exists():
            photo_html = (
                f'<img style="position:absolute;left:{cfg["photo_left"]}%;top:{cfg["photo_top"]}%;'
                f'width:{cfg["photo_w"]}%;height:{cfg["photo_h"]}%;'
                f'object-fit:contain;z-index:8;pointer-events:none;"'
                f' src="data:image/png;base64,{cached_image_to_base64(p)}" alt="photo">'
            )

    single_line_style = (
        "position:absolute;z-index:8;font-family:Georgia,serif;"
        "font-size:clamp(7px,0.8vw,13px);color:#1a0e07;font-weight:600;"
        "white-space:nowrap;overflow:hidden;text-overflow:ellipsis;pointer-events:none;"
    )

    multiline_style = (
        "position:absolute;z-index:8;font-family:Georgia,serif;"
        "font-size:clamp(7px,0.8vw,13px);color:#1a0e07;font-weight:600;"
        "white-space:normal;overflow:hidden;pointer-events:none;"
        "overflow-wrap:break-word;word-break:normal;"
    )

    multiline_first_line_style = (
        "position:absolute;z-index:8;font-family:Georgia,serif;"
        "font-size:clamp(7px,0.8vw,13px);color:#1a0e07;font-weight:600;"
        "white-space:nowrap;overflow:visible;pointer-events:none;"
    )

    def field_html(field_key: str, value: object, multiline: bool = False) -> str:
        field = cfg["text_fields"][field_key]
        raw_text = str(value or "")
        style = multiline_style if multiline else single_line_style
        if multiline and ("line2_x" in field or "\n" in raw_text):
            if "\n" in raw_text:
                first_line, rest = raw_text.split("\n", 1)
            else:
                first_line, rest = _split_first_line(raw_text, _first_line_char_limit(field))

            first_line = html.escape(first_line.strip())
            rest = html.escape(rest.strip()).replace("\n", "<br>")
            second_x = field.get("line2_x", field["x"])
            second_y = field["y"] + field.get("line2_y_offset", 2.2)
            second_w = field.get("line2_w", field["w"])
            second_span = ""
            if rest:
                second_span = (
                    f'<span style="{multiline_style}left:{second_x}%;top:{second_y}%;'
                    f'width:{second_w}%;line-height:{field.get("line_h", 1.12)};">'
                    f'{rest}</span>'
                )

            return (
                f'<span style="{multiline_first_line_style}left:{field["x"]}%;top:{field["y"]}%;'
                f'width:{field["w"]}%;line-height:{field.get("line_h", 1.12)};">'
                f'{first_line}</span>'
                + second_span
            )

        text = html.escape(raw_text).replace("\n", "<br>")
        return (
            f'<span style="{style}left:{field["x"]}%;top:{field["y"]}%;'
            f'width:{field["w"]}%;line-height:{field.get("line_h", 1.12)};">'
            f'{text}</span>'
        )

    return (
        file_html
        + photo_html
        + field_html("full_name", suspect.get("full_name"))
        + field_html("occupation", suspect.get("occupation"))
        + field_html("age", suspect.get("age"))
        + field_html("distinguishing_features", suspect.get("distinguishing_features"), multiline=True)
        + field_html("alibi", suspect.get("alibi"), multiline=True)
    )


def _render_select(
    suspects: list[dict],
    bg_b64: str,
    aspect: float,
    view_start: int,
    selected_index: int,
    back_btn_html: str,
    back_btn_css: str,
) -> None:
    total = len(suspects)
    left_suspect  = suspects[view_start]         if view_start     < total else None
    right_suspect = suspects[view_start + 1]     if view_start + 1 < total else None

    left_selected  = "ar-selected" if selected_index == view_start     else ""
    right_selected = "ar-selected" if selected_index == view_start + 1 else ""

    left_cfg = {**_LEFT, "index": view_start, "selected_class": left_selected}
    right_cfg = {**_RIGHT, "index": view_start + 1, "selected_class": right_selected}

    left_html  = _card_html(left_suspect,  left_cfg)
    right_html = _card_html(right_suspect, right_cfg)

    hide_left_arrow  = "ar-arrow-disabled" if view_start == 0 else ""
    hide_right_arrow = "ar-arrow-disabled" if view_start + SUSPECTS_PER_PAGE >= total else ""

    confirm_active = "ar-confirm-active" if selected_index >= 0 else "ar-confirm-inactive"
    selected_name  = suspects[selected_index].get("full_name", "") if 0 <= selected_index < total else ""

    left_arrow_url = _asset_data_url(LEFT_ARROW_IMAGE)
    right_arrow_url = _asset_data_url(RIGHT_ARROW_IMAGE)
    confirm_url = _asset_data_url(CONFIRM_IMAGE)

    html = f"""
    <!DOCTYPE html><html><head>
    <style>
    html,body{{margin:0;padding:0;width:100vw;height:100vh;overflow:hidden;background:#1a0a04;}}
    .ar-page{{width:100vw;height:100vh;display:flex;justify-content:center;align-items:center;background:#1a0a04;}}
    .ar-stage{{position:relative;width:min(100vw,calc(100vh*{aspect}));aspect-ratio:{aspect};}}
    .ar-bg{{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;z-index:1;pointer-events:none;user-select:none;}}

    .ar-file-card{{
        position:absolute;z-index:10;cursor:pointer;background:transparent;
        border:0;padding:0;margin:0;
    }}
    .ar-file-image{{
        position:absolute;z-index:6;object-fit:contain;display:block;
        pointer-events:none;user-select:none;
        transition:filter 0.15s ease, transform 0.15s ease;
    }}
    .ar-file-card:hover + .ar-file-image{{filter:brightness(1.08);transform:scale(1.015);}}
    .ar-selected{{filter:drop-shadow(0 0 18px rgba(255,215,0,0.7)) brightness(1.08)!important;}}

    .ar-image-button{{
        position:absolute;z-index:15;cursor:pointer;background:transparent;
        border:0;padding:0;margin:0;
        transition:filter 0.15s ease, transform 0.15s ease;
    }}
    .ar-image-button:hover{{filter:brightness(1.18);transform:scale(1.04);}}
    .ar-image-button img{{width:100%;height:100%;object-fit:contain;display:block;pointer-events:none;user-select:none;}}
    .ar-arrow-disabled{{opacity:0.25;pointer-events:none;}}

    .ar-confirm-button{{
        left:26.0%;top:82.5%;width:57%;height:17.25%;
    }}
    .ar-confirm-active:hover{{filter:brightness(1.18);transform:scale(1.025);}}
    .ar-confirm-inactive{{opacity:0.45;cursor:not-allowed;}}

    #ar-overlay{{
        display:none;position:absolute;inset:0;z-index:100;
        background:rgba(0,0,0,0.75);
        justify-content:center;align-items:center;
    }}
    .ar-dialog{{
        background:linear-gradient(160deg,#2a1508,#1a0d04);
        border:2px solid #8B5E3C;border-radius:14px;
        padding:2em 2.5em;text-align:center;
        box-shadow:0 8px 32px rgba(0,0,0,0.8);
        min-width:260px;
    }}
    .ar-dialog p{{
        font-family:Georgia,serif;color:#f4dfaa;
        font-size:clamp(13px,1.2vw,20px);margin:0 0 1em;
        line-height:1.5;
    }}
    .ar-dialog strong{{color:#ffd700;}}
    .ar-btn{{
        font-family:Georgia,serif;font-size:clamp(12px,1vw,17px);
        padding:0.4em 1.2em;border-radius:8px;cursor:pointer;
        border:2px solid #8B5E3C;margin:0 0.4em;transition:filter 0.15s;
    }}
    .ar-btn:hover{{filter:brightness(1.2);}}
    .ar-btn-yes{{background:#8B2020;color:#f4dfaa;}}
    .ar-btn-no {{background:#3a2010;color:#f4dfaa;}}

    {back_btn_css}
    </style></head>
    <body>
    <div class="ar-page">
        <div class="ar-stage">
            {back_btn_html}
            <img class="ar-bg" src="data:image/png;base64,{bg_b64}" alt="Arrest screen">

            {left_html}
            {right_html}

            <button class="ar-image-button {hide_left_arrow}"
                    style="left:12.8%;top:38.0%;width:9.0%;height:19.0%;"
                    onclick="navigate('ar_left')"
                    aria-label="Previous suspect">
                <img src="{left_arrow_url}" alt="Previous suspect">
            </button>

            <button class="ar-image-button {hide_right_arrow}"
                    style="right:5.8%;top:38.0%;width:9.0%;height:19.0%;"
                    onclick="navigate('ar_right')"
                    aria-label="Next suspect">
                <img src="{right_arrow_url}" alt="Next suspect">
            </button>

            <button class="ar-image-button ar-confirm-button {confirm_active}"
                    onclick="tryConfirm()"
                    aria-label="Confirm arrest">
                <img src="{confirm_url}" alt="Confirm arrest">
            </button>

            <div id="ar-overlay" style="display:none;position:absolute;inset:0;z-index:100;background:rgba(0,0,0,0.75);justify-content:center;align-items:center;">
                <div class="ar-dialog">
                    <p>Are you sure you want to arrest<br><strong>{selected_name}</strong>?</p>
                    <button class="ar-btn ar-btn-yes" onclick="doConfirm()">Confirm arrest</button>
                    <button class="ar-btn ar-btn-no"  onclick="cancelConfirm()">Cancel</button>
                </div>
            </div>
        </div>
    </div>

    {robust_navigation_script()}
    <script>
    function tryConfirm() {{
        if ({str(selected_index)} < 0) return;
        document.getElementById('ar-overlay').style.display = 'flex';
    }}
    function doConfirm() {{
        navigate('ar_confirm');
    }}
    function cancelConfirm() {{
        document.getElementById('ar-overlay').style.display = 'none';
    }}
    </script>
    </body></html>
    """

    components.html(html, height=1, scrolling=False)


def show_arrest_suspect() -> None:
    bg_path = ASSETS_DIR / "Arrest person screen.png"
    if not bg_path.exists():
        st.error(f"Background image not found: {bg_path}")
        st.stop()

    bg_b64 = cached_image_to_base64(bg_path)
    aspect = get_aspect_ratio(bg_path)

    suspects = _get_arrest_candidates()
    if not suspects:
        st.markdown(streamlit_chrome_css(background="#1a0a04"), unsafe_allow_html=True)
        st.error("No suspects have been added yet. Fill in SUSPECTS in Suspects/Code/suspects.py.")
        return

    total = len(suspects)

    if "ar_view"     not in st.session_state: st.session_state.ar_view     = 0
    if "ar_selected" not in st.session_state: st.session_state.ar_selected = -1

    max_view_start = max(0, ((total - 1) // SUSPECTS_PER_PAGE) * SUSPECTS_PER_PAGE)
    view_start = max(0, min(st.session_state.ar_view, max_view_start))
    view_start = (view_start // SUSPECTS_PER_PAGE) * SUSPECTS_PER_PAGE
    st.session_state.ar_view = view_start
    selected = st.session_state.ar_selected
    if selected >= total:
        selected = -1
        st.session_state.ar_selected = -1

    back_btn_html = get_back_button_html(btn_key="ar_back")
    back_btn_css  = get_back_button_css(left="1.0%", top="1.5%", width="10%")

    st.markdown(streamlit_chrome_css(background="#1a0a04"), unsafe_allow_html=True)
    _render_select(suspects, bg_b64, aspect, view_start, selected, back_btn_html, back_btn_css)

    render_back_button_streamlit(btn_key="ar_back", target_page="main_menu")

    if st.button("ar_left", key="ar_hidden_left"):
        st.session_state.ar_view = max(0, view_start - SUSPECTS_PER_PAGE)
        st.rerun()

    if st.button("ar_right", key="ar_hidden_right"):
        st.session_state.ar_view = min(max_view_start, view_start + SUSPECTS_PER_PAGE)
        st.rerun()

    if st.button("ar_confirm", key="ar_hidden_confirm"):
        arrested = suspects[selected] if 0 <= selected < total else {}
        arrested_name = arrested.get("full_name", "")

        is_correct = _is_correct_arrest(arrested)
        guilty_name, guilty_photo = _get_guilty_result(suspects, arrested)
        arrested_id = arrested.get("id")

        if arrested_id is not None:
            save_arrest_guess(
                st.session_state.get("game_number", 0),
                int(arrested_id),
                is_correct,
            )

        st.session_state["result_is_correct"] = is_correct
        st.session_state["result_arrested_name"] = arrested_name
        st.session_state["result_arrested_photo"] = arrested.get("photo", None)
        st.session_state["result_guilty_name"] = guilty_name
        st.session_state["result_guilty_photo"] = guilty_photo
        st.session_state["page"] = "you_win" if is_correct else "you_lose"
        st.rerun()

    sel_cols = st.columns(max(total, 1))
    for i, col in enumerate(sel_cols):
        with col:
            if st.button(f"ar_select_{i}", key=f"ar_hidden_sel_{i}"):
                st.session_state.ar_selected = i
                st.rerun()


def show_arrest_person() -> None:
    show_arrest_suspect()

