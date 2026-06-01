import base64
import html
import sys
from pathlib import Path

from PIL import Image
import streamlit as st
import streamlit.components.v1 as components


project_root = Path(__file__).resolve().parents[2]
back_button_code_dir = project_root / "Back to main menu" / "Code"
screen_arrows_code_dir = project_root / "Screen arrows" / "Code"
witness_button_code_dir = project_root / "Witness shortcut" / "Code"

if str(back_button_code_dir) not in sys.path:
    sys.path.append(str(back_button_code_dir))
if str(screen_arrows_code_dir) not in sys.path:
    sys.path.append(str(screen_arrows_code_dir))
if str(witness_button_code_dir) in sys.path:
    sys.path.remove(str(witness_button_code_dir))
sys.path.insert(0, str(witness_button_code_dir))

# Streamlit keeps imported modules alive between reruns. Force this helper to
# reload from the shared Witness shortcut folder after it was moved there.
sys.modules.pop("witness_button", None)

from back_to_main_menu import get_back_button_css, get_back_button_html, render_back_button_streamlit
from screen_arrows import screen_arrow_css, make_screen_arrow_button
from witness_button import (
    get_witness_file_button_css,
    get_witness_file_button_html,
    get_witness_green_button_css,
    get_witness_overview_button_css,
    get_witness_overview_button_html,
    get_witness_red_button_css,
    get_witness_red_button_html,
    get_witness_static_button_html,
    render_witness_file_button_streamlit,
    render_witness_overview_button_streamlit,
    render_witness_red_button_streamlit,
)
from witness_overview import PERSONS, get_witness_statement


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
CHARS_DIR = project_root / "Characters"


# Same birth details as suspects.py, so Witness File and Suspect File line up.
PERSON_BIRTH_DETAILS = {
    1: {"age": "34", "date_of_birth": "14/02/1992"},
    2: {"age": "29", "date_of_birth": "03/08/1996"},
    3: {"age": "31", "date_of_birth": "19/11/1994"},
    4: {"age": "42", "date_of_birth": "27/04/1984"},
    5: {"age": "38", "date_of_birth": "09/06/1987"},
    6: {"age": "35", "date_of_birth": "22/01/1991"},
    7: {"age": "24", "date_of_birth": "16/09/2001"},
    8: {"age": "27", "date_of_birth": "30/03/1999"},
    9: {"age": "33", "date_of_birth": "05/12/1992"},
    10: {"age": "40", "date_of_birth": "11/07/1985"},
    11: {"age": "32", "date_of_birth": "25/10/1993"},
    12: {"age": "36", "date_of_birth": "08/05/1990"},
    13: {"age": "58", "date_of_birth": "17/01/1968"},
    14: {"age": "45", "date_of_birth": "29/09/1980"},
    15: {"age": "30", "date_of_birth": "06/06/1995"},
    16: {"age": "28", "date_of_birth": "13/04/1998"},
    17: {"age": "61", "date_of_birth": "02/12/1964"},
    18: {"age": "26", "date_of_birth": "21/07/1999"},
    19: {"age": "39", "date_of_birth": "18/02/1987"},
    20: {"age": "33", "date_of_birth": "12/10/1992"},
    21: {"age": "41", "date_of_birth": "04/03/1985"},
    22: {"age": "67", "date_of_birth": "26/08/1958"},
    23: {"age": "23", "date_of_birth": "15/05/2003"},
    24: {"age": "37", "date_of_birth": "01/11/1988"},
    25: {"age": "72", "date_of_birth": "20/04/1954"},
    26: {"age": "25", "date_of_birth": "07/01/2001"},
    27: {"age": "29", "date_of_birth": "24/06/1996"},
    28: {"age": "44", "date_of_birth": "10/09/1981"},
    29: {"age": "31", "date_of_birth": "28/12/1994"},
    30: {"age": "46", "date_of_birth": "05/02/1980"},
}


def _character_photo_path(person_id: int) -> str | None:
    # Use the same image as suspects.py. No Char_zoom_ version here.
    standard_path = CHARS_DIR / f"Char_{person_id}.png"

    if standard_path.exists():
        return str(standard_path)
    return None


