import argparse
import json
import os
import re
import sys
from datetime import datetime
from typing import Any, Dict, Optional

from . import chunker
from .config import load_playbook


def _now_iso() -> str:
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def _read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _write_text(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def _save_json(path: str, data: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _normalize_section_id(section_id: str) -> str:
    """
    Normalize section_id to prevent path traversal and ensure consistent format.
    Returns a safe section identifier without manuscript/ prefix or .md suffix.
    """
    # Remove any directory traversal attempts
    section_id = section_id.replace("..", "")
    
    # Remove manuscript/ prefix if present (before converting slashes)
    manuscript_prefix = "manuscript/"
    if section_id.startswith(manuscript_prefix):
        section_id = section_id[len(manuscript_prefix):]
    
    # Remove .md suffix if present
    if section_id.endswith(".md"):
        section_id = section_id[:-3]
    
    # Now replace any remaining path separators
    section_id = section_id.replace("/", "_").replace("\\", "_")
    
    # Ensure only safe characters (alphanumeric, underscore, hyphen)
    section_id = re.sub(r'[^a-zA-Z0-9_-]', '_', section_id)
    
    return section_id


def _resolve_section_path(section_id: str) -> str:
    """
    Resolve section_id to absolute manuscript path.
    Normalizes input and constructs consistent path under manuscript/.
    """
    normalized_id = _normalize_section_id(section_id)
    return os.path.abspath(os.path.join("manuscript", f"{normalized_id}.md"))


def cmd_plan(section_id: str) -> int:
    """Plan phase: Generate planning artifacts for a section."""
    # Normalize section_id for artifact naming
    normalized_id = _normalize_section_id(section_id)
    section_path = _resolve_section_path(section_id)
    
    # Load playbook if available
    playbook = load_playbook(".")
    
    plan = {
        "planner_output": {
            "section": section_path,
            "task": "Auto-generated plan (stub)",
            "generated_date": _now_iso(),
        }
    }
    _save_json(os.path.abspath(f"plans/{normalized_id}_planner_output.json"), plan)
    
    # Also copy existing curated YAML if present to plans/
    curated_yaml = os.path.abspath("planner_output.yaml")
    if os.path.exists(curated_yaml):
        content = _read_text(curated_yaml)
        _write_text(os.path.abspath(f"plans/{normalized_id}_planner_output.yaml"), content)
    return 0


def cmd_audit(section_id: str) -> int:
    """Audit phase: Generate audit report for a section."""
    normalized_id = _normalize_section_id(section_id)
    
    report = {
        "section_id": normalized_id,
        "approved": False,
        "findings": [
            {
                "id": "stub-1",
                "severity": "minor",
                "issue": "Dies ist ein Platzhalter-Auditor-Report. Bitte echten Auditorlauf ausführen.",
                "fix": "Agentenlauf mit aktueller Evidenz durchführen."
            }
        ],
        "generated_date": _now_iso(),
    }
    _save_json(os.path.abspath(f"audit/{normalized_id}_auditor_report.json"), report)
    return 0


def cmd_execute(section_id: str) -> int:
    """Execute phase: Generate draft and change log for a section."""
    normalized_id = _normalize_section_id(section_id)
    src_path = _resolve_section_path(section_id)
    
    if os.path.exists(src_path):
        draft = _read_text(src_path)
    else:
        draft = f"# {normalized_id}\n\n[Stub‑Entwurf erzeugt { _now_iso() }]\n"
    
    _write_text(os.path.abspath(f"drafts/{normalized_id}_draft.md"), draft)
    
    # Change log schema aligned with agents.diff_logging
    change_log = {
        "generated_date": _now_iso(),
        "changes": [
            {
                "loc": "full",
                "change_type": "rewrite",
                "rationale": "Stub‑Executor hat Entwurf gespiegelt.",
                "sources_added": [],
                "old_snippet": "",
                "new_snippet": draft[:200] + "..." if len(draft) > 200 else draft
            }
        ]
    }
    _save_json(os.path.abspath(f"drafts/{normalized_id}_change_log.json"), change_log)
    return 0


def cmd_verify(section_id: str) -> int:
    """Verify phase: Generate verification report for a section."""
    normalized_id = _normalize_section_id(section_id)
    
    verification = {
        "section_id": normalized_id,
        "approved": False,
        "issues_remaining": [
            "Stub‑Verifier: APA‑Konformität nicht geprüft",
            "Stub‑Verifier: Wortziel nicht geprüft",
        ],
        "release_notes": "Dies ist ein Platzhalter‑Verifikationsbericht.",
        "generated_date": _now_iso(),
    }
    _save_json(os.path.abspath(f"verify/{normalized_id}_verification_result.json"), verification)
    return 0


def cmd_run_all(section_id: str) -> int:
    """Run all phases sequentially: plan → audit → execute → verify."""
    rc = cmd_plan(section_id)
    if rc != 0:
        return rc
    rc = cmd_audit(section_id)
    if rc != 0:
        return rc
    rc = cmd_execute(section_id)
    if rc != 0:
        return rc
    rc = cmd_verify(section_id)
    if rc != 0:
        return rc
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="agents", description="Multi‑Agent Orchestrator (Planner → Auditor → Executor → Verifier)")
    sub = p.add_subparsers(dest="cmd", required=True)

    for name in ("plan", "audit", "execute", "verify", "run-all"):
        sp = sub.add_parser(name)
        sp.add_argument("section_id", help="Kapitel/Abschnitts‑ID, z. B. 5_material_methods oder 3_background")

    return p


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    cmd = args.cmd.replace("-", "_")
    section_id: str = args.section_id

    if cmd == "plan":
        return cmd_plan(section_id)
    if cmd == "audit":
        return cmd_audit(section_id)
    if cmd == "execute":
        return cmd_execute(section_id)
    if cmd == "verify":
        return cmd_verify(section_id)
    if cmd == "run_all":
        return cmd_run_all(section_id)
    parser.error(f"Unbekannter Befehl: {args.cmd}")
    return 2


if __name__ == "__main__":
    sys.exit(main())

