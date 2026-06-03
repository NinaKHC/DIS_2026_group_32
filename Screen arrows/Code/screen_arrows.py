import base64
from pathlib import Path


def image_to_base64(image_path: Path) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


def get_arrow_image_base64(direction: str) -> str:
    direction = direction.lower().strip()

    assets_dir = Path(__file__).resolve().parents[1] / "Assets"
    image_paths = {
        "left": assets_dir / "Left_Arrow.png",
        "right": assets_dir / "Right_Arrow.png",
    }

    if direction not in image_paths:
        raise ValueError("direction must be 'left' or 'right'")

    image_path = image_paths[direction]
    if not image_path.exists():
        raise FileNotFoundError(f"Arrow image not found: {image_path}")

    return image_to_base64(image_path)


def screen_arrow_css() -> str:
    return """
    .screen-arrow-button {
        position: absolute;
        z-index: 50;
        display: block;
        border: none;
        outline: none;
        background: transparent;
        cursor: pointer;
        padding: 0;
        margin: 0;
        transition: transform 0.15s ease, filter 0.15s ease;
    }

    .screen-arrow-button:hover {
        transform: scale(1.06);
        filter: brightness(1.12);
    }

    .screen-arrow-button img {
        width: 100%;
        height: 100%;
        object-fit: contain;
        display: block;
        user-select: none;
        pointer-events: none;
    }
    """


def make_screen_arrow_button(
    direction: str,
    onclick: str,
    css_class: str,
    aria_label: str,
) -> str:
    encoded_image = get_arrow_image_base64(direction)

    return f"""
    <button
        class="screen-arrow-button {css_class}"
        onclick="{onclick}"
        aria-label="{aria_label}">
        <img
            src="data:image/png;base64,{encoded_image}"
            alt="{aria_label}">
    </button>
    """
