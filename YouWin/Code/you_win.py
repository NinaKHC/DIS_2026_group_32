import base64
import sys
from pathlib import Path

from PIL import Image
import streamlit as st
import streamlit.components.v1 as components


project_root = Path(__file__).resolve().parents[2]
back_button_code_dir = project_root / "Back to start" / "Code"

if str(back_button_code_dir) not in sys.path:
    sys.path.append(str(back_button_code_dir))

from back_to_start import (
    get_back_to_start_button_css,
    get_back_to_start_button_html,
    render_back_to_start_streamlit,
)


ASSETS_DIR = Path(__file__).resolve().parents[1] / "Assets"

PHOTO_LEFT = 39.8
PHOTO_TOP = 27.2
PHOTO_WIDTH = 20.0
PHOTO_HEIGHT = 35.7

NAME_LEFT = 26.5
NAME_TOP = 73.5
NAME_WIDTH = 37.0
NAME_HEIGHT = 9.0


def _b64(path: Path) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


@st.cache_data
def _cached_b64(path: Path) -> str:
    return _b64(path)


def _aspect(path: Path) -> float:
    with Image.open(path) as img:
        w, h = img.size
    return w / h


def show_you_win() -> None:
    bg_path = ASSETS_DIR / "Youwin.png"
    if not bg_path.exists():
        st.error(f"Image not found: {bg_path}")
        st.stop()

    bg_b64  = _cached_b64(bg_path)
    aspect  = _aspect(bg_path)

    guilty_name  = st.session_state.get("result_guilty_name",  "")
    guilty_photo = st.session_state.get("result_guilty_photo", None)

    photo_html = ""
    if guilty_photo:
        p = Path(guilty_photo)
        if p.exists():
            photo_html = (
                f'<img style="position:absolute;left:{PHOTO_LEFT}%;top:{PHOTO_TOP}%;'
                f'width:{PHOTO_WIDTH}%;height:{PHOTO_HEIGHT}%;'
                f'object-fit:contain;z-index:10;pointer-events:none;user-select:none;"'
                f' src="data:image/png;base64,{_cached_b64(p)}" alt="Guilty person">'
            )

    name_style = (
        f"position:absolute;left:{NAME_LEFT}%;top:{NAME_TOP}%;"
        f"width:{NAME_WIDTH}%;height:{NAME_HEIGHT}%;"
        "display:flex;align-items:center;justify-content:center;"
        "z-index:10;pointer-events:none;"
        "font-family:Georgia,serif;font-size:clamp(17px,1.95vw,33px);"
        "font-weight:bold;color:#2a1a0a;text-align:center;"
        "white-space:nowrap;overflow:hidden;text-overflow:ellipsis;"
    )

    back_btn_html = get_back_to_start_button_html(btn_key="yw_back")
    back_btn_css  = get_back_to_start_button_css(left="1.0%", top="1.5%", width="18%")

    st.markdown(
        """
        <style>
        html, body, .stApp { margin:0!important;padding:0!important;overflow:hidden!important;background:#1a0a04!important; }
        [data-testid="stHeader"] { background:rgba(0,0,0,0)!important;height:0rem!important; }
        [data-testid="stToolbar"],[data-testid="stDecoration"] { display:none!important; }
        .block-container { padding:0!important;margin:0!important;max-width:100%!important;height:100vh!important;overflow:hidden!important; }
        section.main,div[data-testid="stAppViewContainer"],div[data-testid="stVerticalBlock"] { overflow:hidden!important; }
        iframe { width:100vw!important;height:100vh!important;display:block!important;border:none!important; }
        .element-container:has(iframe) { width:100vw!important;height:100vh!important;overflow:hidden!important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    html = f"""
    <!DOCTYPE html><html><head>
    <style>
    html,body{{margin:0;padding:0;width:100vw;height:100vh;overflow:hidden;background:#1a0a04;}}
    .yw-page{{width:100vw;height:100vh;display:flex;justify-content:center;align-items:center;background:#1a0a04;}}
    .yw-stage{{position:relative;width:min(100vw,calc(100vh*{aspect}));aspect-ratio:{aspect};}}
    .yw-bg{{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;z-index:1;pointer-events:none;user-select:none;}}
    {back_btn_css}
    </style></head>
    <body>
    <div class="yw-page">
        <div class="yw-stage">
            {back_btn_html}
            <img class="yw-bg" src="data:image/png;base64,{bg_b64}" alt="You Win">
            {photo_html}
            <div style="{name_style}">{guilty_name}</div>
        </div>
    </div>
    <script>
    let navigationPending = false;
    function navigate(page) {{
        if (navigationPending) return;
        navigationPending = true;

        let attempts = 0;
        const clickWhenReady = function() {{
            attempts += 1;
            var btns = window.parent.document.querySelectorAll('button');
            for (var i = 0; i < btns.length; i++) {{
                if (btns[i].innerText.trim() === page && !btns[i].disabled) {{
                    btns[i].click();
                    return;
                }}
            }}

            if (attempts < 20) {{
                window.setTimeout(clickWhenReady, 75);
            }} else {{
                navigationPending = false;
            }}
        }};

        window.setTimeout(clickWhenReady, 120);
    }}
    </script>
    </body></html>
    """

    components.html(html, height=1, scrolling=False)
    render_back_to_start_streamlit(btn_key="yw_back", target_page="start_screen")
