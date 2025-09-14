from __future__ import annotations

from typing import Any, Dict, Optional

try:
    from Bio import Entrez
except Exception:  # pragma: no cover - optional in dev
    Entrez = None  # type: ignore


def set_entrez_credentials(email: str, api_key: Optional[str] = None) -> None:
    if Entrez is None:
        return
    Entrez.email = email
    if api_key:
        Entrez.api_key = api_key


def fetch_pubmed_record(pmid: str) -> Dict[str, Any]:
    if Entrez is None:
        return {"pmid": pmid, "error": "Entrez nicht verfgbar"}
    handle = Entrez.efetch(db="pubmed", id=pmid, rettype="medline", retmode="text")
    data = handle.read()
    handle.close()
    return {"pmid": pmid, "raw": data}


def format_apa_stub(metadata: Dict[str, Any]) -> str:
    # Minimaler Platzhalter, bis vollwertiges Mapping ausgebaut wird
    pmid = metadata.get("pmid")
    title = metadata.get("title", "[Titel unbekannt]")
    journal = metadata.get("journal", "[Journal]")
    year = metadata.get("year", "n. d.")
    authors = metadata.get("authors", "[Autoren]")
    return f"{authors} ({year}). {title}. {journal}. PMID:{pmid}"

