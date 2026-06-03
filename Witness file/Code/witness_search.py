import json
import sys
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


shared_code_dir = Path(__file__).resolve().parents[2] / "Shared" / "Code"
if str(shared_code_dir) not in sys.path:
    sys.path.append(str(shared_code_dir))

from path_helpers import PROJECT_ROOT, add_code_paths, assets_dir, code_dir
from ui_helpers import cached_image_to_base64, get_aspect_ratio, navigate_script, streamlit_chrome_css


witness_button_code_dir = code_dir("Witness shortcut")

add_code_paths(
    code_dir("Back to main menu"),
    code_dir("Picture Frame"),
    code_dir("Witness file"),
    code_dir("Database"),
)
if str(witness_button_code_dir) in sys.path:
    sys.path.remove(str(witness_button_code_dir))
sys.path.insert(0, str(witness_button_code_dir))
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
    get_witness_search_button_html,
    render_witness_file_button_streamlit,
    render_witness_overview_button_streamlit,
    render_witness_red_button_streamlit,
    render_witness_search_button_streamlit,
)
from witness_overview import get_current_game_persons, get_witness_statement


BACKGROUND_FILENAME = "Witnes Search.png"
CHARS_DIR = PROJECT_ROOT / "Characters"


def _photo_path(person_id: int | None) -> Path | None:
    if person_id is None:
        return None

    for filename in (f"Char_zoom_{person_id}.png", f"Char_{person_id}.png"):
        path = CHARS_DIR / filename
        if path.exists():
            return path
    return None


def _search_fields(person: dict) -> dict:
    return {
        "name": str(person.get("name", "")),
        "role": str(person.get("role", "")),
        "gender": str(person.get("gender", "")),
        "hair": str(person.get("hair", "")),
        "eyes": str(person.get("eyes", "")),
        "skin": str(person.get("skin", "")),
        "clothing": str(person.get("clothing", "")),
        "presence": f"{person.get('arrived', '')} - {person.get('left', '')}",
    }


def _person_payload(person: dict) -> dict:
    person_id = person.get("id")
    photo_path = _photo_path(person_id)
    photo_data_url = ""
    if photo_path:
        photo_data_url = f"data:image/png;base64,{cached_image_to_base64(photo_path)}"

    statement = get_witness_statement(person)
    search_fields = _search_fields(person)

    return {
        "id": person_id,
        "name": search_fields["name"],
        "role": search_fields["role"],
        "gender": search_fields["gender"],
        "hair": search_fields["hair"],
        "eyes": search_fields["eyes"],
        "skin": search_fields["skin"],
        "clothing": search_fields["clothing"],
        "presence": search_fields["presence"],
        "statement": statement,
        "searchFields": search_fields,
        "photo": photo_data_url,
    }


