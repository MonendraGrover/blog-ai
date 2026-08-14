"""
Reads the blog catalogue straight off the filesystem.

Folder contract
---------------
static/blogs/
    categories.json                  optional — order, icons, blurbs
    01_Methylation-Biology/          folder name = category ("01_" prefix only sorts)
        meta.json                    optional — per-PDF title, summary, author, date, tags
        cpg-islands-in-rice.pdf      drop a PDF here and it appears on the site
        cpg-islands-in-rice.png      optional cover, same name as the PDF

Nothing else is required. A bare PDF with no metadata still shows up, using a
title derived from the filename and the file's own modified date.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path

import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
BLOGS_DIR = BASE_DIR / "static" / "blogs"
COVER_EXTS = (".png", ".jpg", ".jpeg", ".webp")
WORDS_PER_MINUTE = 220


@dataclass
class Post:
    slug: str
    title: str
    category: str
    path: Path
    summary: str = ""
    author: str = ""
    published: date = field(default_factory=date.today)
    tags: list[str] = field(default_factory=list)
    featured: bool = False
    cover: Path | None = None
    size_kb: int = 0
    pages: int | None = None

    @property
    def date_label(self) -> str:
        return self.published.strftime("%d %b %Y")

    @property
    def size_label(self) -> str:
        return f"{self.size_kb / 1024:.1f} MB" if self.size_kb >= 1024 else f"{self.size_kb} KB"

    @property
    def page_label(self) -> str:
        return f"{self.pages} pages" if self.pages else self.size_label

    def read_bytes(self) -> bytes:
        return self.path.read_bytes()


@dataclass
class Category:
    name: str
    slug: str
    icon: str = ""
    blurb: str = ""
    posts: list[Post] = field(default_factory=list)

    @property
    def label(self) -> str:
        return f"{self.icon} {self.name}".strip()


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def _pretty(stem: str) -> str:
    cleaned = re.sub(r"^\d+[_\-.\s]+", "", stem).replace("_", " ").replace("-", " ")
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned[:1].upper() + cleaned[1:]


def _parse_date(value, fallback: float) -> date:
    if isinstance(value, str):
        for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%d %b %Y", "%B %d, %Y"):
            try:
                return datetime.strptime(value.strip(), fmt).date()
            except ValueError:
                continue
    return datetime.fromtimestamp(fallback).date()


def _page_count(path: Path) -> int | None:
    """Cheap page count without pulling in a PDF dependency."""
    try:
        blob = path.read_bytes()
        hits = len(re.findall(rb"/Type\s*/Page[^s]", blob))
        return hits or None
    except Exception:
        return None


def _find_cover(pdf: Path) -> Path | None:
    for ext in COVER_EXTS:
        candidate = pdf.with_suffix(ext)
        if candidate.exists():
            return candidate
    return None


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # a typo in meta.json must never blank the site
        st.warning(f"Could not read {path.name}: {exc}. Falling back to filenames.")
        return {}


@st.cache_data(ttl=30, show_spinner=False)
def load_catalog() -> list[Category]:
    """Scan static/blogs and return categories in display order."""
    if not BLOGS_DIR.exists():
        return []

    settings = _read_json(BLOGS_DIR / "categories.json")
    order = [s.lower() for s in settings.get("order", [])]
    icons = {k.lower(): v for k, v in settings.get("icons", {}).items()}
    blurbs = {k.lower(): v for k, v in settings.get("descriptions", {}).items()}

    categories: list[Category] = []
    for folder in sorted(p for p in BLOGS_DIR.iterdir() if p.is_dir()):
        name = _pretty(folder.name)
        meta = _read_json(folder / "meta.json")
        posts: list[Post] = []

        for pdf in sorted(folder.glob("*.pdf")):
            entry = meta.get(pdf.name) or meta.get(pdf.stem) or {}
            stat = pdf.stat()
            posts.append(
                Post(
                    slug=slugify(f"{name}-{pdf.stem}"),
                    title=entry.get("title") or _pretty(pdf.stem),
                    category=name,
                    path=pdf,
                    summary=entry.get("summary", ""),
                    author=entry.get("author", ""),
                    published=_parse_date(entry.get("date"), stat.st_mtime),
                    tags=[t for t in entry.get("tags", []) if t],
                    featured=bool(entry.get("featured")),
                    cover=_find_cover(pdf),
                    size_kb=max(1, round(stat.st_size / 1024)),
                    pages=_page_count(pdf),
                )
            )

        if not posts:
            continue

        posts.sort(key=lambda p: p.published, reverse=True)
        categories.append(
            Category(
                name=name,
                slug=slugify(name),
                icon=icons.get(name.lower(), ""),
                blurb=blurbs.get(name.lower(), ""),
                posts=posts,
            )
        )

    if order:
        categories.sort(
            key=lambda c: order.index(c.name.lower()) if c.name.lower() in order else 999
        )
    return categories


def all_posts(categories: list[Category] | None = None) -> list[Post]:
    categories = categories if categories is not None else load_catalog()
    posts = [p for c in categories for p in c.posts]
    posts.sort(key=lambda p: p.published, reverse=True)
    return posts


def find_post(slug: str) -> Post | None:
    return next((p for p in all_posts() if p.slug == slug), None)


# ─────────────────────────────────────────────────────────────────────────────
# Inline PDF viewer
#
# Order of attempts:
#   1. st.pdf            — built into Streamlit >= 1.45, the cleanest option
#   2. streamlit-pdf-viewer — pdf.js component, works in every browser
#                             (pip install streamlit-pdf-viewer)
#   3. friendly fallback  — points the reader at the Download button
#
# The old base64 <object data="data:application/pdf..."> approach was removed:
# Chrome and Edge block PDFs loaded from data: URLs, which is why previews
# showed up blank.
# ─────────────────────────────────────────────────────────────────────────────
def render_pdf(post: Post, height: int = 820) -> None:
    """Inline viewer for a post's PDF."""
    # 1. Native viewer (Streamlit >= 1.45)
    if hasattr(st, "pdf"):
        try:
            st.pdf(str(post.path), height=height)
            return
        except Exception:
            pass

    # 2. pdf.js component — immune to the Chrome/Edge data-URL block
    try:
        from streamlit_pdf_viewer import pdf_viewer

        pdf_viewer(
            post.read_bytes(),
            height=height,
            key=f"pdfviewer_{post.slug}",
        )
        return
    except ImportError:
        pass
    except Exception:
        pass

    # 3. Last resort — tell the reader what to do instead of showing a blank box
    st.info(
        "Inline preview is not available here. "
        "Install it with `pip install streamlit-pdf-viewer` (or upgrade Streamlit "
        "to 1.45+), or use the **Download PDF** button above to read this blog."
    )
