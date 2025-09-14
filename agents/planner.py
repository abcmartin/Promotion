import os
from datetime import datetime
from .file_utils import read_text


def run_planner(section_id: str) -> str:
    """
    Minimale Planner-Implementierung: Gibt vorhandenes `planner_output.yaml` zurück,
    falls vorhanden; sonst erzeugt sie ein schlankes YAML-Gerüst mit Metadaten.
    """
    # Falls ein globales planner_output.yaml im Repo existiert, verwende es direkt
    repo_path = os.path.join("planner_output.yaml")
    if os.path.exists(repo_path):
        return read_text(repo_path)

    # Fallback: minimales YAML mit Platzhaltern
    ts = datetime.utcnow().isoformat() + "Z"
    yaml_text = (
        "planner_output:\n"
        f"  section: \"{section_id}\"\n"
        f"  task: \"Automated plan for {section_id}\"\n"
        f"  generated_date: \"{ts}\"\n"
        "  evidence_shortlist: []\n"
        "  acceptance_criteria_covered: []\n"
        "  acceptance_criteria_status: {}\n"
    )
    return yaml_text

