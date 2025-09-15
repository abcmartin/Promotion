# Reporter Prompt

Kontext:
- Konsolidiere Ergebnisse für `<section_id>` aus: `planner_output`, `research_output`, `draft_markdown`/`change_log` (Writer/Executor), `auditor_report`, `verification_result`.
- Nutze `prompts/prompt_playbook.yaml` (Wortziele, Aliasse) als Referenz.

Aufgabe:
1) Erzeuge einen JSON‑Bericht `report` mit Feldern:
   - `section_id`, `canonical_section_id` (gemäß `section_aliases`)
   - `word_target` (aus Playbook), `word_count`
   - `approvals`: {auditor: bool, verifier: bool}
   - `open_issues`: konsolidierte Liste offener Punkte (Quelle: Auditor/Verifier)
   - `changes`: aus `change_log` (Liste mit Ort, Änderung, Begründung)
   - `references_summary`: Zählung und Liste aller DOIs aus `citations_manifest`
2) Erzeuge zusätzlich eine kurze Markdown‑Zusammenfassung `summary_md` (stichpunktartig, high‑signal), inkl. Compliance‑Status.

Constraints:
- Nur Quellen aus `citations_manifest`; alle Einträge mit DOI.
- Keine vertraulichen Daten aus RAG exportieren; nur Metadaten der Zitationen.

Outputs:
- `report` (JSON) und `summary_md` (Markdown).