from __future__ import annotations

from pathlib import Path
from typing import Any, Dict
import yaml


def build_plan_from_yaml(yaml_path: Path) -> Dict[str, Any]:
    data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    section = data.get("planner_output", {}).get("section")
    task = data.get("planner_output", {}).get("task")
    acceptance = data.get("planner_output", {}).get("acceptance_criteria_covered", [])
    status = data.get("planner_output", {}).get("acceptance_criteria_status", {})

    plan = {
        "target_section": section,
        "task": task,
        "acceptance_criteria": acceptance,
        "status": status,
        "raw": data,
    }
    return plan

