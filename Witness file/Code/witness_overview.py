import base64
import sys
from pathlib import Path

from PIL import Image
import streamlit as st
import streamlit.components.v1 as components


project_root = Path(__file__).resolve().parents[2]
back_button_code_dir  = project_root / "Back to main menu" / "Code"
picture_frame_code_dir = project_root / "Picture Frame" / "Code"
witness_button_code_dir = project_root / "Witness shortcut" / "Code"
char_randomizer_code_dir = project_root / "Char Randomizer" / "Code"
suspect_selecter_code_dir = project_root / "Suspect selecter" / "Code"

if str(back_button_code_dir) not in sys.path:
    sys.path.append(str(back_button_code_dir))
if str(picture_frame_code_dir) not in sys.path:
    sys.path.append(str(picture_frame_code_dir))
if str(char_randomizer_code_dir) not in sys.path:
    sys.path.append(str(char_randomizer_code_dir))
if str(suspect_selecter_code_dir) not in sys.path:
    sys.path.append(str(suspect_selecter_code_dir))
if str(witness_button_code_dir) in sys.path:
    sys.path.remove(str(witness_button_code_dir))
sys.path.insert(0, str(witness_button_code_dir))

# Streamlit keeps imported modules alive between reruns. Force this helper to
# reload from the shared Witness shortcut folder after it was moved there.
sys.modules.pop("witness_button", None)

from back_to_main_menu import get_back_button_css, get_back_button_html, render_back_button_streamlit
from picture_frame import get_picture_frame_css, get_picture_frame_html
from witness_button import (
    get_witness_file_button_css,
    get_witness_file_button_html,
    get_witness_green_button_css,
    get_witness_overview_button_css,
    get_witness_overview_button_html,
    get_witness_red_button_css,
    get_witness_red_button_html,
    get_witness_static_button_html,
    render_witness_file_button_streamlit,
    render_witness_overview_button_streamlit,
    render_witness_red_button_streamlit,
)


try:
    from Random_char_selector import get_selected_characters
except ImportError:
    # Fallback so the page can still run before the randomizer file exists.
    def get_selected_characters() -> list[dict]:
        return []

try:
    from Is_Suspect import get_guilty_suspect
except ImportError:
    def get_guilty_suspect() -> dict | None:
        return None

ASSETS_DIR  = Path(__file__).resolve().parents[1] / "Assets"
CHARS_DIR   = project_root / "Characters"
BG_FILENAME = "Witness overview.png"

# ── Persondata ────────────────────────────────────────────────────────────────
# Når SQL-databasen kobles til, erstat PERSONS med en forespørgsel:
#
#   import psycopg2
#   conn = psycopg2.connect(DATABASE_URL)
#   cur  = conn.cursor()
#   cur.execute("""
#       SELECT p.person_id, p.name, p.role, p.gender,
#              p.hair_color, p.eye_color, p.skin_color, p.clothing,
#              TO_CHAR(pr.arrived_at,'HH24:MI') AS arrived,
#              TO_CHAR(pr.left_at,  'HH24:MI') AS left,
#              s.statement_text
#       FROM Person p
#       LEFT JOIN Presence  pr ON p.person_id = pr.person_id
#       LEFT JOIN Statement s  ON p.person_id = s.person_id
#       ORDER BY p.person_id
#   """)
#   PERSONS = [
#       {"id":r[0],"name":r[1],"role":r[2],"gender":r[3],
#        "hair":r[4],"eyes":r[5],"skin":r[6],"clothing":r[7],
#        "arrived":r[8],"left":r[9],"statement":r[10] or ""}
#       for r in cur.fetchall()
#   ]

