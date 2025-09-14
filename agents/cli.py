import argparse
import json
import os
import sys
from datetime import datetime
from typing import Any, Dict, Optional


def _now_iso() -> str:
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def _read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _write_text(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def _load_yaml(path: str) -> Optional[Dict[str, Any]]:
    try:
        import yaml  # type: ignore
    except Exception:
        return None
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _save_json(path: str, data: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def cmd_plan(section_id: str) -> int:
    # Pass-through: read prompts/planner_prompt.md and create a stub plan
    prompt = _read_text(os.path.abspath("prompts/planner_prompt.md"))
    plan = {
        "planner_output": {
            "section": f"manuscript/{section_id}.md" if section_id.endswith(".md") is False else section_id,
            "task": "Auto-generated plan (stub)",
            "generated_date": _now_iso(),
        }
    }
    _save_json(os.path.abspath(f"plans/{section_id}_planner_output.json"), plan)
    # Also copy existing curated YAML if present to plans/
    curated_yaml = os.path.abspath("planner_output.yaml")
    if os.path.exists(curated_yaml):
        content = _read_text(curated_yaml)
        _write_text(os.path.abspath(f"plans/{section_id}_planner_output.yaml"), content)
    return 0


def cmd_audit(section_id: str) -> int:
    prompt = _read_text(os.path.abspath("prompts/auditor_prompt.md"))
    report = {
        "section_id": section_id,
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
    _save_json(os.path.abspath(f"audit/{section_id}_auditor_report.json"), report)
    return 0


def cmd_execute(section_id: str) -> int:
    prompt = _read_text(os.path.abspath("prompts/executor_prompt.md"))
    # Minimal draft passthrough: copy manuscript file to drafts with timestamp note
    src_path = os.path.abspath(f"manuscript/{section_id}.md") if not section_id.endswith(".md") else os.path.abspath(f"manuscript/{section_id}")
    if os.path.exists(src_path):
        draft = _read_text(src_path)
    else:
        draft = f"# {section_id}\n\n[Stub‑Entwurf erzeugt { _now_iso() }]\n"
    _write_text(os.path.abspath(f"drafts/{section_id}_draft.md"), draft)
    # Minimal change log
    change_log = {
        "generated_date": _now_iso(),
        "changes": [
            {
                "loc": "full",
                "change_type": "rewrite",
                "rationale": "Stub‑Executor hat Entwurf gespiegelt.",
                "sources_added": []
            }
        ]
    }
    _save_json(os.path.abspath(f"drafts/{section_id}_change_log.json"), change_log)
    return 0


def cmd_verify(section_id: str) -> int:
    prompt = _read_text(os.path.abspath("prompts/verifier_prompt.md"))
    verification = {
        "section_id": section_id,
        "approved": False,
        "issues_remaining": [
            "Stub‑Verifier: APA‑Konformität nicht geprüft",
            "Stub‑Verifier: Wortziel nicht geprüft",
        ],
        "release_notes": "Dies ist ein Platzhalter‑Verifikationsbericht.",
        "generated_date": _now_iso(),
    }
    _save_json(os.path.abspath(f"verify/{section_id}_verification_result.json"), verification)
    return 0


def cmd_run_all(section_id: str) -> int:
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

