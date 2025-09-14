from __future__ import annotations

import os
from typing import List

from .config import Playbook, canonical_section_id


def resolve_section_path(section_id: str, playbook: Playbook, root: str = ".") -> str:
    canonical = canonical_section_id(section_id, playbook)
    if canonical.endswith(".md"):
        rel = canonical
    else:
        rel = f"manuscript/{canonical}.md"
    return os.path.abspath(os.path.join(root, rel))


def available_sections(root: str = "manuscript") -> List[str]:
    # Return list of section ids without directory prefix
    abs_root = os.path.abspath(root)
    if not os.path.isdir(abs_root):
        return []
    ids: List[str] = []
    for name in os.listdir(abs_root):
        if not name.endswith(".md"):
            continue
        ids.append(name.replace(".md", ""))
    return sorted(ids)