def show_witness_search() -> None:
    page_assets_dir = assets_dir(__file__)
    background_path = page_assets_dir / BACKGROUND_FILENAME
    if not background_path.exists():
        st.error(f"Background image not found: {background_path}")
        st.stop()

    bg_b64 = cached_image_to_base64(background_path)
    aspect = get_aspect_ratio(background_path)
    game_persons = get_current_game_persons()
    people = [_person_payload(person) for person in game_persons]
    people_json = json.dumps(people)
    initial_photo_path = _photo_path(game_persons[0].get("id")) if game_persons else None
    frame_css = get_picture_frame_css(
        left="20.5%",
        top="6.0%",
        width="21.0%",
        height="43.0%",
        photo_fit="contain",
    )
    frame_html = get_picture_frame_html(
        initial_photo_path,
        alt=game_persons[0].get("name", "") if game_persons else "",
    )

    back_btn_html = get_back_button_html(btn_key="ws_back")
    back_btn_css = get_back_button_css(left="1.2%", top="2.0%", width="13%")

    overview_tab_html = get_witness_overview_button_html(btn_key="ws_tab_overview")
    overview_tab_css = get_witness_overview_button_css(
        css_class="witness-overview-tab",
        left="84.6%",
        top="27.7%",
        selected=False,
    )
    file_tab_html = get_witness_file_button_html(btn_key="ws_tab_file")
    file_tab_css = get_witness_file_button_css(
        css_class="witness-file-tab",
        left="84.9%",
        top="46.8%",
        selected=False,
    )
    red_tab_html = get_witness_red_button_html(btn_key="ws_tab_suspects")
    red_tab_css = get_witness_red_button_css(
        css_class="witness-red-tab",
        left="84.7%",
        top="11.6%",
        selected=False,
    )
    search_tab_html = get_witness_search_button_html(btn_key="ws_tab_search")
    search_tab_css = get_witness_green_button_css(
        css_class="witness-green-tab",
        left="85.2%",
        top="65.8%",
        selected=False,
    )

    st.markdown(streamlit_chrome_css(background="#2a1a0a"), unsafe_allow_html=True)

    page_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
        html, body {{
            margin: 0;
            padding: 0;
            width: 100vw;
            height: 100vh;
            overflow: hidden;
            background: #2a1a0a;
        }}

        .ws-page {{
            width: 100vw;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #2a1a0a;
            overflow: hidden;
        }}

        .ws-stage {{
            position: relative;
            width: min(100vw, calc(100vh * {aspect}));
            aspect-ratio: {aspect};
            overflow: hidden;
        }}

        .ws-bg {{
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            object-fit: contain;
            z-index: 1;
            pointer-events: none;
            user-select: none;
        }}

        .ws-list {{
            position: absolute;
            left: 19.5%;
            top: 59.5%;
            width: 28.0%;
            height: 30.0%;
            z-index: 20;
            overflow-y: auto;
            padding-right: 0.4rem;
            box-sizing: border-box;
            scrollbar-width: thin;
            scrollbar-color: rgba(85, 45, 15, 0.45) transparent;
        }}

        .ws-person-row {{
            display: grid;
            grid-template-columns: 1fr 0.9fr;
            gap: 0.55rem;
            align-items: center;
            min-height: 1.8rem;
            border-bottom: 1px solid rgba(100, 65, 30, 0.32);
            cursor: pointer;
            font-family: Georgia, serif;
            color: #241509;
            padding: 0 0.25rem;
            box-sizing: border-box;
        }}

        .ws-person-row:hover,
        .ws-selected {{
            background: rgba(160, 105, 35, 0.22);
        }}

        .ws-person-row span {{
            font-size: clamp(8px, 0.78vw, 13px);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .ws-person-row em {{
            font-size: clamp(7px, 0.62vw, 10px);
            color: #5d3b17;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .ws-search-panel {{
            position: absolute;
            left: 51.0%;
            top: 15.5%;
            width: 27.0%;
            height: 18.5%;
            z-index: 25;
            font-family: Georgia, serif;
            color: #241509;
        }}

        .ws-search-title {{
            font-size: clamp(13px, 1.15vw, 21px);
            font-weight: 800;
            margin-bottom: 0.45rem;
        }}

        .ws-search-input {{
            display: block;
            width: 100%;
            min-height: 2.4rem;
            border-bottom: 2px solid rgba(75, 45, 20, 0.55);
            border-left: none;
            border-right: none;
            border-top: none;
            outline: none;
            background: rgba(255, 235, 195, 0.28);
            padding: 0 0.45rem;
            font-size: clamp(10px, 0.9vw, 16px);
            box-sizing: border-box;
            font-family: Georgia, serif;
            color: #241509;
        }}

        .ws-search-input::placeholder {{
            color: rgba(80, 50, 20, 0.72);
        }}

        .ws-search-hint {{
            margin-top: 0.35rem;
            font-size: clamp(7px, 0.62vw, 11px);
            color: #6b471e;
        }}

        .ws-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.28rem;
            margin-top: 0.45rem;
            max-height: 3.8rem;
            overflow-y: auto;
        }}

        .ws-tag {{
            display: inline-flex;
            align-items: center;
            gap: 0.28rem;
            max-width: 100%;
            padding: 0.18rem 0.42rem;
            border: 1px solid rgba(90, 60, 25, 0.45);
            border-radius: 999px;
            background: rgba(255, 235, 195, 0.5);
            color: #241509;
            font-size: clamp(7px, 0.62vw, 11px);
            font-weight: 700;
        }}

        .ws-tag button {{
            border: none;
            background: transparent;
            color: #8b2020;
            cursor: pointer;
            font-weight: 900;
            font-size: 1em;
            line-height: 1;
            padding: 0;
        }}

        .ws-regex-error {{
            margin-top: 0.35rem;
            color: #8b2020;
            font-weight: 700;
            font-size: clamp(7px, 0.65vw, 12px);
        }}

        .ws-details {{
            position: absolute;
            left: 50.8%;
            top: 36.0%;
            width: 29.0%;
            height: 47.5%;
            z-index: 20;
            overflow: hidden;
            font-family: Georgia, serif;
            color: #241509;
        }}

        .ws-detail-grid {{
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            column-gap: 0.55rem;
            margin-bottom: 0.45rem;
            border-bottom: 1px solid rgba(90, 60, 25, 0.35);
            padding-bottom: 0.25rem;
        }}

        .ws-detail-row {{
            margin-bottom: 0.42rem;
            border-bottom: 1px solid rgba(90, 60, 25, 0.35);
            padding-bottom: 0.25rem;
        }}

        .ws-detail-cell {{
            min-width: 0;
        }}

        .ws-detail-cell span,
        .ws-detail-row span {{
            display: block;
            font-family: Arial, sans-serif;
            font-size: clamp(7px, 0.58vw, 10px);
            font-weight: 800;
            text-transform: uppercase;
            color: #3a2410;
            margin-bottom: 0.1rem;
        }}

        .ws-detail-cell strong,
        .ws-detail-row strong {{
            display: block;
            font-size: clamp(8px, 0.74vw, 13px);
            line-height: 1.2;
            max-height: 3.8em;
            overflow: hidden;
            word-break: break-word;
        }}

        .ws-count {{
            position: absolute;
            left: 19.5%;
            top: 55.7%;
            z-index: 20;
            font-family: Georgia, serif;
            font-size: clamp(8px, 0.7vw, 12px);
            color: #5d3b17;
            font-weight: 700;
        }}

        .ws-no-results,
        .ws-empty {{
            font-family: Georgia, serif;
            color: #5d3b17;
            font-size: clamp(9px, 0.85vw, 14px);
            padding: 0.6rem;
        }}

        .ws-empty span {{
            display: block;
            font-size: 0.8em;
            margin-top: 0.3rem;
        }}

        {back_btn_css}
        {overview_tab_css}
        {file_tab_css}
        {red_tab_css}
        {search_tab_css}
        {frame_css}
        </style>
    </head>
    <body>
        <div class="ws-page">
            <div class="ws-stage">
                {back_btn_html}
                <img class="ws-bg" src="data:image/png;base64,{bg_b64}" alt="Witness search">
                {overview_tab_html}
                {file_tab_html}
                {red_tab_html}
                {search_tab_html}
                {frame_html}
                <div class="ws-search-panel">
                    <div class="ws-search-title">Person Search</div>
                    <input
                        id="ws-search-input"
                        class="ws-search-input"
                        type="text"
                        autocomplete="off"
                        spellcheck="false"
                        placeholder="brown eyes"
                    >
                    <div class="ws-search-hint">Press Enter to add a search tag.</div>
                    <div id="ws-tags" class="ws-tags"></div>
                    <div id="ws-regex-error" class="ws-regex-error"></div>
                </div>
                <div id="ws-count" class="ws-count"></div>
                <div id="ws-list" class="ws-list"></div>
                <div id="ws-details" class="ws-details"></div>
            </div>
        </div>
        {navigate_script()}
        <script>
        const PEOPLE = {people_json};
        let selectedId = PEOPLE.length ? PEOPLE[0].id : null;
        let searchTags = [];

        function escapeHtml(value) {{
            return String(value ?? "")
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#039;");
        }}

        function setSelected(personId) {{
            selectedId = personId;
            render();
        }}

        const FIELD_ALIASES = {{
            hair: "hair",
            hairs: "hair",
            eye: "eyes",
            eyes: "eyes",
            skin: "skin",
            gender: "gender",
            sex: "gender",
            clothes: "clothing",
            clothing: "clothing",
            outfit: "clothing",
            role: "role",
            occupation: "role",
            job: "role",
            name: "name",
            person: "name",
            presence: "presence",
            time: "presence",
        }};

        const GENDER_ALIASES = {{
            man: "male",
            male: "male",
            men: "male",
            boy: "male",
            woman: "female",
            female: "female",
            women: "female",
            girl: "female",
            nonbinary: "nonbinary",
            "non-binary": "nonbinary",
        }};

        const SEARCHABLE_FIELDS = [
            "name",
            "role",
            "gender",
            "hair",
            "eyes",
            "skin",
            "clothing",
            "presence",
        ];

        function normalizeText(value) {{
            return String(value ?? "").toLowerCase().replace(/[-_/]+/g, " ").replace(/\\s+/g, " ").trim();
        }}

        function splitSearchTerms(tag) {{
            const normalized = normalizeText(tag);
            if (!normalized) return {{ field: null, query: "" }};

            const words = normalized.split(" ");
            let field = null;
            const remaining = [];

            for (const word of words) {{
                if (!field && FIELD_ALIASES[word]) {{
                    field = FIELD_ALIASES[word];
                }} else {{
                    remaining.push(word);
                }}
            }}

            const query = remaining.join(" ").trim();
            if (!field && GENDER_ALIASES[normalized]) {{
                return {{ field: "gender", query: GENDER_ALIASES[normalized] }};
            }}
            if (field === "gender" && GENDER_ALIASES[query]) {{
                return {{ field, query: GENDER_ALIASES[query] }};
            }}

            return {{ field, query }};
        }}

        function regexMatches(pattern, value) {{
            return pattern.test(normalizeText(value));
        }}

        function fieldMatches(person, tag) {{
            const {{ field, query }} = splitSearchTerms(tag);
            const patternText = query || normalizeText(tag);
            const pattern = new RegExp(patternText, "i");
            const fields = person.searchFields || {{}};

            if (field) {{
                return regexMatches(pattern, fields[field] || "");
            }}

            return SEARCHABLE_FIELDS.some((fieldName) =>
                regexMatches(pattern, fields[fieldName] || "")
            );
        }}

        function filteredPeople() {{
            const errorEl = document.getElementById("ws-regex-error");
            errorEl.textContent = "";

            if (!searchTags.length) return PEOPLE;

            try {{
                return PEOPLE.filter((person) =>
                    searchTags.every((tag) => fieldMatches(person, tag))
                );
            }} catch (error) {{
                errorEl.textContent = "Invalid regex: " + error.message;
                return PEOPLE;
            }}
        }}

        function addTag() {{
            const input = document.getElementById("ws-search-input");
            const value = input.value.trim();
            const errorEl = document.getElementById("ws-regex-error");
            errorEl.textContent = "";

            if (!value) return;

            try {{
                new RegExp(value, "i");
            }} catch (error) {{
                errorEl.textContent = "Invalid regex: " + error.message;
                return;
            }}

            if (!searchTags.some((tag) => tag.toLowerCase() === value.toLowerCase())) {{
                searchTags.push(value);
            }}
            input.value = "";
            render();
        }}

        function removeTag(index) {{
            searchTags.splice(index, 1);
            render();
        }}

        function renderTags() {{
            const tagsEl = document.getElementById("ws-tags");
            if (!searchTags.length) {{
                tagsEl.innerHTML = "";
                return;
            }}

            tagsEl.innerHTML = searchTags.map((tag, index) => `
                <div class="ws-tag">
                    <span>${{escapeHtml(tag)}}</span>
                    <button type="button" onclick="removeTag(${{index}})" aria-label="Remove ${{escapeHtml(tag)}}">x</button>
                </div>
            `).join("");
        }}

        function renderList(matches) {{
            const listEl = document.getElementById("ws-list");
            if (!matches.length) {{
                listEl.innerHTML = '<div class="ws-no-results">No witnesses match the search.</div>';
                return;
            }}

            listEl.innerHTML = matches.map((person) => `
                <div class="ws-person-row ${{person.id === selectedId ? "ws-selected" : ""}}"
                     onclick="setSelected(${{person.id}})">
                    <span>${{escapeHtml(person.name)}}</span>
                    <em>${{escapeHtml(person.role)}}</em>
                </div>
            `).join("");
        }}

        function renderDetails(person) {{
            const detailsEl = document.getElementById("ws-details");
            if (!person) {{
                detailsEl.innerHTML = `
                    <div class="ws-empty">
                        <div>No witness selected</div>
                        <span>Use the list to select a witness.</span>
                    </div>
                `;
                return;
            }}

            const topRows = [
                [
                    ["Full Name", person.name],
                    ["Occupation", person.role],
                    ["Gender", person.gender],
                ],
                [
                    ["Hair", person.hair],
                    ["Eyes", person.eyes],
                    ["Skin", person.skin],
                ],
            ];
            const rows = [
                ["Clothing", person.clothing],
                ["Presence", person.presence],
                ["Statement", person.statement],
            ];

            const gridHtml = topRows.map((group) => `
                <div class="ws-detail-grid">
                    ${{group.map(([label, value]) => `
                        <div class="ws-detail-cell">
                            <span>${{escapeHtml(label)}}</span>
                            <strong>${{escapeHtml(value)}}</strong>
                        </div>
                    `).join("")}}
                </div>
            `).join("");

            const rowHtml = rows.map(([label, value]) => `
                <div class="ws-detail-row">
                    <span>${{escapeHtml(label)}}</span>
                    <strong>${{escapeHtml(value)}}</strong>
                </div>
            `).join("");

            detailsEl.innerHTML = gridHtml + rowHtml;
        }}

        function renderPhoto(person) {{
            const photo = document.querySelector(".pf-photo");
            if (!photo) return;
            if (person && person.photo) {{
                photo.src = person.photo;
                photo.alt = person.name || "Witness photo";
            }}
        }}

        function render() {{
            const matches = filteredPeople();
            if (matches.length && !matches.some((person) => person.id === selectedId)) {{
                selectedId = matches[0].id;
            }}

            const selected = matches.find((person) => person.id === selectedId) || null;
            document.getElementById("ws-count").textContent = `${{matches.length}} / ${{PEOPLE.length}} witnesses`;
            renderTags();
            renderList(matches);
            renderDetails(selected);
            renderPhoto(selected);
        }}

        document.getElementById("ws-search-input").addEventListener("keydown", (event) => {{
            if (event.key === "Enter") {{
                event.preventDefault();
                addTag();
            }}
        }});
        render();
        </script>
    </body>
    </html>
    """

    components.html(page_html, height=1, scrolling=False)

    render_back_button_streamlit(btn_key="ws_back", target_page="main_menu")
    render_witness_overview_button_streamlit(btn_key="ws_tab_overview", target_page="witnesses")
    render_witness_file_button_streamlit(btn_key="ws_tab_file", target_page="witness_file")
    render_witness_red_button_streamlit(btn_key="ws_tab_suspects", target_page="suspects")
    render_witness_search_button_streamlit(btn_key="ws_tab_search", target_page="witness_search")
