import argparse
import json
import os
import sys
from datetime import datetime
from typing import Any, Dict, Optional

# Wire agent modules
from .config import load_playbook
from .planner import run_planner
from .auditor import run_auditor
from .executor import run_executor
from .verifier import run_verifier
try:
    from .researcher import run_researcher  # type: ignore
except Exception:
    run_researcher = None  # type: ignore
try:
    from .reporter import run_reporter  # type: ignore
except Exception:
    run_reporter = None  # type: ignore


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
    playbook = load_playbook(root=".")
    plan = run_planner(section_id, playbook)
    # add timestamp
    plan.setdefault("planner_output", {})["generated_date"] = _now_iso()
    _save_json(os.path.abspath(f"plans/{section_id}_planner_output.json"), plan)
    # optional curated YAML mirror
    curated_yaml = os.path.abspath("planner_output.yaml")
    if os.path.exists(curated_yaml):
        content = _read_text(curated_yaml)
        _write_text(os.path.abspath(f"plans/{section_id}_planner_output.yaml"), content)
    return 0


def cmd_audit(section_id: str) -> int:
    playbook = load_playbook(root=".")
    report = run_auditor(section_id, playbook)
    report["generated_date"] = _now_iso()
    _save_json(os.path.abspath(f"audit/{section_id}_auditor_report.json"), report)
    return 0


def cmd_execute(section_id: str) -> int:
    playbook = load_playbook(root=".")
    result = run_executor(section_id, playbook, root=".")
    draft = result.get("draft_markdown", "")
    _write_text(os.path.abspath(f"drafts/{section_id}_draft.md"), draft)
    log = result.get("change_log", {})
    log["generated_date"] = _now_iso()
    _save_json(os.path.abspath(f"drafts/{section_id}_change_log.json"), log)
    return 0


def cmd_verify(section_id: str) -> int:
    playbook = load_playbook(root=".")
    verification = run_verifier(section_id, playbook)
    verification["generated_date"] = _now_iso()
    _save_json(os.path.abspath(f"verify/{section_id}_verification_result.json"), verification)
    return 0


def cmd_research(section_id: str) -> int:
    if run_researcher is None:
        # graceful fallback stub
        out = {
            "section_id": section_id,
            "queries": [],
            "sources": [],
            "generated_date": _now_iso(),
            "note": "Researcher-Modul nicht verfügbar (Stub)",
        }
    else:
        playbook = load_playbook(root=".")
        out = run_researcher(section_id, playbook)
        out["generated_date"] = _now_iso()
    _save_json(os.path.abspath(f"research/{section_id}_research_output.json"), out)
    return 0


def cmd_report(section_id: str) -> int:
    if run_reporter is None:
        out = {
            "section_id": section_id,
            "approved": False,
            "open_issues": ["Reporter-Modul nicht verfügbar (Stub)"],
            "generated_date": _now_iso(),
        }
        _save_json(os.path.abspath(f"reports/{section_id}_report.json"), out)
        _write_text(os.path.abspath(f"reports/{section_id}_summary.md"), "Reporter-Stub: keine Zusammenfassung verfügbar.")
        return 0
    playbook = load_playbook(root=".")
    out = run_reporter(section_id, playbook, root=".")
    out_json = out.get("report", {})
    out_json["generated_date"] = _now_iso()
    _save_json(os.path.abspath(f"reports/{section_id}_report.json"), out_json)
    summary_md = out.get("summary_md", "")
    _write_text(os.path.abspath(f"reports/{section_id}_summary.md"), summary_md)
    return 0


def cmd_run_all(section_id: str) -> int:
    # Full pipeline: plan → research → audit → execute → verify → report
    for fn in (cmd_plan, cmd_research, cmd_audit, cmd_execute, cmd_verify, cmd_report):
        rc = fn(section_id)
        if rc != 0:
            return rc
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="agents", description="Multi‑Agent Orchestrator (Planner → Auditor → Executor → Verifier)")
    sub = p.add_subparsers(dest="cmd", required=True)

    for name in ("plan", "research", "audit", "execute", "verify", "report", "run-all"):
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
    if cmd == "research":
        return cmd_research(section_id)
    if cmd == "execute":
        return cmd_execute(section_id)
    if cmd == "verify":
        return cmd_verify(section_id)
    if cmd == "report":
        return cmd_report(section_id)
    if cmd == "run_all":
        return cmd_run_all(section_id)
    parser.error(f"Unbekannter Befehl: {args.cmd}")
    return 2


if __name__ == "__main__":
    sys.exit(main())

