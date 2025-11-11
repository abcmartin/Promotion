# Manuskript-Editor

Dieses Verzeichnis ist für die Integration von https://github.com/abcmartin/manubot-ai-editor.git vorgesehen. Der eigentliche Editor-Code sollte aus dem genannten Repository übernommen und hier eingebunden werden.

Start (Beispiel):

```bash
cd editor
npm install
npm run dev
```

Konfigurieren Sie den Editor so, dass er über einen konfigurierbaren Pfad (z. B. Umgebungsvariable `MANUSCRIPT_CONTENT_DIR`) auf die Markdown-Dateien im Verzeichnis `content/` zugreifen kann.
