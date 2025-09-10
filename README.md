# Dissertationsoptimierung – Copilot‑Instructions

Dieses Verzeichnis enthält eine Sammlung von **Custom Instructions** und **Prompts** für GitHub Copilot Chat zur Optimierung einer medizinischen Dissertation über das prognostische Potential von CD44 bei Kopf‑Hals‑Plattenepithelkarzinomen.

## Struktur

* `.github/copilot-instructions.md` – Globale Richtlinien für alle Kapitel (Inhalt, Methodik, Sprache, Formalia und Qualitätssicherung).
* `.github/instructions/` – Rollenbasierte Anweisungen (Planner, Auditor, Executor, Verifier) sowie allgemeine Stil‑, APA‑ und Markdown‑Richtlinien. Zusätzlich enthalten sind kapitel‑ und abschnittsspezifische Anweisungen sowie Vorgaben zu Tabellen/Abbildungen.
* `.github/instructions/chapters/` – Kapitelweise Vorgaben mit Zielwortzahlen und Schwerpunkten für Deckblatt, Abstract, Hintergrund, Fragestellung, Methoden, Ergebnisse, Diskussion und Literaturverzeichnis.
* `.github/instructions/sections/` – Feingranulare Anweisungen für spezielle Abschnitte, z. B. die Ätiologie und Risikofaktoren in Kapitel 3.
* `prompts/` – Vorlage‑Prompts für Planner, Auditor, Executor, Verifier und eine JSON‑Datei mit Wortzielvorgaben pro Kapitel.
* `.vscode/settings.json` – Aktiviert die Verwendung der Instructions‑Files in VS Code/GitHub Copilot Chat.

## Verwendung

1. **Integration**: Kopiere den Inhalt dieses Verzeichnisses in das Wurzelverzeichnis deines Projekts. Die Ordner `.github`, `.vscode` und `prompts` sollten sich auf derselben Ebene wie das `manuscript`‑Verzeichnis befinden.
2. **Aktivierung**: Stelle in VS Code sicher, dass die Einstellung `github.copilot.chat.codeGeneration.useInstructionFiles` auf `true` gesetzt ist (bereits in dieser Vorlage enthalten).
3. **Chat‑Konfiguration**: In Copilot Chat kannst du gezielt einzelne Instructions anhängen (Configure Chat → Instructions) oder die automatische Anwendung über die `applyTo`‑Muster nutzen.
4. **Kapitelweise Arbeit**: Befolge die Workflows Planner → Auditor → Executor → Verifier. Nutze die Prompts aus dem `prompts`‑Ordner als Startpunkt für deine Chat‑Interaktionen.
5. **Weitere Anpassungen**: Passe die Zielwortzahlen in `chapter_word_targets.json` oder die `applyTo`‑Filter an deine spezifischen Bedürfnisse an. Erstelle bei Bedarf weitere `sections`‑Files, um besonders komplexe Abschnitte gesondert zu steuern.