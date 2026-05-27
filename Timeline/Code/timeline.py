import base64
import sys
from pathlib import Path

from PIL import Image
import streamlit as st
import streamlit.components.v1 as components


project_root = Path(__file__).resolve().parents[2]
back_button_code_dir = project_root / "Back to main menu" / "Code"

if str(back_button_code_dir) not in sys.path:
    sys.path.append(str(back_button_code_dir))

from back_to_main_menu import get_back_button_css, get_back_button_html, render_back_button_streamlit


ASSETS_DIR = Path(__file__).resolve().parents[1] / "Assets"

# ── Tidslinje-konfiguration ───────────────────────────────────────────────────
# Tilpas x_start/x_end/y så linjens endepunkter matcher billedet (i procent).
TIMELINE = {
    "x_start":      10.2,    # % fra venstre — linjens venstre endepunkt
    "x_end":        92.8,    # % fra venstre — linjens højre endepunkt
    "y":            46.5,    # % fra toppen  — linjens højde i billedet
    "time_start":   "06:00", # Tidspunkt ved linjens venstre kant
    "time_end":     "24:00", # Tidspunkt ved linjens højre kant
    "time_of_crime": "",     # Udfyld med fx "14:30" — vises over den røde pin i billedet
    # Positionen for crime-pin-labelen i billedet (venstre kant af "__" feltet)
    "crime_label_x": 56.0,   # %
    "crime_label_y": 52.8,   # %
}

# ── Begivenheder ─────────────────────────────────────────────────────────────
# type: "arrival" (grøn) | "departure" (orange) | "event" (blå)
# Populér fra SQL ved at bygge denne liste dynamisk.
#
# Eksempel:
#   {"name": "Viktor Hargreaves", "time": "12:15", "type": "arrival"},
#   {"name": "Viktor Hargreaves", "time": "13:45", "type": "departure"},
#   {"name": "Elena Marsh",       "time": "11:00", "type": "arrival"},
TIMELINE_EVENTS: list[dict] = [
    # Indsæt begivenheder her, fx fra SQL
]
# ─────────────────────────────────────────────────────────────────────────────

TYPE_COLORS = {
    "arrival":   "#2d8a4e",
    "departure": "#c85000",
    "event":     "#225599",
}
TYPE_LABELS_DA = {
    "arrival":   "Ankomst",
    "departure": "Afgang",
    "event":     "Hændelse",
}


def image_to_base64(image_path: Path) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def get_aspect_ratio(image_path: Path) -> float:
    with Image.open(image_path) as img:
        w, h = img.size
    return w / h


def _time_to_minutes(t: str) -> int:
    h, m = map(int, t.split(":"))
    return h * 60 + m


def _time_to_x(time_str: str) -> float:
    """Konverterer et tidspunkt til en x-position (%) på tidslinjen."""
    t   = _time_to_minutes(time_str)
    t0  = _time_to_minutes(TIMELINE["time_start"])
    t1  = _time_to_minutes(TIMELINE["time_end"])
    frac = max(0.0, min(1.0, (t - t0) / (t1 - t0)))
    return TIMELINE["x_start"] + frac * (TIMELINE["x_end"] - TIMELINE["x_start"])


def _build_events_html(events: list[dict]) -> str:
    if not events:
        return ""

    sorted_events = sorted(events, key=lambda e: _time_to_minutes(e.get("time", "00:00")))
    y_line = TIMELINE["y"]
    html = ""

    for i, ev in enumerate(sorted_events):
        time_str  = ev.get("time", "")
        name      = ev.get("name", "")
        ev_type   = ev.get("type", "event")
        color     = TYPE_COLORS.get(ev_type, "#225599")
        type_label = TYPE_LABELS_DA.get(ev_type, ev_type.capitalize())

        if not time_str:
            continue

        x = _time_to_x(time_str)

        # Alternér labels over/under linjen for at undgå overlap
        above = (i % 2 == 0)
        label_class = "tl-label-above" if above else "tl-label-below"

        html += f"""
        <div class="tl-event" style="left:{x}%;top:{y_line}%;--ev-color:{color};">
            <div class="tl-dot"></div>
            <div class="{label_class}">
                <span class="tl-time">{time_str}</span>
                <span class="tl-name">{name}</span>
                <span class="tl-type">{type_label}</span>
            </div>
        </div>
        """

    return html


