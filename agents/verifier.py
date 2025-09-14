from __future__ import annotations

from typing import Dict, Any

from .config import Playbook, canonical_section_id


def run_verifier(section_id: str, playbook: Playbook) -> Dict[str, Any]:
    canonical = canonical_section_id(section_id, playbook)
    return {
        "section_id": canonical,
        "approved": False,
        "issues_remaining": [],
    }

