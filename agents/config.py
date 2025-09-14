from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class Playbook:
    section_aliases: Dict[str, str]
    word_targets: Dict[str, Dict[str, int]]


def _load_yaml(path: str) -> Optional[Dict[str, Any]]:
    try:
        import yaml  # type: ignore
    except Exception:
        return None
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_playbook(root: str = ".") -> Playbook:
    # Primary playbook path
    pb_path = os.path.abspath(os.path.join(root, "prompts/prompt_playbook.yaml"))
    data = _load_yaml(pb_path) or {}

    section_aliases = (data.get("global_context", {}) or {}).get("section_aliases", {}) or {}
    # Fallback alias map if not provided
    if not section_aliases:
        section_aliases = {}

    # Extract word targets
    word_targets = (data.get("global_context", {}) or {}).get("wortziel", {}) or {}

    return Playbook(section_aliases=section_aliases, word_targets=word_targets)


def canonical_section_id(section_id: str, playbook: Playbook) -> str:
    # Normalize to alias if defined
    return playbook.section_aliases.get(section_id, section_id)

