import argparse
import json
import sys
from pathlib import Path


def _read_text_file(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return path.read_text(encoding="utf-8")


def _write_text_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _load_json(path: Path):
    return json.loads(_read_text_file(path))


def _save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def cmd_plan(args: argparse.Namespace) -> int:
    # For now, simply echo the planner_output.yaml location and section
    print(f"[Planner] Section: {args.section}")
    planner_path = Path(args.planner_output)
    if planner_path.exists():
        print(f"[Planner] Using existing planner_output: {planner_path}")
    else:
        print(f"[Planner] Planner output not found at {planner_path}; skipping generation.")
    return 0


def cmd_audit(args: argparse.Namespace) -> int:
    print(f"[Auditor] Section: {args.section}")
    # Minimal stub that writes a simple auditor report
    report = {
        "section_id": args.section,
        "approved": True,
        "findings": [],
    }
    out = Path(args.output or f"audit/{args.section.replace('/', '_')}_auditor_report.json")
    _save_json(out, report)
    print(f"[Auditor] Wrote {out}")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    print(f"[Verifier] Section: {args.section}")
    # Minimal verifier: check word count range if targets file exists
    targets_path = Path("prompts/chapter_word_targets.json")
    result = {"section_id": args.section, "approved": True, "issues_remaining": []}
    try:
        targets = _load_json(targets_path)
        key = Path(args.section).stem
        tgt = targets.get(key)
        word_count = 0
        section_file = Path(args.section)
        if section_file.exists():
            text = _read_text_file(section_file)
            word_count = len(text.split())
        result["word_count"] = word_count
        if tgt:
            lo = tgt["target"] - tgt["tolerance"]
            hi = tgt["target"] + tgt["tolerance"]
            result["word_target"] = tgt["target"]
            if not (lo <= word_count <= hi):
                result["approved"] = False
                result["issues_remaining"].append({
                    "severity": "minor",
                    "issue": f"Word count {word_count} outside [{lo}, {hi}]",
                    "fix": "Adjust section length"
                })
    except Exception as e:
        result["approved"] = False
        result["issues_remaining"].append({"severity": "major", "issue": str(e), "fix": "Ensure targets file exists and is valid JSON"})
    out = Path(args.output or f"verify/{args.section.replace('/', '_')}_verification_result.json")
    _save_json(out, result)
    print(f"[Verifier] Wrote {out}")
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    section_id = args.section
    print(f"[Reporter] Section: {section_id}")
    # Assemble available artifacts
    auditor = Path(f"audit/{section_id.replace('/', '_')}_auditor_report.json")
    verifier = Path(f"verify/{section_id.replace('/', '_')}_verification_result.json")
    citations = Path("drafts/3_1_citations_manifest.json") if not args.citations else Path(args.citations)
    report = {
        "section_id": section_id,
        "approvals": {
            "auditor": auditor.exists(),
            "verifier": verifier.exists(),
        },
        "open_issues": [],
        "references_summary": {
            "count": 0,
            "dois": []
        }
    }
    if verifier.exists():
        try:
            ver = _load_json(verifier)
            report["open_issues"].extend(ver.get("issues_remaining", []))
        except Exception:
            pass
    if citations.exists():
        try:
            cm = _load_json(citations)
            dois = [c.get("doi") for c in cm if isinstance(cm, list)] if isinstance(cm, list) else []
            report["references_summary"]["dois"] = [d for d in dois if d]
            report["references_summary"]["count"] = len(report["references_summary"]["dois"])
        except Exception:
            pass
    out = Path(args.output or f"reports/{section_id.replace('/', '_')}_report.json")
    _save_json(out, report)
    print(f"[Reporter] Wrote {out}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="agents", description="Multi‑Agent Dissertation Manager (stub)")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("plan", help="Create or load plan for a section")
    sp.add_argument("section", help="Path to manuscript section (e.g., manuscript/5_material_methods.md)")
    sp.add_argument("--planner-output", default="planner_output.yaml")
    sp.set_defaults(func=cmd_plan)

    sa = sub.add_parser("audit", help="Run auditor checks for a section")
    sa.add_argument("section")
    sa.add_argument("--output")
    sa.set_defaults(func=cmd_audit)

    sv = sub.add_parser("verify", help="Run verifier for a section")
    sv.add_argument("section")
    sv.add_argument("--output")
    sv.set_defaults(func=cmd_verify)

    sr = sub.add_parser("report", help="Consolidate artifacts into a report")
    sr.add_argument("section")
    sr.add_argument("--citations")
    sr.add_argument("--output")
    sr.set_defaults(func=cmd_report)

    return p


def main(argv=None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)

