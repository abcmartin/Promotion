from __future__ import annotations

from typing import Dict, Any, List

from .config import Playbook, canonical_section_id


def _default_queries(section_id: str) -> List[str]:
    # Minimal heuristic queries; in einer echten Implementierung würden hier PubMed-APIs genutzt
    base = section_id.replace("_", " ")
    return [
        f"({base}) AND (head and neck squamous cell carcinoma OR HNSCC)",
        f"CD44 AND survival AND Cox AND (proportional hazards)",
        f"REMARK reporting guideline tumor markers"
    ]


def run_researcher(section_id: str, playbook: Playbook) -> Dict[str, Any]:
    canonical = canonical_section_id(section_id, playbook)
    # Stubbed output structure compatible with prompts/researcher_prompt.md expectations
    return {
        "section_id": canonical,
        "queries": _default_queries(canonical),
        "inclusion_criteria": [
            "Peer-Reviewed Journals",
            "Impact Factor >= 5",
            "HNSCC/CD44-Relevanz",
        ],
        "exclusion_criteria": [
            "Preprints",
            "Nicht-peer-reviewte Quellen",
        ],
        "sources": [],  # echte Suche kann später ergänzt werden
        "gaps": [],
        "risks": [],
    }

