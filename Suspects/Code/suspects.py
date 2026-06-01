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
witness_file_code_dir = project_root / "Witness file" / "Code"
database_code_dir = project_root / "Database" / "Code"

if str(back_button_code_dir) not in sys.path:
    sys.path.append(str(back_button_code_dir))
if str(screen_arrows_code_dir) not in sys.path:
    sys.path.append(str(screen_arrows_code_dir))
if str(witness_file_code_dir) not in sys.path:
    sys.path.append(str(witness_file_code_dir))
if str(database_code_dir) not in sys.path:
    sys.path.append(str(database_code_dir))
if str(witness_button_code_dir) in sys.path:
    sys.path.remove(str(witness_button_code_dir))
sys.path.insert(0, str(witness_button_code_dir))

# Streamlit keeps imported modules alive between reruns. Force this helper to
# reload from the shared Witness shortcut folder.
sys.modules.pop("witness_button", None)

from back_to_main_menu import get_back_button_css, get_back_button_html, render_back_button_streamlit
from screen_arrows import screen_arrow_css, make_screen_arrow_button
from person_birth_details import get_person_birth_details
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

# Tilføj mistænkte her. Felter svarende til formularen i billedet.
# "photo" kan være en absolut sti til et billede, eller None.
CHARS_DIR = project_root / "Characters"



def _character_photo_path(person_id: int) -> str | None:
    standard_path = CHARS_DIR / f"Char_{person_id}.png"

    if standard_path.exists():
        return str(standard_path)
    return None


