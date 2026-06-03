import base64
from pathlib import Path

import streamlit as st


ASSETS_DIR = Path(__file__).resolve().parents[1] / "Assets"


def _image_to_base64(image_path: Path) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


def _asset_data_url(filename: str) -> str:
    image_path = ASSETS_DIR / filename
    if not image_path.exists():
        return ""
    return f"data:image/png;base64,{_image_to_base64(image_path)}"


def get_witness_button_css(
    css_class: str,
    left: str,
    top: str,
    width: str,
    height: str,
    normal_filename: str,
    highlight_filename: str,
    selected: bool = False,
) -> str:
    normal_url = _asset_data_url(normal_filename)
    highlight_url = _asset_data_url(highlight_filename)
    active_url = highlight_url if selected else normal_url

    if not active_url:
        return ""

    hover_rule = ""
    if highlight_url:
        hover_rule = f"""
        .{css_class}:hover {{
            background-image: url("{highlight_url}");
            filter: brightness(1.04);
        }}
        """

    return f"""
    .{css_class} {{
        position: absolute;
        left: {left};
        top: {top};
        width: {width};
        height: {height};
        z-index: 80;
        cursor: pointer;
        display: block;
        border: none;
        outline: none;
        padding: 0;
        margin: 0;
        background-image: url("{active_url}");
        background-size: contain;
        background-position: center;
        background-repeat: no-repeat;
        transition: filter 0.15s ease, transform 0.15s ease;
    }}

    {hover_rule}
    """


def get_witness_overview_button_css(
    css_class: str = "witness-overview-tab",
    left: str = "84.7%",
    top: str = "22.7%",
    width: str = "5.2%",
    height: str = "17.0%",
    selected: bool = False,
) -> str:
    return get_witness_button_css(
        css_class=css_class,
        left=left,
        top=top,
        width=width,
        height=height,
        normal_filename="Yellow_Normal.png",
        highlight_filename="Yellow_Higlight.png",
        selected=selected,
    )


def get_witness_file_button_css(
    css_class: str = "witness-file-tab",
    left: str = "84.9%",
    top: str = "42.8%",
    width: str = "5.2%",
    height: str = "17.0%",
    selected: bool = False,
) -> str:
    return get_witness_button_css(
        css_class=css_class,
        left=left,
        top=top,
        width=width,
        height=height,
        normal_filename="Blue_Normal.png",
        highlight_filename="Blue_Higlight.png",
        selected=selected,
    )


def get_witness_red_button_css(
    css_class: str = "witness-red-tab",
    left: str = "84.9%",
    top: str = "8.6%",
    width: str = "5.2%",
    height: str = "17.0%",
    selected: bool = False,
) -> str:
    return get_witness_button_css(
        css_class=css_class,
        left=left,
        top=top,
        width=width,
        height=height,
        normal_filename="Red_Normal.png",
        highlight_filename="Red_Higlight.png",
        selected=selected,
    )


def get_witness_green_button_css(
    css_class: str = "witness-green-tab",
    left: str = "84.9%",
    top: str = "62.8%",
    width: str = "5.2%",
    height: str = "17.0%",
    selected: bool = False,
) -> str:
    return get_witness_button_css(
        css_class=css_class,
        left=left,
        top=top,
        width=width,
        height=height,
        normal_filename="Green_Normal.png",
        highlight_filename="Green_Higlight.png",
        selected=selected,
    )


def get_witness_overview_button_html(
    btn_key: str = "wb_witness_overview",
    css_class: str = "witness-overview-tab",
    label: str = "Witness Overview",
) -> str:
    return f"""
    <div class="{css_class}" onclick="navigate('{btn_key}')" role="button" aria-label="{label}"></div>
    """


def get_witness_file_button_html(
    btn_key: str = "wb_witness_file",
    css_class: str = "witness-file-tab",
    label: str = "Witness File",
) -> str:
    return f"""
    <div class="{css_class}" onclick="navigate('{btn_key}')" role="button" aria-label="{label}"></div>
    """


def get_witness_search_button_html(
    btn_key: str = "wb_witness_search",
    css_class: str = "witness-green-tab",
    label: str = "Witness Search",
) -> str:
    return f"""
    <div class="{css_class}" onclick="navigate('{btn_key}')" role="button" aria-label="{label}"></div>
    """


def get_witness_red_button_html(
    btn_key: str = "wb_suspects",
    css_class: str = "witness-red-tab",
    label: str = "Suspects",
) -> str:
    return f"""
    <div class="{css_class}" onclick="navigate('{btn_key}')" role="button" aria-label="{label}"></div>
    """


def render_witness_overview_button_streamlit(
    btn_key: str = "wb_witness_overview",
    target_page: str = "witnesses",
) -> None:
    if st.button(btn_key, key=f"wb_hidden_{btn_key}"):
        st.session_state["page"] = target_page
        st.rerun()


def render_witness_file_button_streamlit(
    btn_key: str = "wb_witness_file",
    target_page: str = "witness_file",
) -> None:
    if st.button(btn_key, key=f"wb_hidden_{btn_key}"):
        st.session_state["page"] = target_page
        st.rerun()


def render_witness_red_button_streamlit(
    btn_key: str = "wb_suspects",
    target_page: str = "suspects",
) -> None:
    if st.button(btn_key, key=f"wb_hidden_{btn_key}"):
        st.session_state["page"] = target_page
        st.rerun()


def render_witness_search_button_streamlit(
    btn_key: str = "wb_witness_search",
    target_page: str = "witness_search",
) -> None:
    if st.button(btn_key, key=f"wb_hidden_{btn_key}"):
        st.session_state["page"] = target_page
        st.rerun()
