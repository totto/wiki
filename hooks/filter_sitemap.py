"""
MkDocs hook: remove noindex pages from sitemap.xml

Pages that receive <meta name="robots" content="noindex"> are excluded
from the generated sitemap to avoid wasting crawl budget on thin pages.
Keep the NOINDEX_PREFIXES list in sync with overrides/main.html.
"""

import os
import re

NOINDEX_PREFIXES = [
    "blog/archive/",
    "blog/category/",
    "blog/2026/page/",
    "blog/2025/page/",
    "blog/page/",
    "tags/",
    "linkedin/",
]


def _is_noindex(loc: str, site_url: str) -> bool:
    path = loc.replace(site_url, "").lstrip("/")
    return any(path.startswith(p) for p in NOINDEX_PREFIXES)


def on_post_build(config, **kwargs):
    sitemap_path = os.path.join(config["site_dir"], "sitemap.xml")
    if not os.path.exists(sitemap_path):
        return

    with open(sitemap_path, "r", encoding="utf-8") as f:
        content = f.read()

    site_url = config.get("site_url", "")

    def keep_block(match):
        block = match.group(0)
        loc_match = re.search(r"<loc>(.*?)</loc>", block)
        if loc_match and _is_noindex(loc_match.group(1), site_url):
            return ""
        return block

    filtered = re.sub(r"<url>.*?</url>", keep_block, content, flags=re.DOTALL)
    filtered = re.sub(r"\n{3,}", "\n\n", filtered)

    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(filtered)
