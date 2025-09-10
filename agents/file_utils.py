from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List


def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def find_markdown_files(root_dir: Path) -> List[Path]:
    return sorted([p for p in root_dir.rglob("*.md") if p.is_file()])


def read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text_file(path: Path, content: str) -> None:
    ensure_directory(path.parent)
    path.write_text(content, encoding="utf-8")


def write_json_file(path: Path, data: object) -> None:
    ensure_directory(path.parent)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def iter_lines(text: str) -> Iterable[str]:
    for line in text.splitlines():
        yield line

