import base64
import json
import re
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


ASSETS_DIR = Path(__file__).resolve().parents[1] / "Assets"

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg", ".m4a"}
MUSIC_NAMES = {"music", "intro_music", "background_music", "soundtrack"}
VOICE_NAMES = {"voice", "voiceover", "narration", "intro_voice", "intro_voiceover"}
SECONDS_PER_IMAGE = 20
SCENE_DURATIONS = [26.5, 22, 18.5, 19, 15, 20, 25.5]
FADE_SECONDS = 1.6
INTRO_SCENES = [
    {
        "title": "Scene 1 - The Shop Before the Robbery",
        "text": (
            "In the middle of the city's busy center lies the exclusive jewelry store Maison Aurora.\n\n"
            "The store is known for its rare jewelry, private customers, and expensive collections. "
            "Behind the large glass windows, the display cases are filled with watches, rings, necklaces, and gemstones.\n\n"
            "Everything seems calm. But a few minutes later, everything changes."
        ),
    },
    {
        "title": "Scene 2 - The Robbery",
        "text": (
            "A masked person enters the store.\n\n"
            "While the staff stands back in shock, several display cases are emptied. "
            "One collection in particular is missing: the valuable Northern Lights Collection.\n\n"
            "The thief does not seem random. They know exactly where the jewelry is kept and which display cases to open."
        ),
    },
    {
        "title": "Scene 3 - The Escape",
        "text": (
            "The thief runs out onto the street with a bag full of jewelry.\n\n"
            "Witnesses only catch brief glimpses: dark clothing, quick movements, and a person disappearing between the buildings.\n\n"
            "No one manages to stop the escape. But the thief leaves behind clues."
        ),
    },
    {
        "title": "Scene 4 - The Police Arrive",
        "text": (
            "Shortly after, the area is cordoned off.\n\n"
            "Police cars are parked outside the store, and officers secure the crime scene. "
            "No one is allowed to leave the area before being questioned.\n\n"
            "Several people may have seen something. And perhaps one of them is more involved than they are willing to admit."
        ),
    },
    {
        "title": "Scene 5 - The Investigation Begins",
        "text": (
            "You play as the detective assigned to the case.\n\n"
            "Your task is to investigate the store, examine the clues, and find out who is behind the robbery.\n\n"
            "You should not guess at random. You need to use evidence."
        ),
    },
    {
        "title": "Scene 6 - Witnesses and Suspects",
        "text": (
            "Inside the store are employees, customers, and other people, each with their own explanation.\n\n"
            "Some are telling the truth. Others may remember things incorrectly. "
            "And at least one person may be trying to hide something.\n\n"
            "You must compare their statements with the evidence you find."
        ),
    },
    {
        "title": "Scene 7 - The Player's Task",
        "text": (
            "As the player, you must go through the case step by step.\n\n"
            "You must investigate the crime scene, see which jewelry has been stolen, read witness statements, "
            "check access logs, and compare the information.\n\n"
            "When you believe you have found the guilty person, you must make an arrest. But be careful.\n\n"
            "If you miss an important clue, the real thief may get away."
        ),
    },
]


