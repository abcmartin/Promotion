# Researcher Prompt

Kontext:
- Nutze das Playbook unter `prompts/prompt_playbook.yaml` und die RAG-Quellen unter `/Users/martin/Promotion/context`.
- Nur Peer‑Review‑Quellen mit Impact‑Faktor ≥ 5 (bevorzugt PubMed/MEDLINE, ggf. Scopus/Web of Science zur IF‑Validierung).
- Zitierstil: APA 7 (mit DOI, vorzugsweise `https://doi.org/...`).

Aufgabe:
1) Für `<section_id>` erstelle eine präzise Suchstrategie (boolean queries) für PubMed.
2) Führe die Recherche durch (virtuell) und liefere 10–25 Kernquellen, die die inhaltlichen Anforderungen abdecken (inkl. aktuelle Leitlinien/Positionspapiere, wo relevant).
3) Verifiziere den Impact‑Faktor (IF) ≥ 5 (jährlich oder zum Veröffentlichungsjahr) und dokumentiere Quelle der IF‑Angabe.
4) Erstelle strukturierte Exzerpte (2–4 Sätze) pro Quelle: Kernaussage, Studiendesign, Population, Outcome, Limitationen.
5) Liefere ein JSON `research_output` mit: queries, inclusion_criteria, exclusion_criteria, sources[{apa7, doi, pmid, if, year, summary, relevance_tags}], gaps, risks.

Constraints:
- Keine Preprints, keine nicht-peer-reviewten Quellen, keine Dubletten.
- Bevorzuge systematische Reviews, Metaanalysen, RCTs; ansonsten große Kohorten.
- HPV16-/CD44‑Fokus gemäß Abschnitt.
