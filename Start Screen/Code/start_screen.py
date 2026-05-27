import base64
from pathlib import Path

import streamlit as st


IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp")


def image_to_base64(image_path: Path) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


def find_first_image(assets_dir: Path) -> Path:

    for image_path in sorted(assets_dir.iterdir()):
        if image_path.suffix.lower() in IMAGE_EXTENSIONS:
            return image_path

    raise FileNotFoundError(f"No image file found in: {assets_dir}")


def set_background(image_path: Path) -> None:
    encoded_image = image_to_base64(image_path)

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_image}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}

        [data-testid="stHeader"] {{
            background: rgba(0, 0, 0, 0);
        }}

        [data-testid="stToolbar"] {{
            display: none;
        }}

        .block-container {{
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 0rem;
            padding-right: 0rem;
            max-width: 100%;
        }}

        .start-screen-title {{
            text-align: center;
            color: #f5d28a;
            font-size: 64px;
            font-weight: 900;
            text-shadow: 3px 3px 8px black;
            margin-top: 55px;
        }}

        .menu-click-zone {{
            position: fixed;
            display: block;
            z-index: 9999;
            text-decoration: none;
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

        /* START-skilt */
        .start-zone {{
            left: 17.4vw;
            top: 70.8vh;
            width: 15.5vw;
            height: 17.5vh;
            clip-path: polygon(
                13% 6%,
                88% 6%,
                96% 94%,
                6% 94%
            );
        }}

        .start-zone::after {{
            clip-path: polygon(
                13% 6%,
                88% 6%,
                96% 94%,
                6% 94%
            );
        }}

        /* EXIT-skilt */
        .exit-zone {{
            left: 78.3vw;
            top: 75.2vh;
            width: 13.5vw;
            height: 15.8vh;
            clip-path: polygon(
                10% 5%,
                90% 5%,
                97% 95%,
                4% 95%
            );
        }}

        .exit-zone::after {{
            clip-path: polygon(
                10% 5%,
                90% 5%,
                97% 95%,
                4% 95%
            );
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def handle_start_screen_navigation() -> None:
    page_from_url = st.query_params.get("page")

    if page_from_url == "main_menu":
        st.session_state["page"] = "main_menu"
        st.query_params.clear()
        st.rerun()

    if page_from_url == "exit":
        st.session_state["page"] = "exit"
        st.query_params.clear()
        st.rerun()


def show_start_screen() -> None:
    # Denne fil ligger i: Start Screen / Code / start_screen.py
    # Derfor er parents[1] selve Start Screen-mappen.
    feature_dir = Path(__file__).resolve().parents[1]
    assets_dir = feature_dir / "Assets"

    try:
        background_path = find_first_image(assets_dir)
    except FileNotFoundError as error:
        st.error(str(error))
        st.stop()

    set_background(background_path)
    handle_start_screen_navigation()

    st.markdown(
        '<div class="start-screen-title">JEWEL HEIST DATABASE</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <a class="menu-click-zone start-zone" href="?page=main_menu" aria-label="Start"></a>
        <a class="menu-click-zone exit-zone" href="?page=exit" aria-label="Exit"></a>
        """,
        unsafe_allow_html=True,
    )
