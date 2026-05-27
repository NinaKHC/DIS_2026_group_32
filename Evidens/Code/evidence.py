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


ASSETS_DIR = Path(__file__).resolve().parents[1] / "Assets"

# Maks 8 bevisgenstande (matcher de 8 bokse i Evidens display.png).
# "image_filename" skal være filnavnet i Assets-mappen.
EVIDENCE = [
    {
        "name": "Evidens 1",
        "description": "Skovl fundet ved gerningsstedet",
        "image_filename": "Evidens 1.png",
    },
    # Tilføj flere bevisgenstande her...
]

# Boksenes positioner på Evidens display.png (left%, top%, width%, height%)
BOX_POSITIONS = [
    (14.0, 8.0,  17.0, 38.0),   # Boks 0  (række 1, kol 1)
    (33.0, 8.0,  17.0, 38.0),   # Boks 1  (række 1, kol 2)
    (52.0, 8.0,  17.0, 38.0),   # Boks 2  (række 1, kol 3)
    (71.0, 8.0,  17.0, 38.0),   # Boks 3  (række 1, kol 4)
    (14.0, 54.0, 17.0, 40.0),   # Boks 4  (række 2, kol 1)
    (33.0, 54.0, 17.0, 40.0),   # Boks 5  (række 2, kol 2)
    (52.0, 54.0, 17.0, 40.0),   # Boks 6  (række 2, kol 3)
    (71.0, 54.0, 17.0, 40.0),   # Boks 7  (række 2, kol 4)
]


def image_to_base64(image_path: Path) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def get_aspect_ratio(image_path: Path) -> float:
    with Image.open(image_path) as img:
        w, h = img.size
    return w / h


def _streamlit_chrome_css() -> str:
    return """
        <style>
        html, body, .stApp {
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
            background: #3a1f0f !important;
        }
        [data-testid="stHeader"] { background: rgba(0,0,0,0) !important; height: 0rem !important; }
        [data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }
        .block-container { padding: 0 !important; margin: 0 !important; max-width: 100% !important; height: 100vh !important; overflow: hidden !important; }
        section.main, div[data-testid="stAppViewContainer"], div[data-testid="stVerticalBlock"] { overflow: hidden !important; }
        iframe { width: 100vw !important; height: 100vh !important; display: block !important; border: none !important; }
        .element-container:has(iframe) { width: 100vw !important; height: 100vh !important; overflow: hidden !important; }
        </style>
    """


def _navigate_js() -> str:
    return """
    <script>
    function navigate(page) {
        var buttons = window.parent.document.querySelectorAll('button');
        for (var i = 0; i < buttons.length; i++) {
            if (buttons[i].innerText.trim() === page) {
                buttons[i].click();
                return;
            }
        }
    }
    </script>
    """


def _render_overview(back_btn_html: str, back_btn_css: str) -> None:
    bg_path = ASSETS_DIR / "Evidens display.png"
    if not bg_path.exists():
        st.error(f"Baggrundsbillede ikke fundet: {bg_path}")
        st.stop()

    bg_b64 = image_to_base64(bg_path)
    aspect_ratio = get_aspect_ratio(bg_path)

    boxes_html = ""
    for i, (left, top, width, height) in enumerate(BOX_POSITIONS):
        if i >= len(EVIDENCE):
            break
        item = EVIDENCE[i]
        img_path = ASSETS_DIR / item["image_filename"]
        if not img_path.exists():
            continue
        thumb_b64 = image_to_base64(img_path)
        boxes_html += f"""
        <div
            class="ev-box"
            style="left:{left}%;top:{top}%;width:{width}%;height:{height}%;"
            onclick="navigate('ev_click_{i}')"
            title="{item['name']}"
            role="button"
            aria-label="{item['name']}">
            <img src="data:image/png;base64,{thumb_b64}" alt="{item['name']}">
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
        html, body {{
            margin: 0; padding: 0;
            width: 100vw; height: 100vh;
            overflow: hidden;
            background: #3a1f0f;
        }}

        .ev-page {{
            width: 100vw; height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #3a1f0f;
        }}

        .ev-stage {{
            position: relative;
            width: min(100vw, calc(100vh * {aspect_ratio}));
            aspect-ratio: {aspect_ratio};
        }}

        .ev-bg {{
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            object-fit: contain;
            z-index: 1;
            pointer-events: none;
            user-select: none;
        }}

        .ev-box {{
            position: absolute;
            z-index: 5;
            cursor: pointer;
            transition: filter 0.15s ease, transform 0.12s ease;
        }}

        .ev-box:hover {{
            filter: brightness(1.18);
            transform: scale(1.03);
        }}

        .ev-box img {{
            width: 100%;
            height: 100%;
            object-fit: contain;
            padding: 8%;
            box-sizing: border-box;
            pointer-events: none;
            user-select: none;
        }}

        {back_btn_css}
        </style>
    </head>
    <body>
        <div class="ev-page">
            {back_btn_html}
            <div class="ev-stage">
                <img class="ev-bg" src="data:image/png;base64,{bg_b64}" alt="Evidence display">
                {boxes_html}
            </div>
        </div>
        {_navigate_js()}
    </body>
    </html>
    """

    components.html(html, height=1, scrolling=False)


