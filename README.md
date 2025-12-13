# CD44_Manus — Dissertation Optimization Repository

Dieses Repository bündelt:
- Build-/Manubot-Struktur aus: https://github.com/abcmartin/rootstock.git
- Manuskriptquellen aus: https://github.com/abcmartin/manuscript/tree/main/manuscript
- Editor-Komponente aus: https://github.com/abcmartin/manubot-ai-editor.git

## Was kann das Repository?

Dieses Repository bietet ein **vollständiges System zur wissenschaftlichen Optimierung** einer medizinischen Dissertation über "Prognostisches Potential von CD44 als Tumorstammzellmarker für die kombinierte Radiochemotherapie des lokal fortgeschrittenen Kopf-Hals-Plattenepithelkarzinoms".

### Hauptfunktionen

#### 1. **Agentenbasierter Workflow** (`agents/`)
Ein Multi-Agenten-System zur systematischen Manuskriptoptimierung:

- **Planner** — Analysiert Abschnitte und erstellt konkrete Arbeitspakete mit Zielen und Akzeptanzkriterien
- **Researcher** — Sucht und validiert wissenschaftliche Literatur (PubMed/Web of Science, Impact Factor ≥ 5)
- **Auditor** — Prüft Logik, Methodik, Statistik und APA-7-Konformität
- **Executor** — Schreibt optimierte Fließtexte mit präziser medizinischer Terminologie
- **Verifier** — Finale Qualitätskontrolle (Formatierung, Terminologie, Redundanzen, Plagiatsprüfung)
- **Reporter** — Erstellt Zusammenfassungen und Änderungsprotokolle

#### 2. **Manuskript-Validierung** (`tools/`)
Automatische Prüfung von:
- Wortzielkonformität (±1% Toleranz)
- DOI/PubMed-Link-Präsenz in Referenzen
- Inhaltsverzeichnis-Anker-Konsistenz
- APA-7-Zitationskonformität

#### 3. **Build-System** (`Makefile`)
- HTML-Generierung des Manuskripts
- PDF-Erzeugung (Pandoc/LaTeX/Manubot)
- Clean-Befehle für Artefakte

#### 4. **Strukturierte Prompts** (`.github/instructions/`)
Detaillierte Anweisungen für jeden Dissertationsabschnitt:
- Kapitelspezifische Guidelines (Abstract, Hintergrund, Methoden, Ergebnisse, Diskussion)
- Stilrichtlinien (Deutsch, APA-7, Markdown, Tabellen/Abbildungen)
- Rollenspezifische Agent-Prompts

## Voraussetzungen
- git
- Python 3.8+ (für Agenten und Validierung)
- optional: Docker
- optional: PyYAML (für Playbook-Unterstützung)
- optional: Node.js (für Editor-Komponente)

## Schnellstart

### 1. Repository klonen
```bash
git clone https://github.com/abcmartin/Promotion.git
cd Promotion
```

### 2. Agenten-System verwenden

**Vollständiger Pipeline-Durchlauf für ein Kapitel:**
```bash
python -m agents run-all 5_material_methods
```

**Einzelne Schritte ausführen:**
```bash
# Planungsphase
python -m agents plan 5_material_methods

# Literaturrecherche
python -m agents research 5_material_methods

# Audit/Qualitätsprüfung
python -m agents audit 5_material_methods

# Textgenerierung
python -m agents execute 5_material_methods

# Verifikation
python -m agents verify 5_material_methods

# Bericht erstellen
python -m agents report 5_material_methods
```

**Verfügbare Kapitel-IDs:**
- `0_cover` — Deckblatt
- `1_abstract` — Abstract/Kurzfassung
- `2_tabel_of_content` — Inhaltsverzeichnis
- `3_background` — Hintergrund (Epidemiologie, Ätiologie, Pathogenese)
- `4_question` — Fragestellung & Hypothesen
- `5_material_methods` — Material & Methoden
- `6_results` — Ergebnisse
- `7_discussion_conclusion` — Diskussion & Schlussfolgerungen
- `8_references` — Literaturverzeichnis

### 3. Manuskript validieren
```bash
python tools/validate_manuscript.py
```

### 4. Manuskript bauen
```bash
# HTML-Version
make html

# PDF-Version
make pdf

# Aufräumen
make clean
```

### 5. Editor starten (optional)
Siehe `editor/README.md` für Details zur Editor-Komponente.

## Verzeichnisstruktur

```
├── agents/              # Multi-Agenten-Orchestrierung
│   ├── cli.py          # Kommandozeilen-Interface
│   ├── planner.py      # Planungs-Agent
│   ├── researcher.py   # Recherche-Agent
│   ├── auditor.py      # Audit-Agent
│   ├── executor.py     # Ausführungs-Agent
│   ├── verifier.py     # Verifikations-Agent
│   └── reporter.py     # Berichts-Agent
├── manuscript/          # Manuskript-Quellen (Markdown)
├── plans/              # Generierte Arbeitspläne
├── research/           # Recherche-Ergebnisse
├── audit/              # Audit-Berichte
├── drafts/             # Überarbeitete Entwürfe
├── verify/             # Verifikationsergebnisse
├── reports/            # Finale Berichte
├── tools/              # Validierungs- und Hilfswerkzeuge
├── prompts/            # Agent-Prompts
├── .github/instructions/ # Kapitel- und Stilrichtlinien
└── Makefile            # Build-Befehle
```

## Ausgaben

Das System generiert für jeden Abschnitt:
1. **Optimierter Fließtext** (`.md` oder `.docx`)
2. **Änderungsprotokoll** (`change_log.json`) mit:
   - Position der Änderung
   - Änderungstyp (rewrite/add/delete)
   - Wissenschaftliche Begründung
   - Alte und neue Textschnipsel
   - Wortanzahl vor/nach Änderung
   - Neu hinzugefügte Quellen (DOI/PMID)
3. **Qualitätsberichte** (JSON + Markdown)

## Qualitätsstandards

- **Literatur:** Impact Factor ≥ 5, DOI/PMID verpflichtend
- **Zitation:** APA-7-Format mit vollständigen Referenzen
- **Format:** DIN A4, Arial 11 pt, 1,5-facher Zeilenabstand
- **Wortziele:** Kapitelspezifisch mit ±1% Toleranz
- **Terminologie:** Konsistent (CD44, HNSCC, CSC, RCTx, HPV-Status)

## CI/CD

Die CI-Pipeline:
- Baut das Manuskript automatisch
- Validiert Formatierung und Referenzen
- Lädt HTML/PDF-Artefakte hoch

## Weiterführende Dokumentation

- Agent-System-Details: `.github/copilot-instructions.md`
- Kapitelrichtlinien: `.github/instructions/chapters/`
- Stilrichtlinien: `.github/instructions/`
- Beispiel-Playbook: `prompts/prompt_playbook.yaml`

## Lizenz

Siehe LICENSE-Datei im Repository.
