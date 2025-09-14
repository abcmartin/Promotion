import os
import json
from typing import Tuple, Dict, Any

from .file_utils import read_text


def _resolve_section_path(section_id: str) -> str:
    # Mappe z. B. 5_material_methods → manuscript/5_material_methods.md
    base = os.path.join("manuscript", f"{section_id}.md")
    if os.path.exists(base):
        return base
    # Fallback: placeholder.md
    placeholder = os.path.join("manuscript", "placeholder.md")
    return placeholder if os.path.exists(placeholder) else base


def run_executor(section_id: str, planner_output_path: str, auditor_report_path: str) -> Tuple[str, Dict[str, Any], Dict[str, Any]]:
    """
    Minimaler Executor: Liest den Abschnitt, erzeugt unveränderten Draft,
    und schreibt ein triviales Change-Log und leeres citations_manifest.
    """
    section_path = _resolve_section_path(section_id)
    try:
        original = read_text(section_path)
    except Exception:
        original = f"# {section_id}\n\n(Abschnitt nicht gefunden – Platzhalterentwurf)\n"

    draft_md = original
    change_log = {
        "section_id": section_id,
        "changes": [],
        "rationale": "Initialer Durchlauf ohne Änderungen (Smoke-Executor)",
    }
    citations_manifest = {
        "section_id": section_id,
        "items": []
    }
    return draft_md, change_log, citations_manifest

