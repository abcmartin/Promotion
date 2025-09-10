from __future__ import annotations

import re
from typing import Dict, List


HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")


def chunk_markdown_content(
    content: str,
    source_path: str,
    min_heading_level: int = 2,
) -> List[Dict]:
    lines = content.splitlines()
    headings: List[tuple[int, int, str]] = []
    for idx, line in enumerate(lines):
        m = HEADING_RE.match(line)
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            headings.append((idx, level, title))

    chunk_starts: List[int] = []
    titles: List[str] = []
    levels: List[int] = []

    for i, (idx, level, title) in enumerate(headings):
        if level <= min_heading_level:
            chunk_starts.append(idx)
            titles.append(title)
            levels.append(level)

    chunks: List[Dict] = []
    if not chunk_starts:
        # Fallback: alles als ein Chunk
        title = _derive_title_fallback(lines, source_path)
        chunks.append(
            _build_chunk(
                source_path=source_path,
                title=title,
                level=min_heading_level,
                start_line=1,
                end_line=len(lines),
                lines=lines,
            )
        )
        return chunks

    for i, start_idx in enumerate(chunk_starts):
        end_idx = (chunk_starts[i + 1] - 1) if (i + 1) < len(chunk_starts) else (len(lines) - 1)
        title = titles[i]
        level = levels[i]
        chunks.append(
            _build_chunk(
                source_path=source_path,
                title=title,
                level=level,
                start_line=start_idx + 1,
                end_line=end_idx + 1,
                lines=lines[start_idx : end_idx + 1],
            )
        )

    return chunks


def _derive_title_fallback(lines: List[str], source_path: str) -> str:
    for line in lines[:5]:
        m = HEADING_RE.match(line)
        if m:
            return m.group(2).strip()
    # Dateiname als Titelersatz
    return source_path.split("/")[-1]


def _build_chunk(
    *,
    source_path: str,
    title: str,
    level: int,
    start_line: int,
    end_line: int,
    lines: List[str],
) -> Dict:
    content = "\n".join(lines)
    chunk_id = f"{source_path}#{start_line}-{end_line}"
    return {
        "id": chunk_id,
        "source_path": source_path,
        "title": title,
        "level": level,
        "start_line": start_line,
        "end_line": end_line,
        "content": content,
    }

