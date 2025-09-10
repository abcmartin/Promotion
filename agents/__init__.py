"""Agenten-Framework fr die Dissertation-Optimierung.

Module:
- cli: Kommandozeilen-Schnittstelle fr den Multi-Agenten-Workflow
- file_utils: Datei-/Pfad-Helferfunktionen
- chunker: Markdown-Chunks erzeugen (Kapitel/Abschnitte)
- planner: Planung auf Basis von planner_output.yaml
- auditor: Qualitts-/Evidenz-Checks (heuristisch)
- executor: Vorschle/Edits erzeugen (dry-run standardmg)
- verifier: Wortzahlen/APA/Konsistenz prfen
- diff_logging: Diffs und JSON-Logs schreiben
- pubmed_apa: PubMed/Entrez (Stub) und APA-Formatter
"""

__all__ = [
    "cli",
    "file_utils",
    "chunker",
    "planner",
    "auditor",
    "executor",
    "verifier",
    "diff_logging",
    "pubmed_apa",
]

