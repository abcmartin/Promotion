from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import yaml


@dataclass
class AgentConfig:
    manuscript_dir: Path
    output_dir: Path
    chunk_level: int = 2
    targets_json: Optional[Path] = None
    logs_dir: Optional[Path] = None
    entrez_email: Optional[str] = None
    entrez_api_key: Optional[str] = None


def load_config(path: Path) -> AgentConfig:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return AgentConfig(
        manuscript_dir=Path(data.get("manuscript_dir", ".")),
        output_dir=Path(data.get("output_dir", ".agent")),
        chunk_level=int(data.get("chunk_level", 2)),
        targets_json=Path(data["targets_json"]) if data.get("targets_json") else None,
        logs_dir=Path(data["logs_dir"]) if data.get("logs_dir") else None,
        entrez_email=data.get("entrez_email"),
        entrez_api_key=data.get("entrez_api_key"),
    )