PERSONS: list[dict] = [
    {"id":1,  "name":"Sofia Laurent",    "role":"Investigator",         "gender":"Female",    "hair":"Red",          "eyes":"Green",       "skin":"Medium brown", "arrived":"13:05","left":"18:00","clothing":"Blue blazer, white blouse, grey trousers, brown shoes, gold jewelry",                    "statement":"I arrived after the alarm, but one witness kept mentioning someone with red hair. That detail may matter."},
    {"id":2,  "name":"Maya Johnson",     "role":"Café employee",        "gender":"Female",    "hair":"Dark brown",   "eyes":"Brown",       "skin":"Dark brown",   "arrived":"07:30","left":"15:30","clothing":"Green shirt, brown t-shirt, black apron, brown pants, black sneakers",                    "statement":"During my coffee shift, I saw someone with medium-brown skin moving quickly near the jewelry store entrance."},
    {"id":3,  "name":"Alex Wren",        "role":"Bookstore employee",   "gender":"Nonbinary", "hair":"Black",        "eyes":"Dark brown",  "skin":"Fair",         "arrived":"09:15","left":"17:45","clothing":"Grey cardigan, yellow scarf, red trousers, glasses, brown shoes, staff lanyard",          "statement":"A customer asked strange questions about necklaces. I remember something about the outfit."},
    {"id":4,  "name":"Marcus Reed",      "role":"Bakery employee",      "gender":"Male",      "hair":"Black",        "eyes":"Brown",       "skin":"Light brown",  "arrived":"06:00","left":"14:00","clothing":"Striped shirt, brown apron, dark trousers, green beanie, brown boots",                    "statement":"I was carrying bread outside when I noticed someone with a distinctive hair color looking toward the jewelry window."},
    {"id":5,  "name":"Elena Bloom",      "role":"Florist employee",     "gender":"Female",    "hair":"Grey-brown",   "eyes":"Green",       "skin":"Olive",        "arrived":"08:00","left":"16:00","clothing":"White blouse, green apron, red skirt, brown boots",                                        "statement":"I was arranging flowers outside when someone passed by twice. They seemed nervous."},
    {"id":6,  "name":"Rafael Moreno",    "role":"Witness",              "gender":"Male",      "hair":"Dark brown",   "eyes":"Brown",       "skin":"Tan",          "arrived":"11:45","left":"12:20","clothing":"Red shirt, black t-shirt, brown pants, brown bag, sneakers",                               "statement":"I saw someone leave the area around 12:30. I mostly remember the outfit."},
    {"id":7,  "name":"Luna Hart",        "role":"Customer",             "gender":"Female",    "hair":"Blonde",       "eyes":"Blue",        "skin":"Fair",         "arrived":"12:05","left":"12:50","clothing":"Grey beanie, blue vest, white sweater, black skirt, sneakers",                             "statement":"I was near the display window when someone with distinctive hair brushed past me."},
    {"id":8,  "name":"Nia Carter",       "role":"Customer",             "gender":"Female",    "hair":"Dark brown",   "eyes":"Hazel",       "skin":"Dark brown",   "arrived":"12:10","left":"12:45","clothing":"Orange jacket, black top, blue jeans, black boots",                                        "statement":"I heard footsteps right before the alarm. When I turned around, I noticed the clothing."},
    {"id":9,  "name":"Rowan Vale",       "role":"Customer",             "gender":"Nonbinary", "hair":"Silver-grey",  "eyes":"Grey-green",  "skin":"Olive",        "arrived":"12:00","left":"12:40","clothing":"Grey shirt, black top, brown pants, black sneakers",                                        "statement":"Someone was standing unusually close to the side entrance. I thought it was odd."},
    {"id":10, "name":"Jamal Brooks",     "role":"Customer",             "gender":"Male",      "hair":"Black",        "eyes":"Brown",       "skin":"Medium brown", "arrived":"12:15","left":"13:05","clothing":"Green jacket, white sweater, black pants, green sneakers",                                  "statement":"I remember seeing someone near the store around the time of the theft."},
    {"id":11, "name":"Clara Finch",      "role":"Reporter",             "gender":"Female",    "hair":"Red",          "eyes":"Green",       "skin":"Fair",         "arrived":"13:20","left":"16:30","clothing":"Blue beanie, green sweater, white shirt, grey pants, bag, sneakers",                       "statement":"For my report, I wrote down one detail: distinctive hair color. It came up more than once."},
    {"id":12, "name":"Isabella Cruz",    "role":"Market employee",      "gender":"Female",    "hair":"Covered",      "eyes":"Brown",       "skin":"Dark brown",   "arrived":"08:30","left":"17:00","clothing":"Yellow jacket, blue jumpsuit, brown bag, gold earrings, white sneakers",                   "statement":"From my market stall, I saw someone staring at the police car before walking away."},
    {"id":13, "name":"Hiro Tanaka",      "role":"Watchmaker",           "gender":"Male",      "hair":"Silver-grey",  "eyes":"Brown",       "skin":"Tan",          "arrived":"09:00","left":"16:30","clothing":"Dark blue coat, white shirt, blue scarf, grey trousers, brown bag, brown boots",            "statement":"I repair watches, so I notice small details. The person I saw moved with purpose."},
    {"id":14, "name":"Priya Kapoor",     "role":"Art dealer",           "gender":"Female",    "hair":"Black-grey",   "eyes":"Brown",       "skin":"Medium brown", "arrived":"11:30","left":"12:55","clothing":"Green coat, yellow shirt, red scarf, red pants, brown boots, gold jewelry",               "statement":"I was looking at the displays when someone came very close to the VIP case."},
    {"id":15, "name":"Rex Voss",         "role":"Customer",             "gender":"Male",      "hair":"Platinum",     "eyes":"Brown",       "skin":"Fair",         "arrived":"12:20","left":"12:38","clothing":"Black leather jacket, red t-shirt, green jeans, chains, gloves, black boots",              "statement":"I did not see the face clearly, but I remember distinctive hair near the alley entrance."},
    {"id":16, "name":"Amara Rodriguez",  "role":"Jewelry employee",     "gender":"Female",    "hair":"Dark brown",   "eyes":"Amber-brown", "skin":"Medium brown", "arrived":"09:00","left":"17:30","clothing":"Blue dress, white cardigan, blue scarf, name tag, gold earrings, blue shoes",             "statement":"I was helping a customer when I noticed someone near the counter where the necklace was displayed."},
    {"id":17, "name":"Eleanor Whitmore", "role":"Sr. jewelry employee", "gender":"Female",    "hair":"Silver-grey",  "eyes":"Green",       "skin":"Fair",         "arrived":"08:45","left":"17:15","clothing":"White blouse, blue vest, blue long skirt, blue scarf, glasses, name tag, blue shoes",     "statement":"I have worked here for years. The person near the display did not behave like a normal customer."},
    {"id":18, "name":"Jordan Ellis",     "role":"Jewelry employee",     "gender":"Nonbinary", "hair":"Red",          "eyes":"Hazel",       "skin":"Olive",        "arrived":"09:30","left":"18:00","clothing":"Blue suit, white turtleneck, name tag, gold necklace, blue shoes",                         "statement":"Someone passed behind me just before the alarm. I saw distinctive hair reflected in the glass case."},
    {"id":19, "name":"James Thompson",   "role":"Jewelry employee",     "gender":"Male",      "hair":"Black",        "eyes":"Brown",       "skin":"Dark brown",   "arrived":"09:00","left":"17:00","clothing":"White shirt, blue vest, blue tie, blue trousers, name tag, brown shoes",                   "statement":"I greeted someone around 12:30, but they avoided eye contact."},
    {"id":20, "name":"Mei Sato",         "role":"Jewelry employee",     "gender":"Female",    "hair":"Dark brown",   "eyes":"Brown",       "skin":"Fair",         "arrived":"10:00","left":"18:30","clothing":"Blue blazer, white blouse, blue skirt, blue scarf, name tag, black shoes",                 "statement":"I was checking the front display when I noticed a person leaving in a hurry."},
    {"id":21, "name":"Valentina Moretti","role":"Customer",             "gender":"Female",    "hair":"Dark brown",   "eyes":"Hazel",       "skin":"Medium brown", "arrived":"12:05","left":"12:48","clothing":"Pink coat, blue blouse, white pants, gold earrings, bracelets, shoes",                     "statement":"I remember someone stylish near the entrance. The clearest thing was the clothing."},
    {"id":22, "name":"Arthur Kingsley",  "role":"Collector",            "gender":"Male",      "hair":"White",        "eyes":"Brown",       "skin":"Dark brown",   "arrived":"11:55","left":"13:10","clothing":"Blue blazer, white turtleneck, grey trousers, grey cap, glasses, cane, red shoes",        "statement":"Collectors notice details. I saw someone near the necklace case shortly before the alarm."},
    {"id":23, "name":"Yumi Nakamura",    "role":"Customer",             "gender":"Female",    "hair":"Black",        "eyes":"Brown",       "skin":"Fair",         "arrived":"12:25","left":"12:42","clothing":"Red jacket, white t-shirt, blue skirt, black socks, white sneakers, black bag",           "statement":"I was only there briefly, but I saw someone near the door."},
    {"id":24, "name":"Bruno Vargas",     "role":"Delivery driver",      "gender":"Male",      "hair":"Black",        "eyes":"Brown",       "skin":"Tan",          "arrived":"12:18","left":"12:34","clothing":"Orange vest, blue shirt, green pants, black watch, brown boots",                            "statement":"I had a delivery nearby. Someone crossed in front of me like they were in a rush."},
    {"id":25, "name":"Margaret Green",   "role":"Customer",             "gender":"Female",    "hair":"White",        "eyes":"Brown",       "skin":"Fair",         "arrived":"11:40","left":"12:15","clothing":"Purple cardigan, yellow blouse, green long skirt, pearl earrings, glasses, red shoes",    "statement":"Before I left, I noticed someone. I remember thinking their hair stood out."},
    {"id":26, "name":"Scarlett Hayes",   "role":"Customer",             "gender":"Female",    "hair":"Red",          "eyes":"Blue",        "skin":"Fair",         "arrived":"12:00","left":"12:33","clothing":"Blue blouse, black skirt, black tights, gold earrings, black shoes",                       "statement":"I remember someone near the entrance. The clearest thing was the outfit."},
    {"id":27, "name":"Nova Blake",       "role":"Customer",             "gender":"Nonbinary", "hair":"Silver-grey",  "eyes":"Green",       "skin":"Medium brown", "arrived":"12:12","left":"12:52","clothing":"Yellow shirt, black turtleneck, black trousers, black boots, watch, necklace",             "statement":"I wrote down what I saw: distinctive eyes, quick movements, a glance toward the display."},
    {"id":28, "name":"Adrian Wolfe",     "role":"Customer",             "gender":"Male",      "hair":"Brown",        "eyes":"Hazel",       "skin":"Olive",        "arrived":"11:50","left":"12:45","clothing":"Brown coat, black turtleneck, dark trousers, black belt, black shoes",                      "statement":"Someone passed me near the entrance. I cannot swear to the face, but I remember the hair."},
    {"id":29, "name":"Zara Monroe",      "role":"Customer",             "gender":"Female",    "hair":"Blonde",       "eyes":"Brown",       "skin":"Dark brown",   "arrived":"12:08","left":"12:58","clothing":"Red turtleneck, brown trousers, brown belt, gold necklace, brown boots",                   "statement":"I saw someone leave after the commotion. The detail I remember best is the skin tone."},
    {"id":30, "name":"Daniel Pierce",    "role":"Customer",             "gender":"Male",      "hair":"Brown",        "eyes":"Blue",        "skin":"Fair",         "arrived":"11:35","left":"12:25","clothing":"Green jacket, white shirt, blue jeans, brown belt, brown shoes",                            "statement":"Before the alarm, I noticed someone looking closely at the necklace display."},
]

