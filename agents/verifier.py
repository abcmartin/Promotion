from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from .file_utils import find_markdown_files, read_text_file


def verify_manuscript(*, manuscript_dir: Path, targets_json: Optional[Path]) -> Dict[str, Any]:
    files = find_markdown_files(manuscript_dir)
    file_stats: List[Dict[str, Any]] = []

    targets = {}
    if targets_json and Path(targets_json).exists():
        targets = json.loads(Path(targets_json).read_text(encoding="utf-8"))

    total_words = 0
    for f in files:
        text = read_text_file(f)
        words = _word_count(text)
        citations = _approx_citation_count(text)
        total_words += words
        target = _match_target_for_file(f, targets)
        file_stats.append(
            {
                "path": str(f),
                "words": words,
                "citations": citations,
                "target_words": target,
                "within_target": (target is None) or (abs(words - target) <= int(0.2 * target)),
            }
        )

    return {"total_words": total_words, "files": file_stats}


def _word_count(text: str) -> int:
    return len([w for w in text.split() if w.strip()])


def _approx_citation_count(text: str) -> int:
    # grobe Nherung f APA/Nummernzitierweise
    return text.count(")") + text.count("]")


def _match_target_for_file(path: Path, targets: Dict[str, Any]) -> Optional[int]:
    name = path.name.lower()
    # einfache Heuristik: exakte oder teil-basierte Zuordnung
    for key, val in targets.items():
        if key.lower() in name:
            try:
                return int(val)
            except Exception:
                return None
    return None

