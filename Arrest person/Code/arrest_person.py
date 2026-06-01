import base64
import sys
from pathlib import Path

from PIL import Image
import streamlit as st
import streamlit.components.v1 as components


project_root = Path(__file__).resolve().parents[2]
back_button_code_dir = project_root / "Back to main menu" / "Code"
char_randomizer_code_dir = project_root / "Char Randomizer" / "Code"
suspect_selecter_code_dir = project_root / "Suspect selecter" / "Code"

if str(back_button_code_dir) not in sys.path:
    sys.path.append(str(back_button_code_dir))
if str(char_randomizer_code_dir) not in sys.path:
    sys.path.append(str(char_randomizer_code_dir))
if str(suspect_selecter_code_dir) not in sys.path:
    sys.path.append(str(suspect_selecter_code_dir))

from back_to_main_menu import get_back_button_css, get_back_button_html, render_back_button_streamlit

# Hent mistænkte fra suspects.py (samme liste bruges begge steder)
try:
    suspects_dir = project_root / "Suspects" / "Code"
    if str(suspects_dir) not in sys.path:
        sys.path.append(str(suspects_dir))
    from suspects import SUSPECTS, _person_to_suspect
except Exception:
    SUSPECTS = []
    _person_to_suspect = None

try:
    from Random_char_selector import get_selected_characters
except ImportError:
    def get_selected_characters() -> list[dict]:
        return []

try:
    from Is_Suspect import get_guilty_suspect, is_guilty_suspect
except ImportError:
    def get_guilty_suspect() -> dict | None:
        return None

    def is_guilty_suspect(character: dict) -> bool:
        return bool(character.get("is_suspect"))

ASSETS_DIR = Path(__file__).resolve().parents[1] / "Assets"
CHARS_DIR = project_root / "Characters"

# Sæt dette til den skyldiges full_name for at aktivere rigtigt/forkert feedback.
# Lad feltet være tomt ("") for at springe over.
CORRECT_SUSPECT: str = ""

# ── Kort-layout (% af billedets bredde/højde) ────────────────────────────────
# Juster x_val og y_* hvis teksten ikke lander på de rigtige linjer.
_LEFT = {
    "photo_left": 19.0, "photo_top": 15.0, "photo_w": 24.0, "photo_h": 34.0,
    "click_x": 15.5, "click_y": 13.0, "click_w": 33.0, "click_h": 76.0,
    "x_val": 29.5,
    "y_name": 55.5, "y_occ": 62.0, "y_age": 68.0, "y_feat": 74.0, "y_alibi": 81.0,
}
_RIGHT = {
    "photo_left": 55.0, "photo_top": 15.0, "photo_w": 24.0, "photo_h": 34.0,
    "click_x": 51.5, "click_y": 13.0, "click_w": 33.0, "click_h": 76.0,
    "x_val": 65.5,
    "y_name": 55.5, "y_occ": 62.0, "y_age": 68.0, "y_feat": 74.0, "y_alibi": 81.0,
}
# ─────────────────────────────────────────────────────────────────────────────


def _b64(path: Path) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def _aspect(path: Path) -> float:
    with Image.open(path) as img:
        w, h = img.size
    return w / h


def _get_arrest_candidates() -> list[dict]:
    selected_characters = get_selected_characters()
    suspicious_ids = set(st.session_state.get("wo_suspicious", set()))

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

    if CORRECT_SUSPECT:
        return arrested.get("full_name") == CORRECT_SUSPECT

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

    if CORRECT_SUSPECT:
        matching_candidate = next(
            (candidate for candidate in candidates if candidate.get("full_name") == CORRECT_SUSPECT),
            None,
        )
        if matching_candidate:
            return matching_candidate.get("full_name", ""), matching_candidate.get("photo")
        return CORRECT_SUSPECT, None

    return arrested.get("full_name", ""), arrested.get("photo")


def _card_html(suspect: dict | None, cfg: dict) -> str:
    if suspect is None:
        return ""

    photo_html = ""
    if suspect.get("photo"):
        p = Path(suspect["photo"])
        if p.exists():
            photo_html = (
                f'<img style="position:absolute;left:{cfg["photo_left"]}%;top:{cfg["photo_top"]}%;'
                f'width:{cfg["photo_w"]}%;height:{cfg["photo_h"]}%;'
                f'object-fit:contain;z-index:8;pointer-events:none;"'
                f' src="data:image/png;base64,{_b64(p)}" alt="photo">'
            )

    s = (
        "position:absolute;z-index:8;font-family:Georgia,serif;"
        "font-size:clamp(7px,0.8vw,13px);color:#1a0e07;font-weight:600;"
        "white-space:nowrap;overflow:hidden;text-overflow:ellipsis;pointer-events:none;"
    )
    x = cfg["x_val"]
    return (
        photo_html
        + f'<span style="{s}left:{x}%;top:{cfg["y_name"]}%;max-width:17%;">{suspect.get("full_name","")}</span>'
        + f'<span style="{s}left:{x}%;top:{cfg["y_occ"]}%;max-width:17%;">{suspect.get("occupation","")}</span>'
        + f'<span style="{s}left:{x}%;top:{cfg["y_age"]}%;max-width:8%;">{suspect.get("age","")}</span>'
        + f'<span style="{s}left:{x}%;top:{cfg["y_feat"]}%;max-width:17%;">{suspect.get("distinguishing_features","")}</span>'
        + f'<span style="{s}left:{x}%;top:{cfg["y_alibi"]}%;max-width:17%;">{suspect.get("alibi","")}</span>'
    )