STOLEN_ITEM = "the necklace"
CRIME_TIME = "12:30"

STATEMENT_TEMPLATES: dict[int, str] = {
    1: "I arrived after the alarm, but one witness kept mentioning someone with {{culprit_hair_color}} hair. That detail may matter.",
    2: "During my coffee shift, I saw someone with {{culprit_skin_color}} skin moving quickly near the jewelry store entrance.",
    3: "A customer in the bookshop asked strange questions about expensive necklaces. I remember something about {{culprit_clothing}}.",
    4: "I was carrying bread outside the bakery when I noticed someone with {{culprit_hair_color}} hair looking toward the jewelry window.",
    5: "I was arranging flowers outside when someone with {{culprit_eye_color}} eyes passed by twice. They seemed nervous.",
    6: "I saw someone leave the area around {{crime_time}}. I mostly remember the outfit: {{culprit_clothing}}.",
    7: "I was near the display window when someone with {{culprit_hair_color}} hair brushed past me.",
    8: "I heard footsteps right before the alarm. When I turned around, I noticed someone wearing {{culprit_clothing}}.",
    9: "Someone with {{culprit_skin_color}} skin was standing unusually close to the side entrance. I thought it was odd.",
    10: "I remember seeing a {{culprit_gender}} person near the store around the time of the theft.",
    11: "For my report, I wrote down one detail from a witness: {{culprit_hair_color}} hair. It came up more than once.",
    12: "From my market stall, I saw someone with {{culprit_eye_color}} eyes staring at the police car before walking away.",
    13: "I repair watches, so I notice small details. The person I saw had {{culprit_hair_color}} hair and moved with purpose.",
    14: "I was looking at the displays when someone wearing {{culprit_clothing}} came very close to the VIP case.",
    15: "I did not see the face clearly, but I remember {{culprit_hair_color}} hair near the alley entrance.",
    16: "I was helping a customer when I noticed someone with {{culprit_skin_color}} skin near the counter where {{stolen_item}} was displayed.",
    17: "I have worked here for years. The person near the display did not behave like a normal customer. I noticed {{culprit_clothing}}.",
    18: "Someone passed behind me just before the alarm. I remember seeing {{culprit_hair_color}} hair reflected in the glass case.",
    19: "I greeted someone around {{crime_time}}, but they avoided eye contact. Their eyes looked {{culprit_eye_color}}.",
    20: "I was checking the front display when I noticed a person with {{culprit_skin_color}} skin leaving in a hurry.",
    21: "I remember someone stylish near the entrance. The clearest thing was the clothing: {{culprit_clothing}}.",
    22: "Collectors notice details. I saw a {{culprit_gender}} person near the necklace case shortly before the alarm.",
    23: "I was only there briefly, but I saw someone with {{culprit_hair_color}} hair near the door.",
    24: "I had a delivery nearby. Someone with {{culprit_skin_color}} skin crossed in front of me carrying themselves like they were in a rush.",
    25: "I saw someone before I left. I remember thinking their {{culprit_hair_color}} hair stood out.",
    26: "I noticed a person near the side of the room. The outfit looked like {{culprit_clothing}}.",
    27: "I wrote down what I saw: {{culprit_eye_color}} eyes, quick movements, and a glance toward the display case.",
    28: "Someone passed me near the entrance. I cannot swear to the face, but the person had {{culprit_hair_color}} hair.",
    29: "I saw someone leave after the commotion. The detail I remember best is {{culprit_skin_color}} skin and {{culprit_clothing}}.",
    30: "Before the alarm, I noticed someone with {{culprit_eye_color}} eyes looking closely at {{stolen_item}}.",
}

