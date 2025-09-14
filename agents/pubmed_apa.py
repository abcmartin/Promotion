from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Citation:
    apa7: str
    doi: Optional[str]
    pmid: Optional[str]
    impact_factor: Optional[float]


def format_apa7(author: str, year: int, title: str, journal: str, volume: str, pages: str, doi: Optional[str]) -> str:
    base = f"{author} ({year}). {title}. {journal}, {volume}, {pages}."
    if doi:
        return f"{base} https://doi.org/{doi.split('/')[-2]}/{doi.split('/')[-1]}" if doi.startswith("http") else f"{base} https://doi.org/{doi}"
    return base


def lookup_by_pmid(pmid: str) -> Citation:
    # Stub: returns a placeholder structure. Real implementation would call Entrez.
    return Citation(
        apa7=f"Autor, A. (2020). Beispieltitel. Journal, 10(1), 1–10. https://doi.org/10.1000/example",
        doi="10.1000/example",
        pmid=pmid,
        impact_factor=None,
    )

