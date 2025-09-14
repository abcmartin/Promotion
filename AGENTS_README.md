## Multi-Agenten-CLI fr Dissertation-Optimierung

Kurzanleitung:

- Chunking:
  ```bash
  python -m agents.cli chunk --input-dir /workspace/manuscript --output-dir /workspace/.agent
  ```
- Plan aus YAML:
  ```bash
  python -m agents.cli plan --planner-yaml /workspace/planner_output.yaml --output /workspace/.agent/plan.json
  ```
- Audit der Chunks:
  ```bash
  python -m agents.cli audit --chunks /workspace/.agent/chunks.json --output /workspace/.agent/audit.json
  ```
- Verifikation (Wortziele, einfache APA-Heuristiken):
  ```bash
  python -m agents.cli verify --manuscript-dir /workspace/manuscript \
    --targets /workspace/prompts/chapter_word_targets.json \
    --output /workspace/.agent/verify.json
  ```

Hinweise:
- Die Executor-Funktionalitt erzeugt zunhst nur Vorschle/Diffs (dry-run). Aktive Edits knnen nach Review angewendet werden.
- Logs/JSON-Ausgaben landen in `/workspace/.agent/`.
