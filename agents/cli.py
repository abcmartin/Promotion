import argparse
import json
import os
import sys
from datetime import datetime

from .executor import run_executor
from .planner import run_planner
from .auditor import run_auditor
from .verifier import run_verifier
from .file_utils import ensure_dirs


def _default_paths():
    return {
        "plans": "plans",
        "audit": "audit",
        "drafts": "drafts",
        "verify": "verify",
        "reports": "reports",
    }


def cmd_run(section: str, resume: bool = False) -> int:
    paths = _default_paths()
    ensure_dirs(*paths.values())

    # 1) Planner
    planner_out = run_planner(section_id=section)
    planner_path = os.path.join(paths["plans"], f"{section}_planner_output.yaml")
    with open(planner_path, "w", encoding="utf-8") as f:
        f.write(planner_out)

    # 2) Auditor
    auditor_json = run_auditor(section_id=section, planner_output_path=planner_path)
    auditor_path = os.path.join(paths["audit"], f"{section}_auditor_report.json")
    with open(auditor_path, "w", encoding="utf-8") as f:
        json.dump(auditor_json, f, ensure_ascii=False, indent=2)

    # 3) Executor
    draft_md, change_log, citations_manifest = run_executor(
        section_id=section, planner_output_path=planner_path, auditor_report_path=auditor_path
    )
    draft_path = os.path.join(paths["drafts"], f"{section}_draft.md")
    with open(draft_path, "w", encoding="utf-8") as f:
        f.write(draft_md)
    change_log_path = os.path.join(paths["drafts"], f"{section}_change_log.json")
    with open(change_log_path, "w", encoding="utf-8") as f:
        json.dump(change_log, f, ensure_ascii=False, indent=2)
    citations_path = os.path.join(paths["drafts"], f"{section}_citations_manifest.json")
    with open(citations_path, "w", encoding="utf-8") as f:
        json.dump(citations_manifest, f, ensure_ascii=False, indent=2)

    # 4) Verifier
    verification = run_verifier(
        section_id=section, draft_markdown_path=draft_path, citations_manifest_path=citations_path
    )
    verify_path = os.path.join(paths["verify"], f"{section}_verification_result.json")
    with open(verify_path, "w", encoding="utf-8") as f:
        json.dump(verification, f, ensure_ascii=False, indent=2)

    # 5) Reporter (optional Konsolidat)
    report = {
        "section_id": section,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "artifacts": {
            "planner_output": planner_path,
            "auditor_report": auditor_path,
            "draft_markdown": draft_path,
            "change_log": change_log_path,
            "citations_manifest": citations_path,
            "verification_result": verify_path,
        },
    }
    report_path = os.path.join(paths["reports"], f"{section}_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"[OK] Agenten-Workflow abgeschlossen. Report: {report_path}")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="agents", description="Multi-Agenten Dissertation Workflow")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_run = sub.add_parser("run", help="Planner → Auditor → Executor → Verifier für eine Sektion ausführen")
    p_run.add_argument("--section", required=True, help="Sektions-ID, z. B. 5_material_methods")
    p_run.add_argument("--resume", action="store_true", help="Vorhandene Artefakte wiederverwenden, wenn möglich")

    args = parser.parse_args(argv)

    if args.cmd == "run":
        return cmd_run(section=args.section, resume=args.resume)

    return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

