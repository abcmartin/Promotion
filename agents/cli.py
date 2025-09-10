import argparse
import sys
from pathlib import Path
from typing import Optional

from .file_utils import (
    ensure_directory,
    find_markdown_files,
    read_text_file,
    write_json_file,
)
from .chunker import chunk_markdown_content
from .planner import build_plan_from_yaml
from .auditor import audit_chunks
from .verifier import verify_manuscript
from .executor import propose_edits


def cmd_chunk(args: argparse.Namespace) -> int:
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    ensure_directory(output_dir)

    chunk_level = int(args.level)
    files = find_markdown_files(input_dir)
    all_chunks = []
    for md_file in files:
        content = read_text_file(md_file)
        chunks = chunk_markdown_content(
            content=content,
            source_path=str(md_file),
            min_heading_level=chunk_level,
        )
        all_chunks.extend(chunks)

    write_json_file(output_dir / "chunks.json", all_chunks)
    print(f"[chunk] {len(all_chunks)} Chunks -> {output_dir / 'chunks.json'}")
    return 0


def cmd_plan(args: argparse.Namespace) -> int:
    yaml_path = Path(args.planner_yaml)
    plan = build_plan_from_yaml(yaml_path)
    output_path = Path(args.output)
    ensure_directory(output_path.parent)
    write_json_file(output_path, plan)
    print(f"[plan] Plan gespeichert -> {output_path}")
    return 0


def cmd_audit(args: argparse.Namespace) -> int:
    chunks_path = Path(args.chunks)
    results = audit_chunks(chunks_json_path=chunks_path)
    output_path = Path(args.output)
    ensure_directory(output_path.parent)
    write_json_file(output_path, results)
    print(f"[audit] Bericht gespeichert -> {output_path}")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    manuscript_dir = Path(args.manuscript_dir)
    targets_json: Optional[Path] = Path(args.targets) if args.targets else None
    results = verify_manuscript(manuscript_dir=manuscript_dir, targets_json=targets_json)
    output_path = Path(args.output)
    ensure_directory(output_path.parent)
    write_json_file(output_path, results)
    print(f"[verify] Bericht gespeichert -> {output_path}")
    return 0


def cmd_execute(args: argparse.Namespace) -> int:
    chunks_path = Path(args.chunks)
    audit_path = Path(args.audit) if args.audit else None
    log_dir = Path(args.log_dir) if args.log_dir else None
    edits = propose_edits(chunks_json_path=chunks_path, audit_json_path=audit_path, log_dir=log_dir)
    output_path = Path(args.output)
    ensure_directory(output_path.parent)
    write_json_file(output_path, edits)
    print(f"[execute] Edits gespeichert -> {output_path} (dry-run)")
    return 0

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Multi-Agenten Dissertation-Optimierung (CLI)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_chunk = sub.add_parser("chunk", help="Manuskript in Markdown-Chunks zerlegen")
    p_chunk.add_argument("--input-dir", required=True, help="Pfad zum 'manuscript'-Verzeichnis")
    p_chunk.add_argument("--output-dir", required=True, help="Zielverzeichnis fr chunks.json")
    p_chunk.add_argument("--level", default="2", help="Minimale berschriften-Ebene (2=##, 3=###)")
    p_chunk.set_defaults(func=cmd_chunk)

    p_plan = sub.add_parser("plan", help="Plan aus planner_output.yaml bauen")
    p_plan.add_argument("--planner-yaml", required=True, help="Pfad zu planner_output.yaml")
    p_plan.add_argument("--output", required=True, help="Zielpfad fr plan.json")
    p_plan.set_defaults(func=cmd_plan)

    p_audit = sub.add_parser("audit", help="Heuristische Audits ber Chunks ausfhren")
    p_audit.add_argument("--chunks", required=True, help="Pfad zu chunks.json")
    p_audit.add_argument("--output", required=True, help="Zielpfad fr audit.json")
    p_audit.set_defaults(func=cmd_audit)

    p_verify = sub.add_parser("verify", help="Konsistenz-/Wortzahl-/APA-Checks ausfhren")
    p_verify.add_argument("--manuscript-dir", required=True, help="Pfad zum 'manuscript'-Verzeichnis")
    p_verify.add_argument("--targets", required=False, help="Pfad zu chapter_word_targets.json")
    p_verify.add_argument("--output", required=True, help="Zielpfad fr verify.json")
    p_verify.set_defaults(func=cmd_verify)

    p_exec = sub.add_parser("execute", help="Vorschlags-Edits (dry-run) aus Audit/Chunks ableiten")
    p_exec.add_argument("--chunks", required=True, help="Pfad zu chunks.json")
    p_exec.add_argument("--audit", required=False, help="Pfad zu audit.json")
    p_exec.add_argument("--log-dir", required=False, help="Verzeichnis fr Diff/Logs")
    p_exec.add_argument("--output", required=True, help="Zielpfad fr edits.json")
    p_exec.set_defaults(func=cmd_execute)

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())

