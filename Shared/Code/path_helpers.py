from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def code_dir(*parts: str) -> Path:
    return PROJECT_ROOT.joinpath(*parts, "Code")


def assets_dir(page_file: str) -> Path:
    return Path(page_file).resolve().parents[1] / "Assets"


def add_code_paths(*paths: Path) -> None:
    for path in paths:
        path_text = str(path)
        if path_text not in sys.path:
            sys.path.append(path_text)
