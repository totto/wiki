"""
MkDocs hook: auto-inject the 3 most recent blog posts into the homepage.

Replaces the static ## Recent writing section in index.md with cards
generated from the actual most recent posts at build time.
This prevents the homepage from going stale as new posts are published.
"""
from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

N_POSTS = 3
ICONS = [
    ":material-book-open-variant:",
    ":material-brain:",
    ":material-chart-bar:",
]

_POSTS_DIR: Path | None = None


def _posts_dir(config) -> Path:
    global _POSTS_DIR
    if _POSTS_DIR is None:
        _POSTS_DIR = Path(config["docs_dir"]) / "blog" / "posts"
    return _POSTS_DIR


def _parse_post(path: Path) -> dict | None:
    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        return None

    # Require frontmatter
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not m:
        return None
    fm = m.group(1)

    # Skip drafts and noindex posts
    if re.search(r"^draft:\s*true", fm, re.MULTILINE | re.IGNORECASE):
        return None
    if re.search(r"^noindex:\s*true", fm, re.MULTILINE | re.IGNORECASE):
        return None

    # Extract date
    dm = re.search(r"^date:\s*(\S+)", fm, re.MULTILINE)
    if not dm:
        return None
    date_str = dm.group(1).split("T")[0]  # strip time component if present
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None

    # Extract description from frontmatter
    desc_m = re.search(r'^description:\s*"(.*?)"', fm, re.MULTILINE | re.DOTALL)
    if not desc_m:
        desc_m = re.search(r"^description:\s*'(.*?)'", fm, re.MULTILINE | re.DOTALL)
    description = desc_m.group(1).strip() if desc_m else ""

    # Extract H1 title from post body
    body = content[m.end():]
    title_m = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    if not title_m:
        return None
    title = title_m.group(1).strip()

    # Build URL slug from title (matches MkDocs Material blog slugification)
    slug = re.sub(r"[^\w\s-]", "", title.lower())
    slug = re.sub(r"[\s_]+", "-", slug).strip("-")
    url = f"blog/{date.year:04d}/{date.month:02d}/{date.day:02d}/{slug}/"

    return {
        "date": date,
        "date_display": date.strftime("%B %-d, %Y"),
        "title": title,
        "description": description,
        "url": url,
    }


def _recent_posts(config) -> list[dict]:
    posts = []
    for path in _posts_dir(config).glob("*.md"):
        post = _parse_post(path)
        if post:
            posts.append(post)
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts[:N_POSTS]


def _cards_markdown(posts: list[dict]) -> str:
    lines = [
        "## Recent writing",
        "",
        '<div class="grid cards" markdown>',
        "",
    ]
    for i, post in enumerate(posts):
        icon = ICONS[i] if i < len(ICONS) else ":material-file-document:"
        lines.append(f'-   {icon}{{ .card-icon }} **[{post["title"]}]({post["url"]})**')
        lines.append("")
        lines.append("    ---")
        lines.append("")
        if post["description"]:
            lines.append(f'    {post["description"]}')
            lines.append("")
        lines.append(f'    <span class="card-meta">{post["date_display"]}</span>')
        lines.append("")
    lines += [
        "</div>",
        "",
        '[:octicons-arrow-right-24: All posts](blog/index.md)',
    ]
    return "\n".join(lines)


def on_page_markdown(markdown, page, config, **kwargs):
    """Replace ## Recent writing section in index.md with dynamic cards."""
    if page.file.src_path != "index.md":
        return markdown

    posts = _recent_posts(config)
    if not posts:
        return markdown

    new_section = _cards_markdown(posts)

    # Replace from ## Recent writing up to (but not including) the next --- separator
    updated = re.sub(
        r"## Recent writing\n.*?(?=\n---\n)",
        new_section + "\n",
        markdown,
        flags=re.DOTALL,
    )
    return updated