# ── Layout-positioner (% af billedet) ────────────────────────────────────────
# Juster disse hvis tekst/foto ikke lander korrekt på billedet.
LAYOUT = {
    # Foto-ramme — større nu da listen er rykket ned (4 rækker fjernet)
    "photo_left": 11.0, "photo_top": 4.5, "photo_w": 42.0, "photo_h": 46.0,
    # Statement
    "stmt_left": 56.0, "stmt_top": 15.9, "stmt_w": 21.5, "stmt_h": 20.0,
    # Personliste — rykket 15 % ned (4 fjernede rækker × ~3.8 vh ≈ 15 %)
    # bunden forbliver ca. samme sted som før
    "list_left": 19.5, "list_top": 52.5, "list_w": 27.5, "list_h": 34.0,
    # 6 attributrækker
    "attr_x": 57.0,
    "attr_ys":  [45.7, 53.15, 60.6, 68.05, 75.5, 82.95],
    "attr_row_h": 5.7,
}
# ─────────────────────────────────────────────────────────────────────────────


def _b64(path: Path) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def _aspect(path: Path) -> float:
    with Image.open(path) as img:
        w, h = img.size
    return w / h


def _get_current_game_persons() -> list[dict]:
    """
    Returns the 10 characters selected for the current game.

    If the game has not been started yet, we fall back to all PERSONS.
    This makes the page still work while testing directly.
    """
    selected_characters = get_selected_characters()
    if selected_characters:
        return selected_characters
    return PERSONS


