from __future__ import annotations

import difflib
import json
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class DiffEntry:
    loc: str
    change_type: str
    rationale: str
    old_snippet: str
    new_snippet: str


def compute_unified_diff(old: str, new: str, fromfile: str = "old", tofile: str = "new") -> str:
    diff = difflib.unified_diff(
        old.splitlines(keepends=True),
        new.splitlines(keepends=True),
        fromfile=fromfile,
        tofile=tofile,
        lineterm="",
    )
    return "".join(diff)


def change_log(entries: List[DiffEntry]) -> Dict[str, Any]:
    return {
        "changes": [
            {
                "loc": e.loc,
                "change_type": e.change_type,
                "rationale": e.rationale,
                "old_snippet": e.old_snippet,
                "new_snippet": e.new_snippet,
            }
            for e in entries
        ]
    }

