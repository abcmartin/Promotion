import json
from typing import Dict


def run_auditor(section_id: str, planner_output_path: str) -> Dict:
    """
    Minimaler Auditor: Prüft formale Presence der Planner-Datei und liefert
    ein Dummy-Report-JSON mit approved=true, sofern Datei lesbar ist.
    """
    try:
        with open(planner_output_path, "r", encoding="utf-8") as f:
            _ = f.read(2048)
        approved = True
        findings = []
    except Exception as e:
        approved = False
        findings = [{
            "id": "planner_missing",
            "severity": "blocker",
            "issue": f"Planner output not readable: {e}",
            "fix": "Ensure planner created a valid YAML."
        }]

    return {
        "section_id": section_id,
        "approved": approved,
        "findings": findings,
    }

