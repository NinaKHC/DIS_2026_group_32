import base64
from pathlib import Path

import streamlit as st


def image_to_base64(image_path: Path) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


def _get_image_path() -> Path:
    feature_dir = Path(__file__).resolve().parents[1]
    return feature_dir / "Assets" / "back_to_main_menu.png"


def get_back_button_css(left: str = "1.2%", top: str = "2%", width: str = "16%") -> str:
    """
    Returnerer CSS til back-knappen til brug INDE I en components.html() iframe.
    """
    return f"""
    .back-btn-overlay {{
        position: absolute;
        left: {left};
        top: {top};
        width: {width};
        cursor: pointer;
        z-index: 100;
        transition: transform 0.15s ease, filter 0.15s ease;
    }}

    .back-btn-overlay:hover {{
        transform: scale(1.04);
        filter: brightness(1.08);
    }}

    .back-btn-overlay img {{
        width: 100%;
        height: auto;
        display: block;
        pointer-events: none;
        user-select: none;
    }}
    """


def get_back_button_html(btn_key: str = "back_btn") -> str:
    """
    Returnerer HTML til back-knappen til brug INDE I en components.html() iframe.
    btn_key skal matche den tekst der bruges i det skjulte st.button() kald udenfor iframe'en.
    Kalder navigate(btn_key) — sørg for at navigate()-funktionen er defineret i iframens JS.
    """
    image_path = _get_image_path()

    if not image_path.exists():
        return ""

    encoded_image = image_to_base64(image_path)

    return f"""
    <div class="back-btn-overlay" onclick="navigate('{btn_key}')" aria-label="Back to Main Menu">
        <img src="data:image/png;base64,{encoded_image}" alt="Back to Main Menu">
    </div>
    """


def render_back_button_streamlit(btn_key: str, target_page: str) -> None:
    """
    Rendrer det skjulte Streamlit st.button() der håndterer navigation.
    Kaldes udenfor iframe'en — matcher btn_key i get_back_button_html().
    """
    if st.button(btn_key, key=f"btmm_hidden_{btn_key}"):
        st.session_state["page"] = target_page
        st.rerun()
