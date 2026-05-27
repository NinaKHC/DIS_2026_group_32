import base64
from pathlib import Path

import streamlit as st


SUPPORTED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


def image_to_base64(image_path: Path) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


def find_first_asset_image() -> Path:

    case_overview_folder = Path(__file__).resolve().parents[1]
    assets_folder = case_overview_folder / "Assets"

    if not assets_folder.exists():
        raise FileNotFoundError(f"Assets folder not found: {assets_folder}")

    image_files = sorted(
        file_path
        for file_path in assets_folder.iterdir()
        if file_path.is_file()
        and file_path.suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS
    )

    if not image_files:
        raise FileNotFoundError(
            f"No image file found in {assets_folder}. "
            "Add a .png, .jpg, .jpeg, or .webp file."
        )

    return image_files[0]


def set_case_overview_background(image_path: Path) -> None:
    encoded_image = image_to_base64(image_path)

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_image}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-color: #1c0f08;
        }}

        [data-testid="stHeader"] {{
            background: rgba(0, 0, 0, 0);
        }}

        [data-testid="stToolbar"] {{
            display: none;
        }}

        .block-container {{
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 0rem;
            padding-right: 0rem;
            max-width: 100%;
        }}

        .back-link {{
            position: fixed;
            left: 2vw;
            top: 3vh;
            z-index: 9999;
            padding: 12px 22px;
            background: rgba(25, 15, 8, 0.82);
            color: #f5d28a !important;
            border: 2px solid rgba(217, 164, 65, 0.9);
            border-radius: 12px;
            text-decoration: none !important;
            font-size: 20px;
            font-weight: 800;
            font-family: Arial, Helvetica, sans-serif;
            box-shadow: 0px 0px 14px rgba(0, 0, 0, 0.65);
        }}

        .back-link:hover {{
            background: rgba(80, 55, 28, 0.95);
            color: #ffd27a !important;
            border-color: #ffd27a;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def handle_case_overview_navigation() -> None:
    page_from_url = st.query_params.get("page")

    if page_from_url == "main_menu":
        st.session_state["page"] = "main_menu"
        st.query_params.clear()
        st.rerun()


def show_case_overview() -> None:
    background_path = find_first_asset_image()

    set_case_overview_background(background_path)
    handle_case_overview_navigation()

    st.markdown(
        """
        <a class="back-link" href="?page=main_menu">← Back to Main Menu</a>
        """,
        unsafe_allow_html=True,
    )


# Backwards compatibility:
# If app.py still calls the old function name, this keeps it working.
def show_case_overview_detail() -> None:
    show_case_overview()
