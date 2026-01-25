from __future__ import annotations

from typing import Dict, Any

from .config import Playbook, canonical_section_id
from . import chunker


def run_planner(section_id: str, playbook: Playbook) -> Dict[str, Any]:
    canonical = canonical_section_id(section_id, playbook)
    section_path = chunker.resolve_section_path(canonical, playbook)
    return {
        "planner_output": {
            "section": section_path,
            "task": "Plan (Stub)",
        }
    }

