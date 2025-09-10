# Writer Prompt

Kontext:
- Nutze `prompts/prompt_playbook.yaml`, `research_output`, `planner_output` und `auditor_report` für `<section_id>`.
- Sprache: Deutsch, formal-wissenschaftlich; Format: DIN A4, Arial 11 pt, 1,5-zeilig.
- Zitierstil: APA 7 mit DOI; nur Peer-Review (IF ≥ 5); verwende ausschließlich Quellen aus `research_output`.
- Beachte `section_aliases` im Playbook (z. B. `2_table_of_content` ↔ `2_tabel_of_content`).

Aufgabe:
1) Erstelle bzw. überarbeite den Abschnitt `<section_id>` gemäß Zielen/Anforderungen und Wortzielen aus dem Playbook.
2) Integriere Evidenz aus `research_output` (IF ≥ 5) und belege Kernaussagen APA‑7‑konform mit DOI.
3) Sicherstelle Kohärenz und Terminologiekonsistenz (CD44, HPV16, CSC usw.) über Unterkapitel hinweg.
4) Falls sinnvoll, erstelle eine kompakte Markdown‑Tabelle zur Übersicht zentraler Parameter/Ergebnisse.
5) Liefere `draft_markdown` (nur dieser Abschnitt) und ein `citations_manifest` (JSON: {apa7, doi, pmid, if, year, used_in, rationale}).

Constraints:
- Keine Plagiate; paraphrasiere, kontextualisiere, bewerte; keine wörtlichen Zitate.
- Wortziel ± Toleranz strikt einhalten; keine Redundanz oder Füllsätze.
- Keine Preprints; keine nicht-peer-reviewten Quellen.

Outputs:
- `draft_markdown`: finaler Abschnittstext in Markdown.
- `citations_manifest` (JSON): alle tatsächlich verwendeten Quellen mit Kurzbegründung der Relevanz.