import base64
from pathlib import Path

import streamlit as st


_ASSETS_DIR = Path(__file__).resolve().parents[1] / "Assets"
_FRAME_FILE = _ASSETS_DIR / "Picture_frame.png"


def _b64(path: Path) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


@st.cache_data
def _cached_b64(path: Path) -> str:
    return _b64(path)


def get_picture_frame_css(
    css_class: str = "pf-frame",
    left: str = "17%",
    top: str = "7.5%",
    width: str = "31.5%",
    height: str = "27.5%",
    photo_position: str = "50% 10%",
    photo_scale: float = 1.6,
    photo_fit: str = "cover",
) -> str:
    return f"""
    .{css_class} {{
        position: absolute;
        left: {left};
        top: {top};
        width: {width};
        height: {height};
        z-index: 8;
    }}

    .{css_class} .pf-frame-bg {{
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        object-fit: fill;
        z-index: 1;
        pointer-events: none;
        user-select: none;
    }}

    .{css_class} .pf-photo-clip {{
        position: absolute;
        left: 3%;
        top: 9%;
        width: 94%;
        height: 83%;
        overflow: hidden;
        z-index: 2;
    }}

    .{css_class} .pf-photo {{
        width: 100%;
        height: 100%;
        object-fit: {photo_fit};
        object-position: {photo_position if photo_fit == "cover" else "center"};
        transform: scale({photo_scale if photo_fit == "cover" else 1.0});
        transform-origin: {photo_position if photo_fit == "cover" else "center"};
        pointer-events: none;
        user-select: none;
    }}
    """


def get_picture_frame_html(
    photo_path: Path | None = None,
    css_class: str = "pf-frame",
    alt: str = "",
) -> str:
    if not _FRAME_FILE.exists():
        return ""

    frame_b64 = _cached_b64(_FRAME_FILE)

    photo_tag = ""
    if photo_path is not None and Path(photo_path).exists():
        photo_b64 = _cached_b64(Path(photo_path))
        photo_tag = (
            f'<div class="pf-photo-clip">'
            f'<img class="pf-photo" '
            f'src="data:image/png;base64,{photo_b64}" '
            f'alt="{alt}">'
            f'</div>'
        )

    return f"""
    <div class="{css_class}">
        <img class="pf-frame-bg"
             src="data:image/png;base64,{frame_b64}"
             alt="Picture frame">
        {photo_tag}
    </div>
    """
