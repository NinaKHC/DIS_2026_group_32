from __future__ import annotations

import base64
from pathlib import Path

from PIL import Image
import streamlit as st


def image_to_base64(image_path: Path) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


@st.cache_data
def cached_image_to_base64(image_path: Path) -> str:
    return image_to_base64(image_path)


def get_aspect_ratio(image_path: Path) -> float:
    with Image.open(image_path) as image:
        width, height = image.size
    return width / height


def streamlit_chrome_css(background: str = "#2a1a0a") -> str:
    return f"""
        <style>
        html, body, .stApp {{
            margin: 0 !important; padding: 0 !important;
            overflow: hidden !important; background: {background} !important;
        }}
        [data-testid="stHeader"] {{ background: rgba(0,0,0,0) !important; height: 0rem !important; }}
        [data-testid="stToolbar"], [data-testid="stDecoration"] {{ display: none !important; }}
        .block-container {{ padding: 0 !important; margin: 0 !important; max-width: 100% !important; height: 100vh !important; overflow: hidden !important; }}
        section.main, div[data-testid="stAppViewContainer"], div[data-testid="stVerticalBlock"] {{ overflow: hidden !important; }}
        iframe {{ width: 100vw !important; height: 100vh !important; display: block !important; border: none !important; }}
        .element-container:has(iframe) {{ width: 100vw !important; height: 100vh !important; overflow: hidden !important; }}
        </style>
    """


def robust_navigation_script(function_name: str = "navigate", argument_name: str = "page") -> str:
    return f"""
        <script>
        let __navigationPending = false;

        function {function_name}({argument_name}) {{
            if (__navigationPending) {{
                return;
            }}
            __navigationPending = true;

            let attempts = 0;
            const clickWhenReady = function() {{
                attempts += 1;
                var buttons = window.parent.document.querySelectorAll('button');
                for (var i = 0; i < buttons.length; i++) {{
                    if (buttons[i].innerText.trim() === {argument_name} && !buttons[i].disabled) {{
                        buttons[i].click();
                        return;
                    }}
                }}

                if (attempts < 20) {{
                    window.setTimeout(clickWhenReady, 75);
                }} else {{
                    __navigationPending = false;
                }}
            }};

            window.setTimeout(clickWhenReady, 120);
        }}
        </script>
    """


def navigate_script() -> str:
    return robust_navigation_script()