def _streamlit_css() -> str:
    return """
        <style>
        html, body, .stApp {
            margin:0!important;padding:0!important;overflow:hidden!important;background:#1a0a04!important;
        }
        [data-testid="stHeader"]{background:rgba(0,0,0,0)!important;height:0rem!important;}
        [data-testid="stToolbar"],[data-testid="stDecoration"]{display:none!important;}
        .block-container{padding:0!important;margin:0!important;max-width:100%!important;height:100vh!important;overflow:hidden!important;}
        section.main,div[data-testid="stAppViewContainer"],div[data-testid="stVerticalBlock"]{overflow:hidden!important;}
        iframe{width:100vw!important;height:100vh!important;display:block!important;border:none!important;}
        .element-container:has(iframe){width:100vw!important;height:100vh!important;overflow:hidden!important;}
        </style>
    """


def _navigate_js() -> str:
    return """
    <script>
    function navigate(page) {
        var btns = window.parent.document.querySelectorAll('button');
        for (var i = 0; i < btns.length; i++) {
            if (btns[i].innerText.trim() === page) { btns[i].click(); return; }
        }
    }
    </script>
    """


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

    left_html  = _card_html(left_suspect,  _LEFT)
    right_html = _card_html(right_suspect, _RIGHT)

    left_selected  = "ar-selected" if selected_index == view_start     else ""
    right_selected = "ar-selected" if selected_index == view_start + 1 else ""

    left_name  = left_suspect.get("full_name", "")  if left_suspect  else ""
    right_name = right_suspect.get("full_name", "") if right_suspect else ""

    # Dimmed overlay on arrows when at edges
    hide_left_arrow  = "ar-arrow-disabled" if view_start == 0            else ""
    hide_right_arrow = "ar-arrow-disabled" if view_start >= total - 1    else ""

    confirm_active = "ar-confirm-active" if selected_index >= 0 else "ar-confirm-inactive"
    selected_name  = suspects[selected_index].get("full_name", "") if 0 <= selected_index < total else ""
    right_card_zone = ""
    if right_suspect:
        right_index = view_start + 1
        right_card_zone = (
            f'<div class="ar-card-zone {right_selected}" '
            f'style="left:{_RIGHT["click_x"]}%;top:{_RIGHT["click_y"]}%;'
            f'width:{_RIGHT["click_w"]}%;height:{_RIGHT["click_h"]}%;" '
            f"""onclick="navigate('ar_select_{right_index}')" """
            f'role="button" aria-label="Vælg {right_name}"></div>'
        )

    html = f"""
    <!DOCTYPE html><html><head>
    <style>
    html,body{{margin:0;padding:0;width:100vw;height:100vh;overflow:hidden;background:#1a0a04;}}
    .ar-page{{width:100vw;height:100vh;display:flex;justify-content:center;align-items:center;background:#1a0a04;}}
    .ar-stage{{position:relative;width:min(100vw,calc(100vh*{aspect}));aspect-ratio:{aspect};}}
    .ar-bg{{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;z-index:1;pointer-events:none;user-select:none;}}

    .ar-card-zone{{
        position:absolute;z-index:10;cursor:pointer;border-radius:6px;
        transition:box-shadow 0.15s ease;
    }}
    .ar-card-zone:hover{{box-shadow:inset 0 0 0 2px rgba(255,210,80,0.5);}}
    .ar-selected{{box-shadow:inset 0 0 0 3px gold,0 0 18px 4px rgba(255,215,0,0.45)!important;}}

    .ar-arrow-zone{{
        position:absolute;z-index:15;cursor:pointer;border-radius:50%;
        transition:filter 0.15s ease;
    }}
    .ar-arrow-zone:hover{{filter:brightness(1.25);}}
    .ar-arrow-disabled{{opacity:0.25;pointer-events:none;}}

    .ar-confirm-zone{{
        position:absolute;z-index:15;cursor:pointer;border-radius:8px;
        transition:filter 0.15s ease;
    }}
    .ar-confirm-active:hover{{filter:brightness(1.18);}}
    .ar-confirm-inactive{{opacity:0.45;cursor:not-allowed;}}

    /* JS confirmation overlay */
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
        {back_btn_html}
        <div class="ar-stage">
            <img class="ar-bg" src="data:image/png;base64,{bg_b64}" alt="Arrest screen">

            {left_html}
            {right_html}

            <!-- Card click zones -->
            <div class="ar-card-zone {left_selected}"
                 style="left:{_LEFT['click_x']}%;top:{_LEFT['click_y']}%;width:{_LEFT['click_w']}%;height:{_LEFT['click_h']}%;"
                 onclick="navigate('ar_select_{view_start}')"
                 role="button" aria-label="Vælg {left_name}"></div>

            {right_card_zone}

            <!-- Left arrow click zone -->
            <div class="ar-arrow-zone {hide_left_arrow}"
                 style="left:8%;top:38%;width:8%;height:22%;"
                 onclick="navigate('ar_left')"
                 aria-label="Forrige mistænkt"></div>

            <!-- Right arrow click zone -->
            <div class="ar-arrow-zone {hide_right_arrow}"
                 style="right:8%;top:38%;width:8%;height:22%;"
                 onclick="navigate('ar_right')"
                 aria-label="Næste mistænkt"></div>

            <!-- CONFIRM ARREST click zone -->
            <div class="ar-confirm-zone {confirm_active}"
                 style="left:29%;top:88%;width:42%;height:10%;"
                 onclick="tryConfirm()"
                 aria-label="Bekræft anholdelse"></div>

            <!-- Confirmation dialog overlay -->
            <div id="ar-overlay" style="display:none;position:absolute;inset:0;z-index:100;background:rgba(0,0,0,0.75);justify-content:center;align-items:center;">
                <div class="ar-dialog">
                    <p>Er du sikker på at du vil anholde<br><strong>{selected_name}</strong>?</p>
                    <button class="ar-btn ar-btn-yes" onclick="doConfirm()">Ja, anholdelse</button>
                    <button class="ar-btn ar-btn-no"  onclick="cancelConfirm()">Annuller</button>
                </div>
            </div>
        </div>
    </div>

    <script>
    function navigate(page) {{
        var btns = window.parent.document.querySelectorAll('button');
        for (var i = 0; i < btns.length; i++) {{
            if (btns[i].innerText.trim() === page) {{ btns[i].click(); return; }}
        }}
    }}
    function tryConfirm() {{
        if ({str(selected_index)}) {{
            // Show overlay only if something is selected (selected_index >= 0)
        }}
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
        st.error(f"Baggrundsbillede ikke fundet: {bg_path}")
        st.stop()

    bg_b64 = _b64(bg_path)
    aspect  = _aspect(bg_path)

    suspects = _get_arrest_candidates()
    if not suspects:
        st.markdown(_streamlit_css(), unsafe_allow_html=True)
        st.error("Ingen mistænkte er tilføjet endnu. Udfyld SUSPECTS i Suspects/Code/suspects.py.")
        return

    total = len(suspects)

    if "ar_view"     not in st.session_state: st.session_state.ar_view     = 0
    if "ar_selected" not in st.session_state: st.session_state.ar_selected = -1

    view_start = max(0, min(st.session_state.ar_view, total - 1))
    st.session_state.ar_view = view_start
    selected = st.session_state.ar_selected
    if selected >= total:
        selected = -1
        st.session_state.ar_selected = -1

    back_btn_html = get_back_button_html(btn_key="ar_back")
    back_btn_css  = get_back_button_css(left="1.0%", top="1.5%", width="10%")

    st.markdown(_streamlit_css(), unsafe_allow_html=True)
    _render_select(suspects, bg_b64, aspect, view_start, selected, back_btn_html, back_btn_css)

    # ── Skjulte Streamlit-navigationknapper ──────────────────────────────────

    render_back_button_streamlit(btn_key="ar_back", target_page="main_menu")

    if st.button("ar_left", key="ar_hidden_left"):
        st.session_state.ar_view = max(0, view_start - 1)
        st.rerun()

    if st.button("ar_right", key="ar_hidden_right"):
        st.session_state.ar_view = min(total - 1, view_start + 1)
        st.rerun()

    if st.button("ar_confirm", key="ar_hidden_confirm"):
        arrested = suspects[selected] if 0 <= selected < total else {}
        arrested_name = arrested.get("full_name", "")

        is_correct = _is_correct_arrest(arrested)
        guilty_name, guilty_photo = _get_guilty_result(suspects, arrested)

        st.session_state["result_is_correct"] = is_correct
        st.session_state["result_arrested_name"] = arrested_name
        st.session_state["result_arrested_photo"] = arrested.get("photo", None)
        st.session_state["result_guilty_name"] = guilty_name
        st.session_state["result_guilty_photo"] = guilty_photo
        st.session_state["page"] = "you_win" if is_correct else "you_lose"
        st.rerun()

    # Én knap pr. mistænkt til at vælge dem
    sel_cols = st.columns(max(total, 1))
    for i, col in enumerate(sel_cols):
        with col:
            if st.button(f"ar_select_{i}", key=f"ar_hidden_sel_{i}"):
                st.session_state.ar_selected = i
                st.rerun()


def show_arrest_person() -> None:
    show_arrest_suspect()