def _person_by_id(pid: int, persons: list[dict] | None = None) -> dict | None:
    persons = persons if persons is not None else _get_current_game_persons()
    return next((p for p in persons if p["id"] == pid), None)


def _display_value(value: object) -> str:
    return str(value or "").strip()


def _statement_for_person(person: dict | None) -> str:
    if person is None:
        return ""

    guilty = get_guilty_suspect()
    if not guilty:
        guilty = next(
            (candidate for candidate in get_selected_characters() if candidate.get("is_suspect")),
            None,
        )
    template = STATEMENT_TEMPLATES.get(person.get("id"))
    if not guilty or not template:
        return person.get("statement", "")

    replacements = {
        "{{culprit_hair_color}}": _display_value(guilty.get("hair")).lower(),
        "{{culprit_eye_color}}": _display_value(guilty.get("eyes")).lower(),
        "{{culprit_skin_color}}": _display_value(guilty.get("skin")).lower(),
        "{{culprit_clothing}}": _display_value(guilty.get("clothing")).lower(),
        "{{culprit_gender}}": _display_value(guilty.get("gender")).lower(),
        "{{crime_time}}": CRIME_TIME,
        "{{stolen_item}}": STOLEN_ITEM,
    }

    statement = template
    for placeholder, value in replacements.items():
        statement = statement.replace(placeholder, value)
    return statement


