"""
MkDocs hook: series navigation.

Reads `series:` frontmatter, builds a registry of all series posts sorted by
date (full datetime for same-day ordering), and appends a prev/next admonition
to each post that belongs to a series.
"""

import re
import yaml
from pathlib import Path

_registry = None  # {series_name: [{date, date_sort, title, url, file}]} sorted by date


def _slugify(title: str) -> str:
    s = title.lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s


def _build_registry(docs_dir: str) -> dict:
    global _registry
    if _registry is not None:
        return _registry
    _registry = {}
    for md_file in sorted(Path(docs_dir).glob("blog/posts/*.md")):
        content = md_file.read_text(encoding="utf-8")
        if not content.startswith("---"):
            continue
        try:
            end = content.index("\n---", 3)
            fm = yaml.safe_load(content[3:end])
        except Exception:
            continue
        if not fm or "series" not in fm:
            continue
        series = fm["series"]
        date_raw = fm.get("date", "")
        date_sort = str(date_raw)        # full datetime string for sorting
        date_ymd = date_sort[:10]        # YYYY-MM-DD for URL construction
        body = content[end + 4:]
        m = re.search(r"^# (.+)$", body, re.MULTILINE)
        title = m.group(1).strip() if m else md_file.stem
        d = date_ymd.split("-")
        url = f"/blog/{d[0]}/{d[1]}/{d[2]}/{_slugify(title)}/"
        _registry.setdefault(series, []).append(
            {
                "date_sort": date_sort,
                "date": date_ymd,
                "title": title,
                "url": url,
                "file": md_file.name,
            }
        )
    for s in _registry:
        _registry[s].sort(key=lambda x: x["date_sort"])
    return _registry


def on_page_markdown(markdown, page, config, files):
    series_name = page.meta.get("series")
    if not series_name:
        return markdown
    registry = _build_registry(config["docs_dir"])
    posts = registry.get(series_name, [])
    if len(posts) < 2:
        return markdown
    filename = Path(page.file.src_path).name
    idx = next((i for i, p in enumerate(posts) if p["file"] == filename), None)
    if idx is None:
        return markdown
    total = len(posts)
    pos = idx + 1
    prev_link = (
        f'[← {posts[idx - 1]["title"]}]({posts[idx - 1]["url"]})'
        if idx > 0
        else ""
    )
    next_link = (
        f'[{posts[idx + 1]["title"]} →]({posts[idx + 1]["url"]})'
        if idx < total - 1
        else ""
    )
    center = f"Part {pos} of {total}"
    parts = [x for x in [prev_link, center, next_link] if x]
    nav = (
        f'\n\n---\n\n!!! info "Series: {series_name}"\n'
        f'    {" &ensp;·&ensp; ".join(parts)}\n'
    )
    return markdown + nav