def _render_zoom(
    back_btn_html: str,
    back_btn_css: str,
    current_index: int,
    num_evidence: int,
) -> None:
    bg_path = ASSETS_DIR / "Evidens zoom.png"
    if not bg_path.exists():
        st.error(f"Zoom-baggrund ikke fundet: {bg_path}")
        st.stop()

    bg_b64 = image_to_base64(bg_path)
    aspect_ratio = get_aspect_ratio(bg_path)

    item = EVIDENCE[current_index]
    img_path = ASSETS_DIR / item["image_filename"]
    evidence_img_html = ""
    if img_path.exists():
        ev_b64 = image_to_base64(img_path)
        evidence_img_html = f"""
        <img
            class="ev-zoom-img"
            src="data:image/png;base64,{ev_b64}"
            alt="{item['name']}"
        >
        """

    left_arrow = make_screen_arrow_button(
        direction="left",
        onclick="navigate('prev')",
        css_class="ev-arrow-left",
        aria_label="Forrige bevis",
    )
    right_arrow = make_screen_arrow_button(
        direction="right",
        onclick="navigate('next')",
        css_class="ev-arrow-right",
        aria_label="Næste bevis",
    )

    counter_text = f"{current_index + 1} / {num_evidence}"
    description = item.get("description", "")

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
        html, body {{
            margin: 0; padding: 0;
            width: 100vw; height: 100vh;
            overflow: hidden;
            background: #3a1f0f;
        }}

        .ev-zoom-page {{
            width: 100vw; height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #3a1f0f;
        }}

        .ev-zoom-stage {{
            position: relative;
            width: min(100vw, calc(100vh * {aspect_ratio}));
            aspect-ratio: {aspect_ratio};
        }}

        .ev-zoom-bg {{
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            object-fit: contain;
            z-index: 1;
            pointer-events: none;
            user-select: none;
        }}

        /* Bevisgenstand centreret på parchment */
        .ev-zoom-img {{
            position: absolute;
            left: 18%;
            top: 6%;
            width: 64%;
            height: 78%;
            object-fit: contain;
            z-index: 5;
            pointer-events: none;
            user-select: none;
        }}

        .ev-zoom-name {{
            position: absolute;
            left: 50%;
            bottom: 11%;
            transform: translateX(-50%);
            z-index: 10;
            font-family: Georgia, serif;
            font-size: clamp(13px, 1.3vw, 24px);
            color: #2a1a0a;
            font-weight: bold;
            white-space: nowrap;
        }}

        .ev-zoom-desc {{
            position: absolute;
            left: 50%;
            bottom: 6.5%;
            transform: translateX(-50%);
            z-index: 10;
            font-family: Georgia, serif;
            font-size: clamp(10px, 0.9vw, 16px);
            color: #3a2a18;
            white-space: nowrap;
            font-style: italic;
        }}

        /* Tilbage til oversigt */
        .ev-back-overview {{
            position: absolute;
            right: 2%;
            top: 2.5%;
            z-index: 20;
            cursor: pointer;
            font-family: Georgia, serif;
            font-size: clamp(11px, 1vw, 17px);
            color: #4a2c0a;
            background: rgba(244, 223, 150, 0.85);
            border: 2px solid #8B5E3C;
            border-radius: 8px;
            padding: 0.3em 0.8em;
            transition: filter 0.15s ease;
            user-select: none;
        }}

        .ev-back-overview:hover {{
            filter: brightness(1.1);
        }}

        .ev-counter {{
            position: absolute;
            left: 50%;
            bottom: 2%;
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

        {back_btn_css}

        {screen_arrow_css()}

        .ev-arrow-left {{
            left: 1.0%;
            top: 35%;
            width: 8%;
            height: 28%;
        }}

        .ev-arrow-right {{
            right: 1.0%;
            top: 35%;
            width: 8%;
            height: 28%;
        }}
        </style>
    </head>
    <body>
        <div class="ev-zoom-page">
            {back_btn_html}
            <div class="ev-zoom-stage">

                <img class="ev-zoom-bg" src="data:image/png;base64,{bg_b64}" alt="Evidence zoom">

                {evidence_img_html}

                <div class="ev-zoom-name">{item['name']}</div>
                <div class="ev-zoom-desc">{description}</div>

                <div
                    class="ev-back-overview"
                    onclick="navigate('ev_overview')"
                    role="button"
                    aria-label="Tilbage til oversigt">
                    ← Oversigt
                </div>

                {left_arrow}
                {right_arrow}

                <div class="ev-counter">{counter_text}</div>

            </div>
        </div>
        {_navigate_js()}
    </body>
    </html>
    """

    components.html(html, height=1, scrolling=False)


def show_evidence() -> None:
    if "evidence_mode" not in st.session_state:
        st.session_state.evidence_mode = "overview"
    if "evidence_index" not in st.session_state:
        st.session_state.evidence_index = 0

    num_evidence = len(EVIDENCE)
    current_index = (
        st.session_state.evidence_index % num_evidence
        if num_evidence > 0
        else 0
    )
    st.session_state.evidence_index = current_index
    mode = st.session_state.evidence_mode

    back_btn_html = get_back_button_html(btn_key="ev_back")
    back_btn_css = get_back_button_css(left="1.2%", top="2.0%", width="13%")

    st.markdown(_streamlit_chrome_css(), unsafe_allow_html=True)

    if mode == "overview":
        _render_overview(back_btn_html, back_btn_css)
    else:
        _render_zoom(back_btn_html, back_btn_css, current_index, num_evidence)

    # --- Skjulte Streamlit-navigationknapper ---

    render_back_button_streamlit(btn_key="ev_back", target_page="main_menu")

    if st.button("ev_overview", key="ev_hidden_overview"):
        st.session_state.evidence_mode = "overview"
        st.rerun()

    # Klik på boks i oversigten → zoom til det pågældende bevis
    ev_click_cols = st.columns(max(num_evidence, 1))
    for i, col in enumerate(ev_click_cols):
        if i < num_evidence:
            with col:
                if st.button(f"ev_click_{i}", key=f"ev_hidden_click_{i}"):
                    st.session_state.evidence_index = i
                    st.session_state.evidence_mode = "zoom"
                    st.rerun()

    # Pile-navigation i zoom-tilstand
    col_prev, col_next = st.columns(2)
    with col_prev:
        if st.button("prev", key="ev_prev"):
            if num_evidence > 0:
                st.session_state.evidence_index = (current_index - 1) % num_evidence
            st.rerun()
    with col_next:
        if st.button("next", key="ev_next"):
            if num_evidence > 0:
                st.session_state.evidence_index = (current_index + 1) % num_evidence
            st.rerun()


def show_evidens() -> None:
    show_evidence()