def _file_to_data_uri(path: Path) -> str:
    mime_type = _mime_type(path)
    with open(path, "rb") as file:
        encoded = base64.b64encode(file.read()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def _mime_type(path: Path) -> str:
    extension = path.suffix.lower()
    if extension == ".png":
        return "image/png"
    if extension in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if extension == ".webp":
        return "image/webp"
    if extension == ".wav":
        return "audio/wav"
    if extension == ".ogg":
        return "audio/ogg"
    if extension == ".m4a":
        return "audio/mp4"
    return "audio/mpeg"


def _find_intro_images() -> list[Path]:
    if not ASSETS_DIR.exists():
        return []

    image_dirs = [ASSETS_DIR / "Images", ASSETS_DIR / "images", ASSETS_DIR]
    images: list[Path] = []

    for image_dir in image_dirs:
        if image_dir.exists():
            images.extend(
                file_path
                for file_path in image_dir.iterdir()
                if file_path.is_file() and file_path.suffix.lower() in IMAGE_EXTENSIONS
            )

    unique_images = set(images)
    numbered_intro_images = [
        image_path
        for image_path in unique_images
        if re.match(r"intro\s*\d+$", image_path.stem, re.IGNORECASE)
    ]
    images_to_show = numbered_intro_images or list(unique_images)

    def sort_key(path: Path) -> tuple[int, str]:
        number_match = re.search(r"\d+", path.stem)
        number = int(number_match.group()) if number_match else 9999
        return number, path.name.lower()

    return sorted(images_to_show, key=sort_key)


def _find_audio_file(allowed_names: set[str]) -> Path | None:
    if not ASSETS_DIR.exists():
        return None

    audio_dirs = [ASSETS_DIR / "Audio", ASSETS_DIR / "audio", ASSETS_DIR]
    for audio_dir in audio_dirs:
        if not audio_dir.exists():
            continue

        for file_path in sorted(audio_dir.iterdir(), key=lambda path: path.name.lower()):
            if file_path.is_file() and file_path.suffix.lower() in AUDIO_EXTENSIONS:
                if file_path.stem.lower() in allowed_names:
                    return file_path

    return None


def _streamlit_chrome_css() -> str:
    return """
        <style>
        html, body, .stApp {
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
            background: #080604 !important;
        }
        [data-testid="stHeader"] { background: rgba(0,0,0,0) !important; height: 0rem !important; }
        [data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }
        .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
            height: 100vh !important;
            overflow: hidden !important;
        }
        section.main,
        div[data-testid="stAppViewContainer"],
        div[data-testid="stVerticalBlock"] {
            overflow: hidden !important;
        }
        iframe {
            width: 100vw !important;
            height: 100vh !important;
            display: block !important;
            border: none !important;
        }
        .element-container:has(iframe) {
            width: 100vw !important;
            height: 100vh !important;
            overflow: hidden !important;
        }
        </style>
    """


def show_intro() -> None:
    image_sources = [_file_to_data_uri(path) for path in _find_intro_images()]
    music_file = _find_audio_file(MUSIC_NAMES)
    voice_file = _find_audio_file(VOICE_NAMES)
    music_source = _file_to_data_uri(music_file) if music_file else ""
    voice_source = _file_to_data_uri(voice_file) if voice_file else ""
    slides_json = json.dumps(image_sources)
    scenes_json = json.dumps(INTRO_SCENES)
    durations_json = json.dumps(SCENE_DURATIONS)
    music_audio_html = (
        f'<audio id="music" src="{music_source}" preload="auto" loop></audio>'
        if music_source
        else ""
    )
    voice_audio_html = (
        f'<audio id="voice" src="{voice_source}" preload="auto"></audio>'
        if voice_source
        else ""
    )

    st.markdown(_streamlit_chrome_css(), unsafe_allow_html=True)

    html = f"""
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
            background: #080604;
            font-family: Georgia, serif;
        }}

        .intro-page {{
            position: relative;
            width: 100vw;
            height: 100vh;
            background:
                radial-gradient(circle at 50% 35%, rgba(143, 91, 34, 0.22), transparent 44%),
                linear-gradient(180deg, #120b06 0%, #040302 100%);
            color: #f7e5b8;
        }}

        .slide {{
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            opacity: 0;
            transform: scale(1.035);
            transition: opacity {FADE_SECONDS}s ease-in-out, transform {SECONDS_PER_IMAGE + 2}s linear;
            z-index: 1;
        }}

        .slide.active {{
            opacity: 1;
            transform: scale(1);
        }}

        .empty-state {{
            position: absolute;
            inset: 0;
            z-index: 2;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 8vw;
            box-sizing: border-box;
            font-size: clamp(22px, 2.5vw, 44px);
            font-weight: 800;
            letter-spacing: 0.04em;
            text-shadow: 0 3px 10px rgba(0,0,0,0.7);
        }}

        .vignette {{
            position: absolute;
            inset: 0;
            z-index: 3;
            background:
                linear-gradient(90deg, rgba(0,0,0,0.62), transparent 24%, transparent 76%, rgba(0,0,0,0.62)),
                linear-gradient(180deg, rgba(0,0,0,0.45), transparent 28%, rgba(0,0,0,0.56));
            pointer-events: none;
        }}

        .caption {{
            position: absolute;
            left: 5.2%;
            bottom: 6.5%;
            z-index: 5;
            width: min(48vw, 780px);
            text-align: left;
            padding: clamp(14px, 1.35vw, 24px) clamp(18px, 1.6vw, 30px);
            box-sizing: border-box;
            border-left: 4px solid rgba(247, 229, 184, 0.82);
            background: linear-gradient(90deg, rgba(5, 3, 2, 0.72), rgba(5, 3, 2, 0.28));
            color: #f7e5b8;
            text-shadow: 0 3px 8px rgba(0,0,0,0.85);
            opacity: 1;
            transition: opacity {FADE_SECONDS}s ease-in-out;
        }}

        .caption.fading {{
            opacity: 0;
        }}

        .caption-title {{
            margin: 0 0 0.55rem 0;
            font-size: clamp(20px, 1.7vw, 34px);
            line-height: 1.05;
            font-weight: 900;
            letter-spacing: 0.03em;
        }}

        .caption-text {{
            margin: 0;
            font-size: clamp(13px, 0.95vw, 19px);
            line-height: 1.32;
            font-weight: 700;
            white-space: pre-line;
        }}

        .skip-button,
        .sound-button {{
            position: absolute;
            z-index: 8;
            border: 2px solid rgba(247, 229, 184, 0.75);
            background: rgba(15, 9, 4, 0.68);
            color: #f7e5b8;
            font-family: Georgia, serif;
            font-weight: 900;
            letter-spacing: 0.05em;
            cursor: pointer;
            box-shadow: 0 8px 22px rgba(0,0,0,0.35);
        }}

        .skip-button {{
            right: 2.2%;
            top: 2.5%;
            padding: 0.55rem 1rem;
            font-size: clamp(12px, 0.9vw, 17px);
        }}

        .sound-button {{
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            padding: 1rem 1.6rem;
            font-size: clamp(16px, 1.25vw, 24px);
            display: none;
        }}

        .sound-button.visible {{
            display: block;
        }}

        .progress {{
            position: absolute;
            left: 0;
            bottom: 0;
            z-index: 7;
            height: 0.45vh;
            width: 0%;
            background: linear-gradient(90deg, #c79642, #f7e5b8);
        }}
        </style>
    </head>
    <body>
        <div class="intro-page">
            <div id="slides"></div>
            <div id="empty-state" class="empty-state">INTRO ASSETS MANGLER</div>
            <div class="vignette"></div>
            <div class="caption" id="caption">
                <h2 class="caption-title" id="caption-title"></h2>
                <p class="caption-text" id="caption-text"></p>
            </div>
            <button class="skip-button" onclick="finishIntro()">SKIP</button>
            <button id="sound-button" class="sound-button" onclick="startIntro()">START INTRO</button>
            <div id="progress" class="progress"></div>
        </div>

        {music_audio_html}
        {voice_audio_html}

        <script>
        const slides = {slides_json};
        const scenes = {scenes_json};
        const sceneDurations = {durations_json};
        const secondsPerImage = {SECONDS_PER_IMAGE};
        const slideRoot = document.getElementById("slides");
        const emptyState = document.getElementById("empty-state");
        const soundButton = document.getElementById("sound-button");
        const progress = document.getElementById("progress");
        const caption = document.getElementById("caption");
        const captionTitle = document.getElementById("caption-title");
        const captionText = document.getElementById("caption-text");
        let currentSlide = 0;
        let slideTimer = null;
        let progressStart = Date.now();
        let slidesDone = false;
        let voiceDone = false;
        let introStarted = false;
        let navigationPending = false;

        function navigate(buttonText) {{
            if (navigationPending) return;
            navigationPending = true;

            let attempts = 0;
            const clickWhenReady = function() {{
                attempts += 1;
                const buttons = window.parent.document.querySelectorAll("button");
                for (let i = 0; i < buttons.length; i++) {{
                    if (buttons[i].innerText.trim() === buttonText && !buttons[i].disabled) {{
                        buttons[i].click();
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

        function finishIntro() {{
            navigate("intro_finish");
        }}

        function handleSkipKey(event) {{
            if (event.key === "Escape") {{
                finishIntro();
            }}
        }}

        document.addEventListener("keydown", handleSkipKey);
        try {{
            window.parent.document.addEventListener("keydown", handleSkipKey);
        }} catch (error) {{}}

        function tryFinishIntro() {{
            const voice = document.getElementById("voice");
            if (slidesDone && (!voice || voiceDone)) {{
                finishIntro();
            }}
        }}

        function renderSlides() {{
            if (!slides.length) {{
                emptyState.style.display = "flex";
                return;
            }}

            emptyState.style.display = "none";
            slides.forEach((src, index) => {{
                const img = document.createElement("img");
                img.className = "slide" + (index === 0 ? " active" : "");
                img.src = src;
                img.alt = "Intro image " + (index + 1);
                slideRoot.appendChild(img);
            }});
            updateCaption(0, false);
        }}

        function updateCaption(index, animate = true) {{
            const scene = scenes[index] || {{}};
            if (!scene.title && !scene.text) {{
                caption.style.display = "none";
                return;
            }}

            caption.style.display = "block";

            const setText = () => {{
                captionTitle.textContent = scene.title || "";
                captionText.textContent = scene.text || "";
                caption.classList.remove("fading");
            }};

            if (!animate) {{
                setText();
                return;
            }}

            caption.classList.add("fading");
            window.setTimeout(setText, {int(FADE_SECONDS * 500)});
        }}

        function showSlide(index) {{
            const images = document.querySelectorAll(".slide");
            images.forEach((img, imgIndex) => {{
                img.classList.toggle("active", imgIndex === index);
            }});
            updateCaption(index);
            progressStart = Date.now();
        }}

        function getCurrentSceneDuration() {{
            return sceneDurations[currentSlide] || secondsPerImage;
        }}

        function scheduleNextSlide() {{
            window.clearTimeout(slideTimer);
            slideTimer = window.setTimeout(advanceSlide, getCurrentSceneDuration() * 1000);
        }}

        function advanceSlide() {{
            if (!slides.length) {{
                slidesDone = true;
                window.clearTimeout(slideTimer);
                tryFinishIntro();
                return;
            }}

            if (currentSlide < slides.length - 1) {{
                currentSlide += 1;
                showSlide(currentSlide);
                scheduleNextSlide();
                return;
            }}

            slidesDone = true;
            window.clearTimeout(slideTimer);
            showSlide(currentSlide);
            tryFinishIntro();
        }}

        function animateProgress() {{
            const elapsed = (Date.now() - progressStart) / 1000;
            const percent = Math.min(100, (elapsed / getCurrentSceneDuration()) * 100);
            progress.style.width = percent + "%";
            requestAnimationFrame(animateProgress);
        }}

        function startTimeline() {{
            progressStart = Date.now();
            animateProgress();
            scheduleNextSlide();
        }}

        async function startAudio() {{
            const music = document.getElementById("music");
            const voice = document.getElementById("voice");
            const playTasks = [];

            if (music) {{
                music.volume = 0.35;
                playTasks.push(music.play());
            }}
            if (voice) {{
                voice.volume = 1.0;
                playTasks.push(voice.play());
            }}

            try {{
                await Promise.all(playTasks);
                soundButton.classList.remove("visible");
                return true;
            }} catch (error) {{
                soundButton.classList.add("visible");
                return false;
            }}
        }}

        async function startIntro() {{
            if (introStarted) {{
                return;
            }}

            const audioStarted = await startAudio();
            if (!audioStarted) {{
                return;
            }}

            introStarted = true;
            startTimeline();
        }}

        renderSlides();
        startIntro();

        const voice = document.getElementById("voice");
        if (voice) {{
            voice.addEventListener("ended", () => {{
                voiceDone = true;
                tryFinishIntro();
            }});
        }}
        </script>
    </body>
    </html>
    """

    components.html(html, height=1, scrolling=False)

    if st.button("intro_finish", key="intro_finish_hidden"):
        st.session_state["intro_seen"] = True
        st.session_state["page"] = "main_menu"
        st.rerun()
