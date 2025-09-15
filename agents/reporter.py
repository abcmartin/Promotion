from __future__ import annotations

import json
import os
from typing import Dict, Any

from .config import Playbook, canonical_section_id
from .chunker import resolve_section_path


def _read_json(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return {}


def _read_text(path: str) -> str:
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def run_reporter(section_id: str, playbook: Playbook, root: str = ".") -> Dict[str, Any]:
    canonical = canonical_section_id(section_id, playbook)

    # Gather inputs
    plan = _read_json(os.path.abspath(os.path.join(root, f"plans/{section_id}_planner_output.json")))
    research = _read_json(os.path.abspath(os.path.join(root, f"research/{section_id}_research_output.json")))
    auditor = _read_json(os.path.abspath(os.path.join(root, f"audit/{section_id}_auditor_report.json")))
    change_log = _read_json(os.path.abspath(os.path.join(root, f"drafts/{section_id}_change_log.json")))
    verify = _read_json(os.path.abspath(os.path.join(root, f"verify/{section_id}_verification_result.json")))

    # Compute word target
    wt = playbook.word_targets.get(canonical, {})
    word_target = wt.get("target", None)

    # Count words in the current manuscript file (if present)
    manuscript_path = resolve_section_path(section_id, playbook, root=root)
    text = _read_text(manuscript_path)
    word_count = len(text.split()) if text else 0

    approvals = {
        "auditor": bool(auditor.get("approved", False)),
        "verifier": bool(verify.get("approved", False)),
    }

    open_issues = []
    for f in auditor.get("findings", []) or []:
        issue = f.get("issue")
        if issue:
            open_issues.append(issue)
    for i in verify.get("issues_remaining", []) or []:
        open_issues.append(i)

    # Collate references from a citations manifest if executor created one (optional)
    citations_manifest_path = os.path.abspath(os.path.join(root, f"drafts/{section_id}_citations_manifest.json"))
    citations_manifest = _read_json(citations_manifest_path)
    references = citations_manifest.get("sources", []) if citations_manifest else []

    report: Dict[str, Any] = {
        "section_id": section_id,
        "canonical_section_id": canonical,
        "word_target": word_target,
        "word_count": word_count,
        "approvals": approvals,
        "open_issues": open_issues,
        "changes": change_log.get("changes", []),
        "references_summary": {
            "count": len(references),
            "dois": [r.get("doi") for r in references if r.get("doi")],
        },
    }

    # Short high-signal markdown summary
    summary_lines = [
        f"- Abschnitt: `{canonical}`",
        f"- Wortzahl: {word_count}" + (f" / Ziel: {word_target}" if word_target else ""),
        f"- Freigaben: Auditor={approvals['auditor']}, Verifier={approvals['verifier']}",
        f"- Offene Punkte: {len(open_issues)}",
    ]
    if references:
        summary_lines.append(f"- Referenzen (DOIs): {min(len(references), 5)} von {len(references)} gelistet")

    return {"report": report, "summary_md": "\n".join(summary_lines)}