def _short_text(text: str, limit: int = 170) -> str:
    text = " ".join(str(text).split())
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def _line_count(
    text: str,
    *,
    chars_per_line: int = 58,
    max_lines: int = 3,
) -> int:
    text = " ".join(str(text).split())
    if not text:
        return 1
    return max(1, min(max_lines, (len(text) + chars_per_line - 1) // chars_per_line))


def _field_html(
    label: str,
    value: str,
    *,
    tall: bool = False,
    single: bool = False,
    chars_per_line: int = 58,
    max_lines: int = 3,
    extra_class: str = "",
) -> str:
    safe_label = html.escape(label)
    safe_value = html.escape(str(value))
    lines = _line_count(
        str(value),
        chars_per_line=chars_per_line,
        max_lines=max_lines,
    ) if tall else 1
    entry_class = "sf-entry sf-entry-tall" if tall and lines > 1 else "sf-entry"
    if extra_class:
        entry_class = f"{entry_class} {extra_class}"
    value_class = "sf-single" if single else "sf-wrap"
    line_style = f' style="--lines:{lines};"' if tall and lines > 1 else ""

    return f"""
                    <div class="{entry_class}"{line_style}>
                        <div class="sf-label">{safe_label}</div>
                        <div class="sf-line"><div class="sf-field {value_class}">{safe_value}</div></div>
                    </div>
    """


def _split_field_html(
    left_label: str,
    left_value: str,
    right_label: str,
    right_value: str,
    *,
    extra_class: str = "",
) -> str:
    entry_class = "sf-entry-split"
    if extra_class:
        entry_class = f"{entry_class} {extra_class}"

    return f"""
                    <div class="{entry_class}">
                        <div class="sf-subentry">
                            <div class="sf-label">{html.escape(left_label)}</div>
                            <div class="sf-line"><div class="sf-field sf-single">{html.escape(str(left_value))}</div></div>
                        </div>
                        <div class="sf-subentry">
                            <div class="sf-label">{html.escape(right_label)}</div>
                            <div class="sf-line"><div class="sf-field sf-single">{html.escape(str(right_value))}</div></div>
                        </div>
                    </div>
    """


def _witness_fields_html(witness: dict) -> str:
    return "".join(
        [
            _field_html(
                "Full Name:",
                witness["full_name"],
                single=True,
                extra_class="wf-full-name-entry",
            ),
            _field_html(
                "Occupation:",
                witness["occupation"],
                single=True,
                extra_class="wf-occupation-entry",
            ),
            _split_field_html(
                "Age:",
                witness["age"],
                "Date of Birth:",
                witness["date_of_birth"],
                extra_class="wf-age-date-entry",
            ),
            _field_html(
                "Personal Characteristics:",
                witness["personal_characteristics"],
                tall=True,
                chars_per_line=88,
                extra_class="wf-personal-characteristics-entry",
            ),
            _field_html(
                "Clothing:",
                witness["clothing"],
                tall=True,
                chars_per_line=88,
                extra_class="wf-clothing-entry",
            ),
            _field_html(
                "Distinguishing Features:",
                witness["distinguishing_features"],
                tall=True,
                chars_per_line=88,
                extra_class="wf-distinguishing-features-entry",
            ),
            _field_html(
                "Relationship to Case:",
                witness["relationship_to_case"],
                single=True,
                extra_class="wf-relationship-entry",
            ),
            _field_html(
                "Alibi:",
                witness["alibi"],
                single=True,
                extra_class="wf-alibi-entry",
            ),
            _field_html(
                "Witness Statement:",
                witness["witness_statement"],
                tall=True,
                chars_per_line=82,
                max_lines=4,
                extra_class="wf-statement-entry",
            ),
        ]
    )


def _person_to_witness(person: dict) -> dict:
    person_id = person.get("id", 0)
    birth_details = PERSON_BIRTH_DETAILS.get(
        person_id,
        {"age": "", "date_of_birth": ""},
    )
    role = person.get("role", "")
    arrived = person.get("arrived", "")
    left = person.get("left", "")
    appearance = (
        f"{person.get('gender', '')}; "
        f"{person.get('hair', '')} hair; "
        f"{person.get('eyes', '')} eyes; "
        f"{person.get('skin', '')} skin"
    )

    return {
        "full_name": person.get("name", ""),
        "occupation": role,
        "age": birth_details["age"],
        "date_of_birth": birth_details["date_of_birth"],
        "personal_characteristics": appearance,
        "clothing": person.get("clothing", ""),
        "distinguishing_features": (
            f"{person.get('hair', '')} hair, "
            f"{person.get('eyes', '')} eyes, "
            f"{person.get('skin', '')} skin"
        ),
        "relationship_to_case": f"{role}; present near case timeline",
        "alibi": f"Registered presence: {arrived} - {left}",
        "witness_statement": _short_text(get_witness_statement(person), 170),
        "photo": _character_photo_path(person_id),
    }


def get_witnesses() -> list[dict]:
    # Unlike Suspect File, this page always shows all characters.
    return [_person_to_witness(person) for person in PERSONS]


def image_to_base64(image_path: Path) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


def find_background_image(assets_dir: Path) -> Path:
    for file_path in sorted(assets_dir.iterdir()):
        if file_path.is_file() and file_path.suffix.lower() in IMAGE_EXTENSIONS:
            return file_path
    raise FileNotFoundError(f"No background image found in: {assets_dir}")


def show_witnesses() -> None:
    back_btn_html = get_back_button_html(btn_key="wf_back")
    back_btn_css = get_back_button_css(left="1.2%", top="2.0%", width="13%")
    witness_tab_html = get_witness_overview_button_html(btn_key="wf_tab_overview")
    witness_tab_css = get_witness_overview_button_css(
        css_class="witness-overview-tab",
        left="82.7%",
        top="27.7%",
        selected=False,
    )
    witness_file_tab_html = get_witness_file_button_html(btn_key="wf_tab_file")
    witness_file_tab_css = get_witness_file_button_css(
        css_class="witness-file-tab",
        left="82.9%",
        top="46.8%",
        selected=True,
    )
    witness_red_tab_html = get_witness_red_button_html(btn_key="wf_tab_suspects")
    witness_red_tab_css = get_witness_red_button_css(
        css_class="witness-red-tab",
        left="82.9%",
        top="11.6%",
        selected=False,
    )
    witness_green_tab_html = get_witness_static_button_html(
        css_class="witness-green-tab",
        label="Witness shortcut green",
    )
    witness_green_tab_css = get_witness_green_button_css(
        css_class="witness-green-tab",
        left="82.9%",
        top="65.8%",
    )

    feature_dir = Path(__file__).resolve().parents[1]
    assets_dir = feature_dir / "Assets"

    try:
        background_path = find_background_image(assets_dir)
    except FileNotFoundError as error:
        st.error(str(error))
        st.stop()

    background_b64 = image_to_base64(background_path)

    with Image.open(background_path) as img:
        img_width, img_height = img.size
    aspect_ratio = img_width / img_height

    witnesses = get_witnesses()
    total_witnesses = len(witnesses)

    if "witness_index" not in st.session_state:
        st.session_state.witness_index = 0

    current_index = st.session_state.witness_index % max(total_witnesses, 1)
    witness = witnesses[current_index]
    counter_text = f"{current_index + 1} / {total_witnesses}"

    left_arrow_html = make_screen_arrow_button(
        direction="left",
        onclick="navigate('prev')",
        css_class="witness-arrow-left",
        aria_label="Previous witness",
    )
    right_arrow_html = make_screen_arrow_button(
        direction="right",
        onclick="navigate('next')",
        css_class="witness-arrow-right",
        aria_label="Next witness",
    )

    photo_html = ""
    if witness.get("photo"):
        photo_path = Path(witness["photo"])
        if photo_path.exists():
            photo_b64 = image_to_base64(photo_path)
            photo_html = f"""
            <img
                class="witness-photo"
                src="data:image/png;base64,{photo_b64}"
                alt="Witness photo"
            >
            """

    witness_fields_html = _witness_fields_html(witness)

    st.markdown(
        """
        <style>
        html, body, .stApp {
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
            background: #3a1f0f !important;
        }
        [data-testid="stHeader"] {
            background: rgba(0, 0, 0, 0) !important;
            height: 0rem !important;
        }
        [data-testid="stToolbar"],
        [data-testid="stDecoration"] {
            display: none !important;
        }
        #wf-nav-anchor, #wf-nav-anchor + div {
            display: none !important;
        }
        .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
            height: 100vh !important;
            overflow: hidden !important;
        }
        section.main,
        div[data-testid="stAppViewContainer"],
        div[data-testid="stVerticalBlock"] {
            overflow: hidden !important;
        }
        iframe {
            width: 100vw !important;
            height: 100vh !important;
            display: block !important;
            border: none !important;
        }
        .element-container:has(iframe) {
            width: 100vw !important;
            height: 100vh !important;
            overflow: hidden !important;
        }
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
            margin: 0;
            padding: 0;
            width: 100vw;
            height: 100vh;
            overflow: hidden;
            background: #3a1f0f;
        }}

        .witness-page {{
            width: 100vw;
            height: 100vh;
            overflow: hidden;
            background: #3a1f0f;
            display: flex;
            justify-content: center;
            align-items: center;
        }}

        .witness-stage {{
            position: relative;
            width: min(100vw, calc(100vh * {aspect_ratio}));
            aspect-ratio: {aspect_ratio};
            overflow: hidden;
        }}

        .witness-bg {{
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            object-fit: contain;
            z-index: 1;
            user-select: none;
            pointer-events: none;
        }}

        /* Same placement as suspects.py */
        .witness-photo {{
            position: absolute;
            left: 19.9%;
            top: 15%;
            width: 25%;
            height: 68%;
            object-fit: contain;
            z-index: 3;
            pointer-events: none;
        }}

        /* Same field layout as suspects.py */
        .witness-fields {{
            position: absolute;
            left: 52.0%;
            top: 15.0%;
            width: 27.5%;
            height: 77.0%;
            z-index: 3;
            font-family: 'Georgia', serif;
            color: #1a0e07;
            box-sizing: border-box;
            padding: 0.6% 0.8%;
        }}

        .sf-entry {{
            position: relative;
            display: block;
            min-height: 6.0%;
            margin-bottom: 0.8%;
        }}

        .sf-entry-tall {{
            min-height: calc(1.35em + (var(--lines, 1) * 1.38em) + 0.35em);
        }}

        .sf-entry-split {{
            display: grid;
            grid-template-columns: 1fr 1.3fr;
            column-gap: 0.75em;
            min-height: 6.0%;
            margin-bottom: 0.8%;
        }}

        .sf-subentry {{
            display: block;
        }}

        .sf-label {{
            display: block;
            font-family: Arial, sans-serif;
            font-size: clamp(6px, 0.58vw, 10px);
            font-weight: 800;
            color: #17202a;
            padding-right: 0;
            white-space: nowrap;
            margin-bottom: 0.05em;
        }}

        .sf-line {{
            position: relative;
            min-height: 1em;
            border-bottom: 1.2px solid rgba(65, 85, 80, 0.58);
            box-sizing: border-box;
            width: 100%;
            margin-top: 0.1em;
        }}

        .sf-entry-tall .sf-line {{
            height: 100%;
            min-height: calc(var(--lines, 1) * 1.38em);
            background-image: linear-gradient(
                to bottom,
                transparent calc(1.38em - 1px),
                rgba(65, 85, 80, 0.46) calc(1.38em - 1px),
                rgba(65, 85, 80, 0.46) 1.38em,
                transparent 1.38em
            );
            background-size: 100% 1.38em;
            border-bottom: 1.2px solid rgba(65, 85, 80, 0.58);
        }}

        .sf-field {{
            position: absolute;
            left: 0.25em;
            right: 0;
            top: 0.64em;
            font-weight: 600;
            overflow: hidden;
            color: #171008;
            font-size: clamp(6px, 0.54vw, 9.5px);
            line-height: 1.25em;
            word-break: break-word;
        }}

        .sf-entry-tall .sf-field {{
            top: 0.50em;
            line-height: 1.38em;
            max-height: calc(var(--lines, 1) * 1.38em);
        }}

        .sf-single {{
            white-space: nowrap;
            text-overflow: ellipsis;
        }}

        .sf-wrap {{
            white-space: normal;
        }}

        /* Manual spacing hooks for every Witness File field. */
        .wf-full-name-entry {{
            margin-bottom: 0.8%;
        }}

        .wf-full-name-entry .sf-line {{
            margin-top: 0.1em;
        }}

        .wf-full-name-entry .sf-field {{
            top: 0.64em;
        }}

        .wf-occupation-entry {{
            margin-bottom: 0.8%;
        }}

        .wf-occupation-entry .sf-line {{
            margin-top: 0.1em;
        }}

        .wf-occupation-entry .sf-field {{
            top: 0.64em;
        }}

        .wf-age-date-entry {{
            margin-bottom: 0.8%;
        }}

        .wf-age-date-entry .sf-line {{
            margin-top: 0.1em;
        }}

        .wf-age-date-entry .sf-field {{
            top: 0.64em;
        }}

        .wf-personal-characteristics-entry {{
            margin-bottom: 0.8%;
        }}

        .wf-personal-characteristics-entry .sf-line {{
            margin-top: 0.1em;
        }}

        .wf-personal-characteristics-entry .sf-field {{
            top: 0.50em;
        }}

        .wf-clothing-entry {{
            margin-bottom: 1em;
        }}

        .wf-clothing-entry .sf-line {{
            margin-top: 0.1em;
        }}

        .wf-clothing-entry .sf-field {{
            top: 0.50em;
        }}

        .wf-distinguishing-features-entry {{
            margin-bottom: 0.8%;
        }}

        .wf-distinguishing-features-entry .sf-line {{
            margin-top: 0.1em;
        }}

        .wf-distinguishing-features-entry .sf-field {{
            top: 0.50em;
        }}

        .wf-relationship-entry {{
            margin-bottom: 0.8%;
        }}

        .wf-relationship-entry .sf-line {{
            margin-top: 0.1em;
        }}

        .wf-relationship-entry .sf-field {{
            top: 0.64em;
        }}

        .wf-alibi-entry {{
            margin-bottom: 0.8%;
        }}

        .wf-alibi-entry .sf-line {{
            margin-top: 0.1em;
        }}

        .wf-alibi-entry .sf-field {{
            top: 0.64em;
        }}

        .wf-statement-entry {{
            margin-bottom: 0.8%;
        }}

        .wf-statement-entry .sf-line {{
            margin-top: -0.25em;
            height: calc(var(--lines, 1) * 1.25em);
            min-height: calc(var(--lines, 1) * 1.25em);
        }}

        .wf-statement-entry .sf-field {{
            top: 1.35em;
            line-height: 1.55em;
        }}

        {back_btn_css}

        {witness_tab_css}

        {witness_file_tab_css}

        {witness_red_tab_css}

        {witness_green_tab_css}

        {screen_arrow_css()}

        .witness-arrow-left {{
            left: 1.0%;
            top: 35%;
            width: 8%;
            height: 28%;
        }}

        .witness-arrow-right {{
            right: 1.0%;
            top: 35%;
            width: 8%;
            height: 28%;
        }}

        .witness-counter {{
            position: absolute;
            left: 50%;
            bottom: 2.5%;
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
        </style>
    </head>
    <body>
        <div class="witness-page">
            {back_btn_html}
            <div class="witness-stage">

                <img
                    class="witness-bg"
                    src="data:image/png;base64,{background_b64}"
                    alt="Witness file"
                >

                {photo_html}

                {witness_tab_html}

                {witness_file_tab_html}

                {witness_red_tab_html}

                {witness_green_tab_html}

                <div class="witness-fields">
                    {witness_fields_html}
                </div>

                {left_arrow_html}
                {right_arrow_html}

                <div class="witness-counter">{counter_text}</div>

            </div>
        </div>

        <script>
        function navigate(direction) {{
            const buttons = window.parent.document.querySelectorAll('button');
            for (const btn of buttons) {{
                if (btn.innerText.trim() === direction) {{
                    btn.click();
                    return;
                }}
            }}
        }}
        </script>
    </body>
    </html>
    """

    components.html(html, height=1, scrolling=False)

    render_back_button_streamlit(btn_key="wf_back", target_page="main_menu")
    render_witness_overview_button_streamlit(btn_key="wf_tab_overview", target_page="witnesses")
    render_witness_file_button_streamlit(btn_key="wf_tab_file", target_page="witness_file")
    render_witness_red_button_streamlit(btn_key="wf_tab_suspects", target_page="suspects")

    col_prev, col_next = st.columns(2)
    with col_prev:
        if st.button("prev", key="wf_prev"):
            if total_witnesses > 0:
                st.session_state.witness_index = (
                    st.session_state.witness_index - 1
                ) % total_witnesses
                st.rerun()
    with col_next:
        if st.button("next", key="wf_next"):
            if total_witnesses > 0:
                st.session_state.witness_index = (
                    st.session_state.witness_index + 1
                ) % total_witnesses
                st.rerun()


def show_witness_file() -> None:
    show_witnesses()
