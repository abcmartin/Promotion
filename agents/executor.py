from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from .diff_logging import write_edit_log


def propose_edits(
    *,
    chunks_json_path: Path,
    audit_json_path: Optional[Path] = None,
    log_dir: Optional[Path] = None,
) -> List[Dict[str, Any]]:
    chunks: List[Dict[str, Any]] = json.loads(Path(chunks_json_path).read_text(encoding="utf-8"))
    audit_issues: List[Dict[str, Any]] = []
    if audit_json_path and Path(audit_json_path).exists():
        audit = json.loads(Path(audit_json_path).read_text(encoding="utf-8"))
        audit_issues = audit.get("issues", [])

    issues_by_id = {}
    for issue in audit_issues:
        issues_by_id.setdefault(issue.get("id"), []).append(issue)

    edits: List[Dict[str, Any]] = []
    for c in chunks:
        cid = c.get("id")
        content = c.get("content", "")
        suggestions: List[str] = []
        new_content = content

        for issue in issues_by_id.get(cid, []):
            if issue.get("type") == "citation_missing":
                suggestions.append("Fge mindestens eine belastbare Quelle mit IF = 5 hinzu.")
                # Minimaler, nicht-destruktiver Hinweis an Chunkende
                new_content = content + "\n\n[Hinweis]: Quelle(n) ergnzen (PMID vorschlagen)."
            elif issue.get("type") == "style_long_sentences":
                suggestions.append("Teile sehr lange Stze in krzere Einheiten.")
            elif issue.get("type") == "style_passive":
                suggestions.append("Aktiviere Formulierungen, Passiv reduzieren.")

        if new_content != content or suggestions:
            edit = {
                "chunk_id": cid,
                "source_path": c.get("source_path"),
                "title": c.get("title"),
                "suggestions": suggestions,
                "old": content,
                "new": new_content,
            }
            edits.append(edit)
            if log_dir:
                write_edit_log(
                    log_dir=log_dir,
                    source_path=str(c.get("source_path")),
                    old=content,
                    new=new_content,
                    meta={"chunk_id": cid, "title": c.get("title")},
                )

    return edits