def _crime_time_overlay() -> str:
    """Overlay der fylder '__' feltet på den røde pin-label ud med crime time."""
    crime_time = TIMELINE.get("time_of_crime", "")
    if not crime_time:
        return ""
    x = TIMELINE["crime_label_x"]
    y = TIMELINE["crime_label_y"]
    return f"""
    <div style="
        position: absolute;
        left: {x}%;
        top:  {y}%;
        z-index: 20;
        font-family: Georgia, serif;
        font-size: clamp(9px, 1.0vw, 16px);
        color: #f8ece0;
        font-weight: 600;
        pointer-events: none;
        user-select: none;
        white-space: nowrap;
    ">{crime_time}</div>
    """


def show_timeline() -> None:
    bg_path = ASSETS_DIR / "Time line map.png"
    if not bg_path.exists():
        st.error(f"Tidslinjebillede ikke fundet: {bg_path}")
        st.stop()

    bg_b64      = image_to_base64(bg_path)
    aspect_ratio = get_aspect_ratio(bg_path)

    back_btn_html = get_back_button_html(btn_key="tl_back")
    back_btn_css  = get_back_button_css(left="1.0%", top="1.5%", width="10%")

    events_html      = _build_events_html(TIMELINE_EVENTS)
    crime_time_html  = _crime_time_overlay()

    st.markdown(
        """
        <style>
        html, body, .stApp {
            margin: 0 !important; padding: 0 !important;
            overflow: hidden !important; background: #2a1a0a !important;
        }
        [data-testid="stHeader"] { background: rgba(0,0,0,0) !important; height: 0rem !important; }
        [data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }
        .block-container { padding: 0 !important; margin: 0 !important; max-width: 100% !important; height: 100vh !important; overflow: hidden !important; }
        section.main, div[data-testid="stAppViewContainer"], div[data-testid="stVerticalBlock"] { overflow: hidden !important; }
        iframe { width: 100vw !important; height: 100vh !important; display: block !important; border: none !important; }
        .element-container:has(iframe) { width: 100vw !important; height: 100vh !important; overflow: hidden !important; }
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
            margin: 0; padding: 0;
            width: 100vw; height: 100vh;
            overflow: hidden;
            background: #2a1a0a;
        }}

        .tl-page {{
            width: 100vw; height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #2a1a0a;
        }}

        .tl-stage {{
            position: relative;
            width: min(100vw, calc(100vh * {aspect_ratio}));
            aspect-ratio: {aspect_ratio};
        }}

        .tl-bg {{
            position: absolute;
            inset: 0; width: 100%; height: 100%;
            object-fit: contain;
            z-index: 1;
            pointer-events: none;
            user-select: none;
        }}

        /* ── Begivenhedsmarkør ─────────────────────────────── */
        .tl-event {{
            position: absolute;
            z-index: 10;
            transform: translate(-50%, -50%);
        }}

        .tl-dot {{
            width:  clamp(8px, 1.0vw, 14px);
            height: clamp(8px, 1.0vw, 14px);
            background: var(--ev-color);
            border: 2px solid #fff;
            border-radius: 50%;
            box-shadow: 0 0 5px rgba(0,0,0,0.5);
            position: relative;
            z-index: 11;
            transition: transform 0.15s ease;
        }}

        .tl-event:hover .tl-dot {{
            transform: scale(1.4);
        }}

        /* Label over linjen */
        .tl-label-above {{
            position: absolute;
            bottom: calc(100% + 4px);
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 1px;
            pointer-events: none;
        }}

        /* Label under linjen */
        .tl-label-below {{
            position: absolute;
            top: calc(100% + 4px);
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 1px;
            pointer-events: none;
        }}

        .tl-time {{
            display: block;
            font-family: Georgia, serif;
            font-size: clamp(8px, 0.8vw, 13px);
            font-weight: 700;
            color: var(--ev-color);
            white-space: nowrap;
            text-shadow: 0 1px 2px rgba(255,255,255,0.8);
        }}

        .tl-name {{
            display: block;
            font-family: Georgia, serif;
            font-size: clamp(8px, 0.75vw, 12px);
            font-weight: 600;
            color: #1a0e07;
            white-space: nowrap;
            text-shadow: 0 1px 2px rgba(255,255,255,0.8);
        }}

        .tl-type {{
            display: block;
            font-family: Georgia, serif;
            font-size: clamp(7px, 0.65vw, 10px);
            font-style: italic;
            color: #3a2a18;
            white-space: nowrap;
            text-shadow: 0 1px 2px rgba(255,255,255,0.8);
        }}

        {back_btn_css}
        </style>
    </head>
    <body>
        <div class="tl-page">
            {back_btn_html}
            <div class="tl-stage">
                <img class="tl-bg" src="data:image/png;base64,{bg_b64}" alt="Timeline">
                {crime_time_html}
                {events_html}
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

    render_back_button_streamlit(btn_key="tl_back", target_page="main_menu")