def get_witness_statement(person: dict | None) -> str:
    return _statement_for_person(person)


def _build_list_html(selected_id: int, suspicious_ids: set, persons: list[dict]) -> str:
    rows = ""
    for p in persons:
        sel_cls  = "wo-selected"   if p["id"] == selected_id  else ""
        susp_cls = "wo-suspicious" if p["id"] in suspicious_ids else ""
        check    = "✓"             if p["id"] in suspicious_ids else ""
        rows += (
            f'<div class="wo-row {sel_cls} {susp_cls}" '
            f'onclick="selectPerson({p["id"]})">'
            f'<span class="wo-name">{p["name"]}</span>'
            f'<span class="wo-role">{p["role"]}</span>'
            f'<span class="wo-check" onclick="event.stopPropagation();toggleSusp({p["id"]})">{check}</span>'
            f'</div>'
        )
    return rows



def _build_statement_html(person: dict | None) -> str:
    if person is None:
        return ""
    stmt = _statement_for_person(person).replace("<", "&lt;").replace(">", "&gt;")
    l = LAYOUT
    return (
        f'<div style="position:absolute;left:{l["stmt_left"]}%;top:{l["stmt_top"]}%;'
        f'width:{l["stmt_w"]}%;height:{l["stmt_h"]}%;z-index:8;overflow:hidden;'
        f'font-family:Georgia,serif;font-size:clamp(7px,0.72vw,11px);'
        f'color:#2a1a0a;'
        # line-height i vh så teksten følger de trykte linjer i notekortet.
        # Linjerne er ca. 3 % af viewport-højden fra hinanden på det skalerede billede.
        f'line-height:2.6vh;word-break:break-word;'
        f'transform:rotate(-0.5deg);transform-origin:left top;'
        f'white-space:pre-wrap;">{stmt}</div>'
    )


def _build_attrs_html(person: dict | None) -> str:
    if person is None:
        return ""
    attrs = [
        "2026-05-12",
        "Maison Aurora Jewelry",
        f"{person.get('arrived','–')} – {person.get('left','–')}",
        person.get("role", ""),
        f"{person.get('hair','')} hair · {person.get('eyes','')} eyes · {person.get('skin','')} skin",
        person.get("clothing", ""),
    ]
    l = LAYOUT
    x    = l["attr_x"]
    rh   = l["attr_row_h"]
    html = ""
    for text, y in zip(attrs, l["attr_ys"]):
        safe = text.replace("<", "&lt;").replace(">", "&gt;")
        html += (
            f'<div style="position:absolute;left:{x}%;top:{y}%;'
            f'width:25%;max-height:{rh}%;z-index:8;pointer-events:none;overflow:hidden;'
            f'font-family:Georgia,serif;font-size:clamp(7px,0.68vw,10.5px);'
            f'color:#2a1a0a;font-weight:600;'
            f'line-height:1.18;word-break:break-word;white-space:normal;">'
            f'{safe}</div>'
        )
    return html


