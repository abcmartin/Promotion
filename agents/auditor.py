from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


def audit_chunks(*, chunks_json_path: Path) -> Dict[str, Any]:
    chunks: List[Dict[str, Any]] = json.loads(Path(chunks_json_path).read_text(encoding="utf-8"))
    issues: List[Dict[str, Any]] = []

    for c in chunks:
        content: str = c.get("content", "")
        checks = {
            "has_citation": _has_citation(content),
            "has_numbers": _has_numbers(content),
            "long_sentences": _count_long_sentences(content),
            "passive_voice_flags": _count_passive_voice_flags(content),
        }
        if not checks["has_citation"]:
            issues.append({"id": c["id"], "type": "citation_missing", "message": "Keine Quelle/Zitation erkannt."})
        if checks["long_sentences"] > 3:
            issues.append({"id": c["id"], "type": "style_long_sentences", "message": "Viele sehr lange Stze."})
        if checks["passive_voice_flags"] > 2:
            issues.append({"id": c["id"], "type": "style_passive", "message": "Vermutete Passivhufung."})

    return {"issues": issues, "summary": {"num_chunks": len(chunks), "num_issues": len(issues)}}


def _has_citation(text: str) -> bool:
    # sehr einfache Heuristik: eckige Klammern/Ziffern oder (Autor, Jahr)
    return any(tok in text for tok in ["]", ")"])


def _has_numbers(text: str) -> bool:
    return any(ch.isdigit() for ch in text)


def _count_long_sentences(text: str) -> int:
    sentences = [s.strip() for s in text.split(".") if s.strip()]
    return sum(1 for s in sentences if len(s) > 240)


def _count_passive_voice_flags(text: str) -> int:
    # Deutsch/Englisch grobe Marker
    flags = ["wird ", "wurden ", "wurde ", "is " "was ", "were ", "be "]
    return sum(text.count(f) for f in flags)

