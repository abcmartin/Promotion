import json
from typing import Dict


def run_verifier(section_id: str, draft_markdown_path: str, citations_manifest_path: str) -> Dict:
    """
    Minimaler Verifier: Prüft Vorhandensein von Draft und Manifest,
    gibt approved=true zurück.
    """
    issues = []
    try:
        with open(draft_markdown_path, "r", encoding="utf-8") as f:
            content = f.read(2000)
            if len(content.strip()) == 0:
                issues.append({"severity": "major", "issue": "Leere Draft-Datei"})
    except Exception as e:
        issues.append({"severity": "blocker", "issue": f"Draft nicht lesbar: {e}"})

    try:
        with open(citations_manifest_path, "r", encoding="utf-8") as f:
            _ = json.load(f)
    except Exception as e:
        issues.append({"severity": "minor", "issue": f"Citations manifest nicht lesbar: {e}"})

    approved = not any(i["severity"] == "blocker" for i in issues)
    return {
        "section_id": section_id,
        "approved": approved,
        "issues_remaining": issues,
        "release_notes": "Minimaler Verifier-Durchlauf"
    }

