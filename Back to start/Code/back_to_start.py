import base64
from pathlib import Path

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = PROJECT_ROOT / "Back to start" / "Assets"


def _image_to_base64(image_path: Path) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


def get_back_to_start_button_css(
    class_name: str = "back-to-start-btn",
    left: str = "1.0%",
    top: str = "1.5%",
    width: str = "16%",
    height: str = "auto",
) -> str:
    height_rule = f"height:{height};" if height != "auto" else ""
    return f"""
    .{class_name} {{
        position:absolute;
        left:{left};
        top:{top};
        width:{width};
        {height_rule}
        z-index:20;
        cursor:pointer;
        background:transparent;
        border:0;
        padding:0;
        margin:0;
        transition:filter 0.15s ease, transform 0.15s ease;
    }}
    .{class_name}:hover {{
        filter:brightness(1.12);
        transform:scale(1.025);
    }}
    .{class_name} img {{
        width:100%;
        height:100%;
        object-fit:contain;
        display:block;
        user-select:none;
        pointer-events:none;
    }}
    """


def get_back_to_start_button_html(
    btn_key: str = "back_to_start",
    image_name: str = "Back_to_start.png",
    class_name: str = "back-to-start-btn",
    label: str = "Back to Start",
) -> str:
    image_path = ASSETS_DIR / image_name
    if not image_path.exists():
        return ""

    image_b64 = _image_to_base64(image_path)
    return f"""
    <button class="{class_name}" onclick="navigate('{btn_key}')" aria-label="{label}">
        <img src="data:image/png;base64,{image_b64}" alt="{label}">
    </button>
    """


def render_back_to_start_streamlit(btn_key: str, target_page: str = "start_screen") -> None:
    if st.button(btn_key, key=f"bts_hidden_{btn_key}"):
        st.session_state["page"] = target_page
        st.rerun()