def show_witness_overview() -> None:
    bg_path = ASSETS_DIR / BG_FILENAME
    if not bg_path.exists():
        st.error(
            f"Baggrundsbillede ikke fundet: {bg_path}\n\n"
            f"Gem billedet som **{BG_FILENAME}** i mappen:\n`{ASSETS_DIR}`"
        )
        st.stop()

    bg_b64 = _b64(bg_path)
    aspect  = _aspect(bg_path)

    # ── Session state ─────────────────────────────────────────────────────────
    game_persons = _get_current_game_persons()
    game_person_ids = {p["id"] for p in game_persons}

    if "wo_selected" not in st.session_state:
        st.session_state.wo_selected = game_persons[0]["id"]

    if "wo_suspicious" not in st.session_state:
        st.session_state.wo_suspicious = set()

    # If selected person is not part of the current game, select the first of the 10.
    if st.session_state.wo_selected not in game_person_ids:
        st.session_state.wo_selected = game_persons[0]["id"]

    # Keep suspicious markings inside the current 10 characters.
    st.session_state.wo_suspicious = set(st.session_state.wo_suspicious) & game_person_ids

    selected_id    = st.session_state.wo_selected
    suspicious_ids = st.session_state.wo_suspicious
    person         = _person_by_id(selected_id, game_persons)

    # ── HTML byggeblokke ──────────────────────────────────────────────────────
    l = LAYOUT
    list_rows = _build_list_html(selected_id, suspicious_ids, game_persons)
    stmt_html = _build_statement_html(person)
    attrs_html = _build_attrs_html(person)

    # Billede-ramme via det fælles picture_frame-komponent
    # Brug zoom-billede hvis det findes, ellers fald tilbage til standard
    if person:
        zoom_path     = CHARS_DIR / f"Char_zoom_{person['id']}.png"
        standard_path = CHARS_DIR / f"Char_{person['id']}.png"
        char_path = zoom_path if zoom_path.exists() else standard_path
    else:
        char_path = None
    frame_css  = get_picture_frame_css(
        css_class="wo-frame",
        left=f"{l['photo_left']}%",
        top=f"{l['photo_top']}%",
        width=f"{l['photo_w']}%",
        height=f"{l['photo_h']}%",
        photo_fit="contain",   # Char_zoom-billeder er allerede beskåret — vis hele billedet
    )
    frame_html = get_picture_frame_html(
        photo_path=char_path if char_path and char_path.exists() else None,
        css_class="wo-frame",
        alt=person.get("name", "") if person else "",
    )

    back_btn_html = get_back_button_html(btn_key="wo_back")
    back_btn_css  = get_back_button_css(left="1.0%", top="1.0%", width="9%")
    witness_tab_html = get_witness_overview_button_html(btn_key="wo_tab_overview")
    witness_tab_css = get_witness_overview_button_css(
        css_class="witness-overview-tab",
        top="27.7%",
        selected=True,
    )
    witness_file_tab_html = get_witness_file_button_html(btn_key="wo_tab_file")
    witness_file_tab_css = get_witness_file_button_css(
        css_class="witness-file-tab",
        top="46.8%",
        selected=False,
    )
    witness_red_tab_html = get_witness_red_button_html(btn_key="wo_tab_suspects")
    witness_red_tab_css = get_witness_red_button_css(
        css_class="witness-red-tab",
        top="11.6%",
    )
    witness_green_tab_html = get_witness_static_button_html(
        css_class="witness-green-tab",
        label="Witness shortcut green",
    )
    witness_green_tab_css = get_witness_green_button_css(
        css_class="witness-green-tab",
        top="65.8%",
    )

    st.markdown(
        """
        <style>
        html,body,.stApp{margin:0!important;padding:0!important;overflow:hidden!important;background:#2a1a0a!important;}
        [data-testid="stHeader"]{background:rgba(0,0,0,0)!important;height:0rem!important;}
        [data-testid="stToolbar"],[data-testid="stDecoration"]{display:none!important;}
        .block-container{padding:0!important;margin:0!important;max-width:100%!important;height:100vh!important;overflow:hidden!important;}
        section.main,div[data-testid="stAppViewContainer"],div[data-testid="stVerticalBlock"]{overflow:hidden!important;}
        iframe{width:100vw!important;height:100vh!important;display:block!important;border:none!important;}
        .element-container:has(iframe){width:100vw!important;height:100vh!important;overflow:hidden!important;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    html = f"""
    <!DOCTYPE html><html><head>
    <style>
    html,body{{margin:0;padding:0;width:100vw;height:100vh;overflow:hidden;background:#2a1a0a;}}

    .wo-page{{width:100vw;height:100vh;display:flex;justify-content:center;align-items:center;background:#2a1a0a;overflow:hidden;}}

    .wo-stage{{
        position:relative;
        /* Hele siden altid synlig — evt. brune bjælker i siden er OK */
        width: min(100vw, calc(100vh * {aspect}));
        height: min(100vh, calc(100vw / {aspect}));
    }}

    .wo-bg{{position:absolute;inset:0;width:100%;height:100%;object-fit:fill;z-index:1;pointer-events:none;user-select:none;}}

    /* ── Personliste ─────────────────────────── */
    .wo-list{{
        position:absolute;
        left:{LAYOUT["list_left"]}%;top:{LAYOUT["list_top"]}%;
        width:{LAYOUT["list_w"]}%;height:{LAYOUT["list_h"]}%;
        z-index:10;
        overflow-y:auto;
        overflow-x:hidden;
        scrollbar-width:thin;
        scrollbar-color:rgba(100,60,20,0.3) transparent;
        /* Luft mellem checkbokser og scrollbar */
        padding-right:10px;
        box-sizing:border-box;
        /* Øverste tabel-linje */
        border-top: 1px solid rgba(110, 70, 25, 0.4);
    }}
    .wo-list::-webkit-scrollbar{{width:3px;}}
    .wo-list::-webkit-scrollbar-thumb{{background:rgba(100,60,20,0.35);border-radius:2px;}}

    .wo-row{{
        display:flex;align-items:center;
        padding:0 1%;
        cursor:pointer;
        height:3.8vh;
        /* Vandret tabel-linje under hver person */
        border-bottom: 1px solid rgba(110, 70, 25, 0.35);
        transition:background 0.12s ease;
        box-sizing:border-box;
    }}
    .wo-row:hover{{background:rgba(180,120,40,0.15);}}
    .wo-selected{{background:rgba(180,120,40,0.28)!important;}}
    .wo-suspicious .wo-name{{color:#8B2020;font-weight:700;}}

    .wo-name{{
        /* Navn-kolonnen — sæt fast bredde så rolle sidder tæt på */
        width:52%;
        flex-shrink:0;
        font-family:Georgia,serif;
        font-size:clamp(7px,0.76vw,12px);
        color:#2a1a0a;
        white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
    }}
    .wo-role{{
        /* Rolle — fylder resten af pladsen (tæt på navnet) */
        flex:1;
        font-family:Georgia,serif;
        font-size:clamp(6px,0.63vw,10px);
        color:#5a3a18;
        font-style:italic;
        white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
    }}
    .wo-check{{
        width:1.3em;height:1.3em;
        border:1.5px solid #8B5E3C;
        border-radius:3px;
        display:flex;align-items:center;justify-content:center;
        font-size:clamp(6px,0.7vw,11px);
        color:#8B2020;font-weight:bold;
        cursor:pointer;flex-shrink:0;
        background:rgba(255,245,220,0.6);
        transition:background 0.12s ease;
    }}
    .wo-check:hover{{background:rgba(255,200,100,0.5);}}

    {back_btn_css}

    {frame_css}

    {witness_tab_css}

    {witness_file_tab_css}

    {witness_red_tab_css}

    {witness_green_tab_css}
    </style></head>
    <body>
    <div class="wo-page">
        {back_btn_html}
        <div class="wo-stage">

            <img class="wo-bg" src="data:image/png;base64,{bg_b64}" alt="Witness overview">

            <!-- Billede-ramme (picture_frame komponent) -->
            {frame_html}

            <!-- Statement -->
            {stmt_html}

            <!-- Attributter -->
            {attrs_html}

            <!-- Shortcut fane: Witness Overview -->
            {witness_tab_html}

            <!-- Shortcut fane: Witness File -->
            {witness_file_tab_html}

            <!-- Passive shortcut faner: klar til fremtidige witness-sider -->
            {witness_red_tab_html}
            {witness_green_tab_html}

            <!-- Personliste -->
            <div class="wo-list">{list_rows}</div>

        </div>
    </div>

    <script>
    function navigate(page) {{
        var btns = window.parent.document.querySelectorAll('button');
        for (var i = 0; i < btns.length; i++) {{
            if (btns[i].innerText.trim() === page) {{ btns[i].click(); return; }}
        }}
    }}
    function selectPerson(id) {{ navigate('wo_sel_' + id); }}
    function toggleSusp(id)   {{ navigate('wo_tog_' + id); }}
    </script>
    </body></html>
    """

    components.html(html, height=1, scrolling=False)

    # ── Skjulte Streamlit-knapper ─────────────────────────────────────────────
    render_back_button_streamlit(btn_key="wo_back", target_page="main_menu")
    render_witness_overview_button_streamlit(btn_key="wo_tab_overview", target_page="witnesses")
    render_witness_file_button_streamlit(btn_key="wo_tab_file", target_page="witness_file")
    render_witness_red_button_streamlit(btn_key="wo_tab_suspects", target_page="suspects")

    sel_cols = st.columns(len(game_persons))
    for col, p in zip(sel_cols, game_persons):
        with col:
            if st.button(f"wo_sel_{p['id']}", key=f"wo_hidden_sel_{p['id']}"):
                st.session_state.wo_selected = p["id"]
                st.rerun()

    tog_cols = st.columns(len(game_persons))
    for col, p in zip(tog_cols, game_persons):
        with col:
            if st.button(f"wo_tog_{p['id']}", key=f"wo_hidden_tog_{p['id']}"):
                susp = set(st.session_state.wo_suspicious)
                if p["id"] in susp:
                    susp.discard(p["id"])
                else:
                    susp.add(p["id"])
                st.session_state.wo_suspicious = susp & game_person_ids
                st.rerun()
