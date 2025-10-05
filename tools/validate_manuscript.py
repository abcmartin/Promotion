#!/usr/bin/env python3
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT_DIR = ROOT / 'manuscript'
BIB_DIR = ROOT / 'context' / 'Referenzen'

WORD_TARGETS = {
    # filename -> list of (section_header_regex, target, tol)
    '1_abstract.md': [
        (r'^##\s+Kurzfassung\s*$', 275, 50),
        (r'^##\s+Abstract\s*$', 275, 50),
    ],
}

DOI_PATTERN = re.compile(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.I)
APA_URL_PATTERN = re.compile(r"https?://doi\.org/10\.", re.I)
ACCEPTABLE_URL_PATTERNS = [
    re.compile(r"ncbi\.nlm\.nih\.gov/pubmed", re.I),
    re.compile(r"books\.google", re.I),
    re.compile(r"onlinelibrary\.wiley\.com/doi", re.I),
    re.compile(r"acsjournals\.onlinelibrary\.wiley\.com/doi", re.I),
    re.compile(r"nejm\.org/doi", re.I),
    re.compile(r"tandfonline\.com/doi", re.I),
    re.compile(r"link\.springer\.com", re.I),
    re.compile(r"nature\.com/articles", re.I),
    re.compile(r"science\.org/doi", re.I),
]


def count_words(text: str) -> int:
    words = re.findall(r"\b\w+\b", text)
    return len(words)


def split_sections(text: str, headers: list[str]):
    # returns dict header->section_text by regex header list (order matters)
    indices = []
    for pattern in headers:
        m = re.search(pattern, text, re.M)
        if m:
            indices.append((m.start(), pattern))
    indices.sort()
    sections = {}
    for i, (start, pattern) in enumerate(indices):
        end = indices[i + 1][0] if i + 1 < len(indices) else len(text)
        sections[pattern] = text[start:end]
    return sections


def validate_word_counts():
    results = []
    for fname, specs in WORD_TARGETS.items():
        fpath = MANUSCRIPT_DIR / fname
        if not fpath.exists():
            results.append((fname, 'missing'))
            continue
        text = fpath.read_text(encoding='utf-8', errors='ignore')
        headers = [pat for pat, _, _ in specs]
        sections = split_sections(text, headers)
        for pat, target, tol in specs:
            sec = sections.get(pat, '')
            n = count_words(sec)
            ok = (n != 0) and (abs(n - target) <= tol)
            results.append((fname, pat, n, target, tol, ok))
    return results


def extract_dois_from_text(text: str):
    return set(DOI_PATTERN.findall(text))


def normalize_doi(doi: str) -> str:
    s = doi.strip().lower()
    s = re.sub(r"[)\].,;]+$", "", s)
    return s


def scan_references_for_doi():
    dois = set()
    for bib in BIB_DIR.glob('*.bib'):
        try:
            content = bib.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        for m in re.finditer(r"doi\s*=\s*[{\"]\s*([^}\"\s]+)\s*", content, re.I):
            dois.add(normalize_doi(m.group(1)))
    return dois


def validate_doi_presence():
    # Check that each reference URL contains a DOI resolver or raw DOI mention
    ref_file = MANUSCRIPT_DIR / '8_references.md'
    if not ref_file.exists():
        return {'status': 'missing_references'}
    text = ref_file.read_text(encoding='utf-8', errors='ignore')
    lines = [ln for ln in text.splitlines() if ln.strip()]
    # simple heuristic: lines that look like references should contain a DOI
    issues = []
    for i, ln in enumerate(lines, 1):
        if re.search(r"\*\w+\*", ln) or re.search(r"\(\d{4}\)", ln):
            has_resolver = bool(
                DOI_PATTERN.search(ln)
                or APA_URL_PATTERN.search(ln)
                or any(p.search(ln) for p in ACCEPTABLE_URL_PATTERNS)
            )
            if not has_resolver:
                issues.append((i, ln[:200]))
    bib_dois = scan_references_for_doi()
    mentioned_dois = {normalize_doi(d) for d in extract_dois_from_text(text)}
    missing_in_bib = [d for d in sorted(mentioned_dois) if d not in bib_dois]
    return {
        'lines_missing_doi': issues,
        'missing_in_bib': missing_in_bib,
        'bib_files': sorted(str(p) for p in BIB_DIR.glob('*.bib')),
    }


def crossref_toc():
    toc = MANUSCRIPT_DIR / '2_tabel_of_content.md'
    if not toc.exists():
        return {'status': 'missing_toc'}
    text = toc.read_text(encoding='utf-8', errors='ignore')
    anchors = re.findall(r"\(#([^)]+)\)", text)
    files = {p.name: p for p in MANUSCRIPT_DIR.glob('*.md')}
    # crude check: anchor exists as a corresponding H1/H2 slug in any file
    def sluggify(s: str) -> str:
        s = s.lower()
        s = re.sub(r"[^a-z0-9\- ]+", '', s)
        s = s.replace(' ', '-')
        return s
    problems = []
    for anchor in set(anchors):
        found = False
        for p in files.values():
            t = p.read_text(encoding='utf-8', errors='ignore')
            for hdr in re.findall(r"^#{1,6}\s+(.+)$", t, re.M):
                if sluggify(hdr) == anchor:
                    found = True
                    break
            if found:
                break
        if not found:
            problems.append(anchor)
    return {'unresolved_anchors': problems}


def main():
    wc = validate_word_counts()
    doi = validate_doi_presence()
    xref = crossref_toc()

    print('WORD_COUNTS')
    for item in wc:
        print(item)
    print('\nDOI_VALIDATION')
    print(doi)
    print('\nTOC_CROSSREF')
    print(xref)


if __name__ == '__main__':
    sys.exit(main())
