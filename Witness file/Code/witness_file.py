import base64
import sys
from pathlib import Path

from PIL import Image
import streamlit as st
import streamlit.components.v1 as components

from sqlalchemy import text


project_root = Path(__file__).resolve().parents[2]
back_button_code_dir = project_root / "Back to main menu" / "Code"
screen_arrows_code_dir = project_root / "Screen arrows" / "Code"

if str(back_button_code_dir) not in sys.path:
    sys.path.append(str(back_button_code_dir))
if str(screen_arrows_code_dir) not in sys.path:
    sys.path.append(str(screen_arrows_code_dir))

from back_to_main_menu import get_back_button_css, get_back_button_html, render_back_button_streamlit
from screen_arrows import screen_arrow_css, make_screen_arrow_button


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}

"""
Tænker at vores SQL skal kunne oprette en "witnesses" tabel med følgende kolonner:
CREATE TABLE witnesses (
    id          SERIAL PRIMARY KEY,
    full_name   TEXT,
    occupation  TEXT,
    age         TEXT,
    date_of_birth TEXT,
    personal_characteristics TEXT,
    clothing    TEXT,
    distinguishing_features  TEXT,
    relationship_to_case     TEXT,
    alibi       TEXT,
    witness_statement        TEXT,
    photo_path  TEXT   -- optional: sti til billede
);
"""


conn = st.connection("postgresql", type="sql")
#    witness["full_name"] = conn.query('SELECT name FROM Person;', ttl="0m")

num_witnesses = conn.session.execute(text("SELECT COUNT(*) FROM Person;")).first()[0]
names = conn.session.execute(text("SELECT name FROM Person;")).all()
id = conn.session.execute(text("SELECT person_id FROM Person;")).all()
occupation = conn.session.execute(text("SELECT role FROM Person;")).all()
clothing = conn.session.execute(text("SELECT clothing FROM Person")).all()

WITNESSES = [{
        "full_name": "test",
        "occupation": "",
        "age": "",
        "date_of_birth": "",
        "personal_characteristics": "",
        "clothing": "",
        "distinguishing_features": "",
        "relationship_to_case": "",
        "alibi": "",
        "witness_statement": "",
        "photo": None,
    } for x in range(num_witnesses)]

for i in range(num_witnesses):
    WITNESSES[id[i][0] - 1]["full_name"] = names[i][0]
    WITNESSES[id[i][0] - 1]["occupation"] = occupation[i][0]
    WITNESSES[id[i][0] - 1]["clothing"] = clothing[i][0]

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

    total_witnesses = len(WITNESSES)

    if "witness_index" not in st.session_state:
        st.session_state.witness_index = 0

    current_index = st.session_state.witness_index % max(total_witnesses, 1)
    witness = WITNESSES[current_index]
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

        /* Vidne-foto vises oven på siluet-pladsen på venstre side */
        .witness-photo {{
            position: absolute;
            left: 6.5%;
            top: 11%;
            width: 34%;
            height: 77%;
            object-fit: contain;
            z-index: 3;
            pointer-events: none;
        }}

        /* Feltværdier oven på de stiplede linjer på højre side */
        .witness-fields {{
            position: absolute;
            left: 53%;
            top: 17%;
            width: 39%;
            z-index: 3;
            display: flex;
            flex-direction: column;
            font-family: 'Georgia', serif;
            color: #1a0e07;
        }}

        .wf-row {{
            display: flex;
            align-items: baseline;
            height: 55px;
        }}

        .wf-row-double {{
            display: flex;
            align-items: baseline;
            height: 52px;
        }}

        .wf-row-tall {{
            display: flex;
            align-items: flex-start;
            height: 104px;
        }}

        .wf-value {{
            font-size: clamp(9px, 0.9vw, 15px);
            font-weight: 600;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            flex: 1;
            padding-left: 0.15em;
        }}

        .wf-value-age {{
            font-size: clamp(9px, 0.9vw, 15px);
            font-weight: 600;
            white-space: nowrap;
            width: 20%;
            padding-left: 0.15em;
        }}

        .wf-value-dob {{
            font-size: clamp(9px, 0.9vw, 15px);
            font-weight: 600;
            white-space: nowrap;
            flex: 1;
            padding-left: 0.15em;
        }}

        .wf-value-statement {{
            font-size: clamp(8px, 0.8vw, 13px);
            font-weight: 500;
            white-space: pre-wrap;
            word-break: break-word;
            line-height: 1.55;
            padding-left: 0.15em;
            flex: 1;
        }}
        .wf-value-name{{
            position: relative;
            left: 172px;
            font-size: 170%;
            top: 40%;
        }}
        .wf-value-occupation{{
            position: relative;
            top: 14px;
            left: 172px;
            font-size: 170%;
            top: 39%;
        }}
        .wf-value-clothing{{
            position: relative;
            max-width: 62%;
            text-indent: 23%;
            font-size: 120%;
            top: 12%;
            line-height: 240%
        }}

        {back_btn_css}

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

                <div class="witness-fields">
                    <div class="wf-row">
                        <span class="wf-value-name">{witness['full_name']}</span>
                    </div>
                    <div class="wf-row">
                        <span class="wf-value-occupation">{witness['occupation']}</span>
                    </div>
                    <div class="wf-row-double">
                        <span class="wf-value-age">{witness['age']}</span>
                        <span class="wf-value-dob">{witness['date_of_birth']}</span>
                    </div>
                    <div class="wf-row-tall">
                        <span class="wf-value-statement">{witness['personal_characteristics']}</span>
                    </div>
                    <div class="wf-row-tall">
                        <span class="wf-value-clothing">{witness['clothing']}</span>
                    </div>
                    <div class="wf-row-tall">
                        <span class="wf-value-statement">{witness['distinguishing_features']}</span>
                    </div>
                    <div class="wf-row">
                        <span class="wf-value">{witness['relationship_to_case']}</span>
                    </div>
                    <div class="wf-row">
                        <span class="wf-value">{witness['alibi']}</span>
                    </div>
                    <div class="wf-row-tall">
                        <span class="wf-value-statement">{witness['witness_statement']}</span>
                    </div>
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