def _short_text(text: str, limit: int = 62) -> str:
    text = " ".join(str(text).split())
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def _line_count(text: str, chars_per_line: int = 58, max_lines: int = 3) -> int:
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
    extra_class: str = "",
) -> str:
    safe_label = html.escape(label)
    safe_value = html.escape(str(value))
    lines = _line_count(str(value), chars_per_line=chars_per_line) if tall else 1
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
) -> str:
    return f"""
                    <div class="sf-entry-split">
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


def _suspect_fields_html(suspect: dict) -> str:
    return "".join(
        [
            _field_html("Full Name:", suspect["full_name"], single=True),
            _field_html("Occupation:", suspect["occupation"], single=True),
            _split_field_html(
                "Age:",
                suspect["age"],
                "Date of Birth:",
                suspect["date_of_birth"],
            ),
            _field_html(
                "Personal Characteristics:",
                suspect["personal_characteristics"],
                tall=True,
                chars_per_line=88,
            ),
            _field_html(
                "Clothing:",
                suspect["clothing"],
                tall=True,
                chars_per_line=88,
                extra_class="sf-clothing-entry",
            ),
            _field_html(
                "Distinguishing Features:",
                suspect["distinguishing_features"],
                tall=True,
                chars_per_line=88,
            ),
            _field_html("Relationship to Case:", suspect["relationship_to_case"], single=True),
            _field_html("Reason for Suspicion:", suspect["reason_for_suspicion"], single=True),
            _field_html(
                "Observed Behavior:",
                suspect["observed_behavior"],
                tall=True,
                chars_per_line=82,
                extra_class="sf-observed-entry",
            ),
            _field_html(
                "Connection to Case:",
                suspect["connection_to_case"],
                single=True,
                extra_class="sf-connection-entry",
            ),
            _field_html("Alibi:", suspect["alibi"], tall=True, chars_per_line=88),
        ]
    )


def _person_to_suspect(person: dict) -> dict:
    person_id = person.get("id", 0)
    birth_details = get_person_birth_details(person_id)
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
        "id": person_id,
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
        "reason_for_suspicion": "Flagged in Witness Overview",
        "observed_behavior": _short_text(get_witness_statement(person), 130),
        "connection_to_case": f"Presence log: {arrived} - {left}",
        "alibi": f"Registered presence: {arrived} - {left}",
        "photo": _character_photo_path(person_id),
    }


# Backwards compatibility for pages that import SUSPECTS directly, such as
# Arrest person. The suspects page itself filters this through
# get_marked_suspects().
SUSPECTS = [_person_to_suspect(person) for person in PERSONS]


def get_marked_suspects() -> list[dict]:
    suspicious_ids = st.session_state.get("wo_suspicious", set())

    if not suspicious_ids:
        return [
            {
                "full_name": "No suspects marked",
                "occupation": "Use Witness Overview",
                "age": "",
                "date_of_birth": "",
                "personal_characteristics": "Mark people with the checkbox in Witness Overview.",
                "clothing": "",
                "distinguishing_features": "",
                "relationship_to_case": "",
                "reason_for_suspicion": "No one has been flagged yet.",
                "observed_behavior": "",
                "connection_to_case": "",
                "alibi": "",
                "photo": None,
            }
        ]

    return [
        _person_to_suspect(person)
        for person in PERSONS
        if person.get("id") in suspicious_ids
    ]


def image_to_base64(image_path: Path) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


def find_background_image(assets_dir: Path) -> Path:
    for file_path in sorted(assets_dir.iterdir()):
        if file_path.is_file() and file_path.suffix.lower() in IMAGE_EXTENSIONS:
            return file_path
    raise FileNotFoundError(f"No background image found in: {assets_dir}")


def show_suspects() -> None:
    back_btn_html = get_back_button_html(btn_key="sp_back")
    back_btn_css = get_back_button_css(left="1.2%", top="2.0%", width="13%")
    witness_overview_tab_html = get_witness_overview_button_html(btn_key="sp_tab_overview")
    witness_overview_tab_css = get_witness_overview_button_css(
        css_class="witness-overview-tab",
        left="82.7%",
        top="27.7%",
        selected=False,
    )
    witness_file_tab_html = get_witness_file_button_html(btn_key="sp_tab_file")
    witness_file_tab_css = get_witness_file_button_css(
        css_class="witness-file-tab",
        left="82.9%",
        top="46.8%",
        selected=False,
    )
    suspect_tab_html = get_witness_red_button_html(btn_key="sp_tab_suspects")
    suspect_tab_css = get_witness_red_button_css(
        css_class="witness-red-tab",
        left="82.9%",
        top="11.6%",
        selected=True,
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

    suspects = get_marked_suspects()
    total_suspects = len(suspects)

    if "suspect_index" not in st.session_state:
        st.session_state.suspect_index = 0

    current_index = st.session_state.suspect_index % max(total_suspects, 1)
    suspect = suspects[current_index]
    counter_text = f"{current_index + 1} / {total_suspects}"

    left_arrow_html = make_screen_arrow_button(
        direction="left",
        onclick="navigate('prev')",
        css_class="suspect-arrow-left",
        aria_label="Previous suspect",
    )
    right_arrow_html = make_screen_arrow_button(
        direction="right",
        onclick="navigate('next')",
        css_class="suspect-arrow-right",
        aria_label="Next suspect",
    )

    photo_html = ""
    if suspect.get("photo"):
        photo_path = Path(suspect["photo"])
        if photo_path.exists():
            photo_b64 = image_to_base64(photo_path)
            photo_html = f"""
            <img
                class="suspect-photo"
                src="data:image/png;base64,{photo_b64}"
                alt="Suspect photo"
            >
            """

    suspect_fields_html = _suspect_fields_html(suspect)

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

        .suspect-page {{
            width: 100vw;
            height: 100vh;
            overflow: hidden;
            background: #3a1f0f;
            display: flex;
            justify-content: center;
            align-items: center;
        }}

        .suspect-stage {{
            position: relative;
            width: min(100vw, calc(100vh * {aspect_ratio}));
            aspect-ratio: {aspect_ratio};
            overflow: hidden;
        }}

        .suspect-bg {{
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            object-fit: contain;
            z-index: 1;
            user-select: none;
            pointer-events: none;
        }}

        /* Mistænkt-foto vises oven på siluet-pladsen på venstre side */
        .suspect-photo {{
            position: absolute;
            left: 19.9%;
            top: 15%;
            width: 25%;
            height: 68%;
            object-fit: contain;
            z-index: 3;
            pointer-events: none;
        }}

        /* Feltværdier på højre side */
        .suspect-fields {{
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

        .sf-observed-entry .sf-line {{
            margin-top: -0.5em;
        }}

        .sf-observed-entry .sf-line {{
            margin-top: -0.5em;
            height: calc(var(--lines, 1) * 1.20em);
            min-height: calc(var(--lines, 1) * 1.20em);
        }}

        .sf-observed-entry .sf-field {{
            top: 1.30em;
        }}

        .sf-single {{
            white-space: nowrap;
            text-overflow: ellipsis;
        }}

        .sf-wrap {{
            white-space: normal;
        }}

        .sf-connection-entry {{
            margin-top: -1.5em;
        }}

        .sf-connection-entry .sf-line {{
            margin-top: -0.25em;
        }}

        .sf-connection-entry .sf-field {{
            top: 0.35em;
        }}

        .sf-clothing-entry {{
            margin-bottom: 1em;
        }}

        {back_btn_css}

        {witness_overview_tab_css}

        {witness_file_tab_css}

        {suspect_tab_css}

        {witness_green_tab_css}

        {screen_arrow_css()}

        .suspect-arrow-left {{
            left: 1.0%;
            top: 35%;
            width: 8%;
            height: 28%;
        }}

        .suspect-arrow-right {{
            right: 1.0%;
            top: 35%;
            width: 8%;
            height: 28%;
        }}

        .suspect-counter {{
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
        <div class="suspect-page">
            {back_btn_html}
            <div class="suspect-stage">

                <img
                    class="suspect-bg"
                    src="data:image/png;base64,{background_b64}"
                    alt="Suspect file"
                >

                {photo_html}

                {witness_overview_tab_html}

                {witness_file_tab_html}

                {suspect_tab_html}

                {witness_green_tab_html}

                <div class="suspect-fields">
                    {suspect_fields_html}
                </div>

                {left_arrow_html}
                {right_arrow_html}

                <div class="suspect-counter">{counter_text}</div>

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

    render_back_button_streamlit(btn_key="sp_back", target_page="main_menu")
    render_witness_overview_button_streamlit(btn_key="sp_tab_overview", target_page="witnesses")
    render_witness_file_button_streamlit(btn_key="sp_tab_file", target_page="witness_file")
    render_witness_red_button_streamlit(btn_key="sp_tab_suspects", target_page="suspects")

    col_prev, col_next = st.columns(2)
    with col_prev:
        if st.button("prev", key="sp_prev"):
            if total_suspects > 0:
                st.session_state.suspect_index = (
                    st.session_state.suspect_index - 1
                ) % total_suspects
                st.rerun()
    with col_next:
        if st.button("next", key="sp_next"):
            if total_suspects > 0:
                st.session_state.suspect_index = (
                    st.session_state.suspect_index + 1
                ) % total_suspects
                st.rerun()

