from __future__ import annotations

import os
from typing import Dict, Any

from .chunker import resolve_section_path
from .config import Playbook, canonical_section_id
from .diff_logging import DiffEntry, change_log, compute_unified_diff


def run_executor(section_id: str, playbook: Playbook, root: str = ".") -> Dict[str, Any]:
    src_path = resolve_section_path(section_id, playbook, root=root)
    if os.path.exists(src_path):
        with open(src_path, "r", encoding="utf-8") as f:
            old_text = f.read()
    else:
        old_text = ""

    # For now, this stub echoes the text unchanged
    new_text = old_text

    # Compute diff/log
    diff = compute_unified_diff(old_text, new_text, fromfile="before.md", tofile="after.md")
    entries = [
        DiffEntry(
            loc="full",
            change_type="rewrite",
            rationale="Stub‑Executor: keine Veränderung vorgenommen",
            old_snippet=old_text[:5000],
            new_snippet=new_text[:5000],
        )
    ]
    log = change_log(entries)
    log["diff"] = diff
    return {
        "draft_markdown": new_text,
        "change_log": log,
        "section_id": canonical_section_id(section_id, playbook),
    }

