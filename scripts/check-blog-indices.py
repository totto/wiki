#!/usr/bin/env python3
"""Verify the hand-maintained blog indices still describe reality.

`docs/blog/series.md` and `docs/blog/topics.md` carry counts and links that nothing
regenerates. They were accurate when written and drifted silently afterwards: in July 2026
the Knowledge Context Protocol card still said "9 posts · February 2026" for a series that
had reached 50 posts across five months, and five of nine topic counts were low.

Nothing failed. Nothing warned. That is the failure mode worth a check of its own.

Run:  python3 scripts/check-blog-indices.py
Exits non-zero and prints every disagreement.
"""
from __future__ import annotations

import collections
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
POSTS = ROOT / "docs" / "blog" / "posts"
SERIES_MD = ROOT / "docs" / "blog" / "series.md"
TOPICS_MD = ROOT / "docs" / "blog" / "topics.md"

FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n", re.S)


def published():
    """Every published post's frontmatter, skipping drafts."""
    for path in sorted(POSTS.glob("*.md")):
        raw = path.read_text(encoding="utf-8")
        m = FRONTMATTER.match(raw)
        if not m:
            continue
        fm = m.group(1)
        if re.search(r"^draft:\s*true", fm, re.M):
            continue
        yield path, fm


def actual_series_counts() -> collections.Counter:
    counts = collections.Counter()
    for _, fm in published():
        m = re.search(r'^series:\s*"?([^"\n]+)"?', fm, re.M)
        if m:
            counts[m.group(1).strip()] += 1
    return counts


def actual_topic_counts() -> collections.Counter:
    counts = collections.Counter()
    for _, fm in published():
        m = re.search(r"^categories:\n((?:\s+-\s+.+\n)+)", fm, re.M)
        if not m:
            continue
        for line in m.group(1).strip().split("\n"):
            counts[line.strip("- ").strip()] += 1
    return counts


def check_series(problems: list[str]) -> None:
    """Each card's stated post count must match the posts declaring that series."""
    text = SERIES_MD.read_text(encoding="utf-8")
    counts = actual_series_counts()

    # A card is "-   :material-x: **Name**" followed later by "**N posts &nbsp;..."
    cards = re.findall(
        r"^-   :[\w-]+: \*\*(.+?)\*\*.*?^    \*\*(\d+) posts", text, re.S | re.M
    )
    if not cards:
        problems.append("series.md: no cards found — has the format changed?")
        return

    for name, stated in cards:
        real = counts.get(name)
        if real is None:
            problems.append(
                f"series.md: card {name!r} has no posts declaring `series: {name}`"
            )
        elif int(stated) != real:
            problems.append(
                f"series.md: {name!r} says {stated} posts, actually {real}"
            )

    carded = {name for name, _ in cards}
    for name, n in counts.items():
        # A single post is not a series; only flag real ones that lack a card.
        if name not in carded and n > 1:
            problems.append(f"series.md: no card for series {name!r} ({n} posts)")


def check_topics(problems: list[str]) -> None:
    """Each topic's stated post count must match the posts in that category."""
    text = TOPICS_MD.read_text(encoding="utf-8")
    counts = actual_topic_counts()
    # Slugs delete punctuation and turn spaces into hyphens, so "&" leaves a double
    # hyphen behind: "AI Agents & the Agentic Web" -> "ai-agents--the-agentic-web".
    def slugify(name: str) -> str:
        kept = "".join(c if (c.isalnum() or c in " -") else "" for c in name.lower())
        return kept.replace(" ", "-").strip("-")

    by_slug = {slugify(name): n for name, n in counts.items()}

    found = re.findall(r"(\d+) posts\]\(/blog/category/([^/]+)/\)", text)
    if not found:
        problems.append("topics.md: no category links found — has the format changed?")
        return

    for stated, slug in found:
        # Match the category whose slugified name equals this link's slug.
        real = by_slug.get(slug)
        if real is None:
            problems.append(f"topics.md: /blog/category/{slug}/ matches no category")
        elif int(stated) != real:
            problems.append(
                f"topics.md: /blog/category/{slug}/ says {stated} posts, actually {real}"
            )


def check_series_links(problems: list[str]) -> None:
    """Every /blog/ link in series.md must point at a date that has a published post.

    Exact slugs are deliberately not reconstructed here. mkdocs-material derives them from
    an explicit `slug:`, else the H1, else the filename, deleting punctuation along the
    way — so "llms.txt" becomes "llmstxt" and an em-dash leaves a double hyphen. A checker
    that guesses that would fail on its own cleverness. Verify slugs against a built
    sitemap when you need certainty; this catches the drift that actually happens, which is
    entries going missing or pointing at dates with no post.
    """
    dates = set()
    for path, fm in published():
        m = re.search(r"^date:\s*(\d{4})-(\d{2})-(\d{2})", fm, re.M)
        if m:
            dates.add("/".join(m.groups()))

    text = SERIES_MD.read_text(encoding="utf-8")
    for link in re.findall(r"\]\((/blog/(\d{4}/\d{2}/\d{2})/[^)]+)\)", text):
        if link[1] not in dates:
            problems.append(f"series.md: link points at a date with no post — {link[0]}")

    # A card claiming N posts should list N of them.
    for block in re.split(r"^-   :", text, flags=re.M)[1:]:
        nm = re.match(r"[\w-]+: \*\*(.+?)\*\*", block)
        cnt = re.search(r"^    \*\*(\d+) posts", block, re.M)
        if not (nm and cnt):
            continue
        listed = len(re.findall(r"^\s+\d+\. \[", block, re.M))
        if listed and listed != int(cnt.group(1)):
            problems.append(
                f"series.md: {nm.group(1)!r} states {cnt.group(1)} posts but lists {listed}"
            )


def main() -> int:
    problems: list[str] = []
    check_series(problems)
    check_topics(problems)
    check_series_links(problems)

    if problems:
        print(f"{len(problems)} problem(s) in the blog indices:\n")
        for p in problems:
            print(f"  - {p}")
        print("\nUpdate docs/blog/series.md / docs/blog/topics.md to match.")
        return 1

    print("blog indices agree with the posts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
