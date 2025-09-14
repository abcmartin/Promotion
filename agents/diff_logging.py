from __future__ import annotations

import difflib
import json
from pathlib import Path
from typing import Any, Dict


def unified_diff(old: str, new: str, *, fromfile: str = "old", tofile: str = "new") -> str:
    return "\n".join(
        difflib.unified_diff(
            old.splitlines(),
            new.splitlines(),
            fromfile=fromfile,
            tofile=tofile,
            lineterm="",
        )
    )


def write_edit_log(*, log_dir: Path, source_path: str, old: str, new: str, meta: Dict[str, Any]) -> None:
    log_dir.mkdir(parents=True, exist_ok=True)
    diff_text = unified_diff(old, new, fromfile=f"a/{source_path}", tofile=f"b/{source_path}")
    (log_dir / "last.diff").write_text(diff_text, encoding="utf-8")
    payload = {"source_path": source_path, "meta": meta}
    (log_dir / "last.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

