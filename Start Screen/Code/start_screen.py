import base64
import sys
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp")

project_root = Path(__file__).resolve().parents[2]
start_game_code_dir = project_root / "Start Game" / "Code"

if str(start_game_code_dir) not in sys.path:
    sys.path.append(str(start_game_code_dir))

try:
    from start_game import start_new_game, continue_game, is_game_started
except ImportError:
    start_new_game = None
    continue_game = None
    is_game_started = None


def image_to_base64(image_path: Path) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


def find_first_image(assets_dir: Path) -> Path:
    for image_path in sorted(assets_dir.iterdir()):
        if image_path.suffix.lower() in IMAGE_EXTENSIONS:
            return image_path
    raise FileNotFoundError(f"No image file found in: {assets_dir}")


def show_start_screen() -> None:
    feature_dir = Path(__file__).resolve().parents[1]
    assets_dir = feature_dir / "Assets"

    try:
        background_path = find_first_image(assets_dir)
    except FileNotFoundError as error:
        st.error(str(error))
        st.stop()

    background_b64 = image_to_base64(background_path)

    st.markdown(
        """
        <style>
        html, body, .stApp {
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
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
        }}

        .ss-page {{
            width: 100vw;
            height: 100vh;
            background-image: url("data:image/png;base64,{background_b64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            position: relative;
        }}

        .ss-title {{
            text-align: center;
            color: #f5d28a;
            font-size: clamp(28px, 4.5vw, 72px);
            font-weight: 900;
            text-shadow: 3px 3px 8px black;
            padding-top: 55px;
            margin: 0;
            font-family: Georgia, serif;
            user-select: none;
        }}

        .menu-click-zone {{
            position: absolute;
            cursor: pointer;
            background: transparent;
        }}

        .menu-click-zone::after {{
            content: "";
            position: absolute;
            inset: 0;
            border: 3px solid rgba(255, 210, 122, 0.65);
            border-radius: 14px;
            opacity: 0;
            transition: opacity 0.2s ease;
            pointer-events: none;
        }}

        .menu-click-zone:hover::after {{
            opacity: 1;
        }}

        .start-zone {{
            left: 17.4%;
            top: 70.8%;
            width: 15.5%;
            height: 17.5%;
            clip-path: polygon(13% 6%, 88% 6%, 96% 94%, 6% 94%);
        }}

        .start-zone::after {{
            clip-path: polygon(13% 6%, 88% 6%, 96% 94%, 6% 94%);
        }}

        .exit-zone {{
            left: 78.3%;
            top: 75.2%;
            width: 13.5%;
            height: 15.8%;
            clip-path: polygon(10% 5%, 90% 5%, 97% 95%, 4% 95%);
        }}

        .exit-zone::after {{
            clip-path: polygon(10% 5%, 90% 5%, 97% 95%, 4% 95%);
        }}
        </style>
    </head>
    <body>
        <div class="ss-page">
            <div class="ss-title">JEWEL HEIST DATABASE</div>

            <div
                class="menu-click-zone start-zone"
                onclick="navigate('ss_start_game')"
                role="button"
                aria-label="Start">
            </div>
            <div
                class="menu-click-zone exit-zone"
                onclick="navigate('ss_exit')"
                role="button"
                aria-label="Exit">
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

    col1, col2 = st.columns(2)
    with col1:
        if st.button("ss_start_game", key="ss_hidden_start_game"):
            if start_new_game is None:
                st.error(
                    "Could not import start_game.py. "
                    "Check that it is placed in: Start Game/Code/start_game.py"
                )
                st.stop()

            start_page = "main_menu" if st.session_state.get("intro_seen", False) else "intro"
            start_new_game(start_page=start_page)
            st.session_state["page"] = start_page
            st.rerun()

    with col2:
        if st.button("ss_exit", key="ss_hidden_exit"):
            st.session_state["page"] = "exit"
            st.rerun()
