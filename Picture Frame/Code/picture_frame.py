"""
picture_frame.py
────────────────
Genanvendeligt billede-ramme-komponent.

Brug det samme som screen_arrows og back_to_main_menu:
    - get_picture_frame_css()  → CSS-streng til <style>-blokken i din iframe
    - get_picture_frame_html() → HTML-streng til at placere rammen i din iframe

Eksempel i en side:

    from picture_frame import get_picture_frame_css, get_picture_frame_html

    frame_css  = get_picture_frame_css(
        css_class="my-frame",
        left="17%", top="7.5%", width="31.5%", height="27.5%",
    )
    frame_html = get_picture_frame_html(
        photo_path=Path("Characters/Char_1.png"),
        css_class="my-frame",
        alt="Sofia Laurent",
    )

    # Indsæt frame_css i <style>-blokken og frame_html i <body>
"""

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
    """Cached version of _b64 to avoid re-encoding images on every render."""
    return _b64(path)


def get_picture_frame_css(
    css_class: str = "pf-frame",
    left:   str = "17%",
    top:    str = "7.5%",
    width:  str = "31.5%",
    height: str = "27.5%",
    photo_position: str = "50% 10%",
    photo_scale:    float = 1.6,
    photo_fit:      str = "cover",
) -> str:
    """
    Returnerer CSS til billede-rammen til brug INDE I en components.html() iframe.

    Parametre
    ---------
    css_class : str
        CSS-klassen der bruges til at positionere rammen.
    left, top, width, height : str
        Position og størrelse i procent (%) af den omsluttende stage-div.
    photo_position : str
        Forankringspunkt for billedet — "50% 0%" = toppen, "center" = midten.
        Kun relevant når photo_fit="cover".
        Standard: "50% 10%".
    photo_scale : float
        Zoom-faktor, fx 1.0 = ingen zoom, 1.6 = tæt på.
        Kun relevant når photo_fit="cover".
        Standard: 1.6.
    photo_fit : str
        "contain" — viser hele billedet uden beskæring (bedst til allerede beskårede zoom-billeder).
        "cover"   — fylder rammen og beskærer (brug photo_position/scale til at styre fokus).
        Standard: "cover".
    """
    return f"""
    .{css_class} {{
        position: absolute;
        left:   {left};
        top:    {top};
        width:  {width};
        height: {height};
        z-index: 8;
    }}

    /* Ramme-billedet (baggrunden) */
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

    /* Inderzone — clipper det der stikker uden for rammen ved zoom */
    .{css_class} .pf-photo-clip {{
        position: absolute;
        left:   3%;
        top:    9%;
        width:  94%;
        height: 83%;
        overflow: hidden;
        z-index: 2;
    }}

    /* Person-billedet */
    .{css_class} .pf-photo {{
        width:  100%;
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
    css_class:  str = "pf-frame",
    alt:        str = "",
) -> str:
    """
    Returnerer HTML til billede-rammen til brug INDE I en components.html() iframe.

    Parametre
    ---------
    photo_path : Path | None
        Sti til personfotoet der skal vises inde i rammen.
        Sæt til None for at vise en tom ramme.
    css_class : str
        CSS-klassen der bruges til at positionere rammen — skal matche css_class i get_picture_frame_css().
    alt : str
        Alt-tekst til tilgængelighed.
    """
    if not _FRAME_FILE.exists():
        return f'<!-- Picture_frame.png ikke fundet: {_FRAME_FILE} -->'

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
