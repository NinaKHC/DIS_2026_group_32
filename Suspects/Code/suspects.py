import base64
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


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}

# Tilføj mistænkte her. Felter svarende til formularen i billedet.
# "photo" kan være en absolut sti til et billede, eller None.
SUSPECTS = [
    {
        "full_name": "",
        "occupation": "",
        "age": "",
        "date_of_birth": "",
        "personal_characteristics": "",
        "clothing": "",
        "distinguishing_features": "",
        "relationship_to_case": "",
        "reason_for_suspicion": "",
        "observed_behavior": "",
        "connection_to_case": "",
        "alibi": "",
        "photo": None,
    },
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

    total_suspects = len(SUSPECTS)

    if "suspect_index" not in st.session_state:
        st.session_state.suspect_index = 0

    current_index = st.session_state.suspect_index % max(total_suspects, 1)
    suspect = SUSPECTS[current_index]
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
            left: 6.5%;
            top: 11%;
            width: 34%;
            height: 77%;
            object-fit: contain;
            z-index: 3;
            pointer-events: none;
        }}

        /* Feltværdier på højre side */
        .suspect-fields {{
            position: absolute;
            left: 55.5%;
            top: 10%;
            width: 39%;
            z-index: 3;
            display: flex;
            flex-direction: column;
            font-family: 'Georgia', serif;
            color: #1a0e07;
        }}

        .sf-row {{
            display: flex;
            align-items: baseline;
            height: 7.5%;
        }}

        .sf-row-double {{
            display: flex;
            align-items: baseline;
            height: 7.5%;
        }}

        .sf-row-tall {{
            display: flex;
            align-items: flex-start;
            height: 11%;
        }}

        .sf-value {{
            font-size: clamp(9px, 0.9vw, 15px);
            font-weight: 600;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            flex: 1;
            padding-left: 0.15em;
        }}

        .sf-value-age {{
            font-size: clamp(9px, 0.9vw, 15px);
            font-weight: 600;
            white-space: nowrap;
            width: 20%;
            padding-left: 0.15em;
        }}

        .sf-value-dob {{
            font-size: clamp(9px, 0.9vw, 15px);
            font-weight: 600;
            white-space: nowrap;
            flex: 1;
            padding-left: 0.15em;
        }}

        .sf-value-text {{
            font-size: clamp(8px, 0.8vw, 13px);
            font-weight: 500;
            white-space: pre-wrap;
            word-break: break-word;
            line-height: 1.55;
            padding-left: 0.15em;
            flex: 1;
        }}

        {back_btn_css}

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

                <div class="suspect-fields">
                    <div class="sf-row">
                        <span class="sf-value">{suspect['full_name']}</span>
                    </div>
                    <div class="sf-row">
                        <span class="sf-value">{suspect['occupation']}</span>
                    </div>
                    <div class="sf-row-double">
                        <span class="sf-value-age">{suspect['age']}</span>
                        <span class="sf-value-dob">{suspect['date_of_birth']}</span>
                    </div>
                    <div class="sf-row-tall">
                        <span class="sf-value-text">{suspect['personal_characteristics']}</span>
                    </div>
                    <div class="sf-row-tall">
                        <span class="sf-value-text">{suspect['clothing']}</span>
                    </div>
                    <div class="sf-row-tall">
                        <span class="sf-value-text">{suspect['distinguishing_features']}</span>
                    </div>
                    <div class="sf-row">
                        <span class="sf-value">{suspect['relationship_to_case']}</span>
                    </div>
                    <div class="sf-row">
                        <span class="sf-value">{suspect['reason_for_suspicion']}</span>
                    </div>
                    <div class="sf-row">
                        <span class="sf-value">{suspect['observed_behavior']}</span>
                    </div>
                    <div class="sf-row">
                        <span class="sf-value">{suspect['connection_to_case']}</span>
                    </div>
                    <div class="sf-row">
                        <span class="sf-value">{suspect['alibi']}</span>
                    </div>
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
