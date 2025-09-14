from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class ProjectPaths:
    root: Path
    manuscript_dir: Path
    prompts_dir: Path
    results_dir: Path
    audit_dir: Path
    verify_dir: Path
    reports_dir: Path

    @classmethod
    def from_root(cls, root: Path) -> "ProjectPaths":
        return cls(
            root=root,
            manuscript_dir=root / "manuscript",
            prompts_dir=root / "prompts",
            results_dir=root / "results",
            audit_dir=root / "audit",
            verify_dir=root / "verify",
            reports_dir=root / "reports",
        )


def ensure_dirs(paths: ProjectPaths) -> None:
    for d in [paths.results_dir, paths.audit_dir, paths.verify_dir, paths.reports_dir]:
        d.mkdir(parents=True, exist_ok=True)

