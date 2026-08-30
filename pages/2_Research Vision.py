"""
Research Vision page for a Streamlit multipage app.

Files in your repo:
- This file:        pages/2_Research Vision.py
- Content folder:   research_vision_content/   (repo ROOT)

The flow diagrams from the Word document lost their alignment during
conversion, so this page detects those diagram regions in the markdown
and renders them as proper centered flow diagrams (boxes + arrows).
"""

import re
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="Research Vision", page_icon="🔬", layout="wide")

# ================================================================ styling
st.markdown(
    """
    <style>
    .block-container { max-width: 1000px; padding-top: 2.5rem; }
    [data-testid="stMarkdownContainer"] p {
        text-align: justify; line-height: 1.75; font-size: 1.02rem;
    }

    /* hero header */
    .rv-hero { text-align: center; padding: 0.5rem 0 1.2rem 0; }
    .rv-hero h1 { font-size: 2.6rem; letter-spacing: 0.5px; margin-bottom: 0.4rem; }
    .rv-hero .rv-sub { font-size: 1.15rem; font-weight: 600; opacity: 0.85; margin-bottom: 0.6rem; }
    .rv-hero .rv-tag { font-style: italic; opacity: 0.65; font-size: 1rem;
                       max-width: 640px; margin: 0 auto; }

    /* headings inside sections */
    [data-testid="stExpander"] h2 {
        font-size: 1.55rem; text-align: center;
        padding-bottom: 0.6rem; margin-bottom: 0.8rem;
        border-bottom: 2px solid rgba(99, 110, 250, 0.45);
    }
    [data-testid="stExpander"] h4 {
        font-size: 1.15rem; margin-top: 1.6rem; color: #8ab4f8;
        border-left: 4px solid #636efa; padding-left: 0.6rem;
    }

    /* taglines & bold statements */
    [data-testid="stExpander"] blockquote {
        border-left: 4px solid #f0b849;
        background: rgba(240, 184, 73, 0.07);
        padding: 0.7rem 1rem; border-radius: 0 8px 8px 0; margin: 1rem 0;
    }
    [data-testid="stExpander"] blockquote p { text-align: center; margin: 0; }

    /* clickable section rows */
    [data-testid="stExpander"] {
        border: 1px solid rgba(255,255,255,0.10); border-radius: 12px;
        margin-bottom: 0.65rem; background: rgba(255,255,255,0.02);
    }
    [data-testid="stExpander"] summary { font-size: 1.06rem; padding: 0.85rem 1rem; }
    [data-testid="stExpander"] summary:hover { color: #8ab4f8; }

    button[data-baseweb="tab"] { font-weight: 600; }
    ul li { line-height: 1.7; margin-bottom: 0.3rem; }

    /* ---------- flow diagrams ---------- */
    .rv-flow {
        display: flex; flex-direction: column; align-items: center;
        gap: 0.15rem; margin: 1.4rem auto; padding: 1.2rem 0.8rem;
        border: 1px solid rgba(138, 180, 248, 0.25); border-radius: 14px;
        background: rgba(99, 110, 250, 0.05); max-width: 760px;
    }
    .rv-node {
        display: inline-block; padding: 0.45rem 1.1rem;
        border: 1.5px solid #636efa; border-radius: 10px;
        background: rgba(99, 110, 250, 0.14);
        font-weight: 600; font-size: 0.95rem; text-align: center;
        max-width: 560px;
    }
    .rv-branchrow {
        display: flex; flex-wrap: wrap; justify-content: center;
        gap: 0.7rem; align-items: center;
    }
    .rv-arrow { color: #8ab4f8; font-size: 1rem; line-height: 1; padding: 0.1rem 0; }
    .rv-harrow { color: #8ab4f8; font-weight: 700; padding: 0 0.3rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ================================================== diagram detection/render
_CONN_CHARS = set("│▼↓─┌┐└┘├┤┬┴┼═→←◄►▲↑ ")


def _is_connector(s: str) -> bool:
    s = s.strip()
    return bool(s) and all(c in _CONN_CHARS for c in s)


def _is_mixed_connector(s: str) -> bool:
    s = s.strip()
    return bool(re.search(r"[◄►←→]", s)) and bool(re.search(r"[A-Za-z]", s))


def _is_nodeish(s: str) -> bool:
    s = s.strip()
    if not s or len(s) > 70:
        return False
    if s[0] in "#>-*|`":
        return False
    if re.match(r"^\d+\.", s):
        return False
    return True


def _clean(label: str) -> str:
    return label.strip().strip("*").strip()


def _emit_row(labels) -> str:
    boxes = "".join(f'<div class="rv-node">{l}</div>' for l in labels)
    return f'<div class="rv-branchrow">{boxes}</div>'


def _region_to_html(units) -> str:
    rows, pending_k, last_arrow = [], None, False
    for u in units:
        s = u.strip()
        if _is_mixed_connector(s):
            labels = [w for w in re.split(r"[\s│─┼◄►←→]+", s) if re.search(r"[A-Za-z]", w)]
            if labels:
                rows.append(
                    '<div class="rv-branchrow">'
                    + '<span class="rv-harrow">⟷</span>'.join(
                        f'<div class="rv-node">{_clean(l)}</div>' for l in labels
                    )
                    + "</div>"
                )
                last_arrow = False
            pending_k = None
        elif _is_connector(s):
            k = s.count("│")
            if k > 1:
                pending_k = k
            elif any(c in s for c in "└┘"):
                pending_k = None
                if not last_arrow:
                    rows.append('<div class="rv-arrow">▼</div>')
                    last_arrow = True
            else:  # │ ▼ ↓ ┌ ┐ ┬ ┼ …
                if not last_arrow:
                    rows.append('<div class="rv-arrow">▼</div>')
                    last_arrow = True
        else:  # node text
            label = _clean(s)
            if pending_k and pending_k > 1:
                words = label.split()
                if len(words) >= pending_k:
                    per, extra = divmod(len(words), pending_k)
                    parts, idx = [], 0
                    for b in range(pending_k):
                        take = per + (1 if b < extra else 0)
                        parts.append(" ".join(words[idx: idx + take]))
                        idx += take
                    rows.append(_emit_row(parts))
                else:
                    rows.append(_emit_row([label]))
                pending_k = None
            else:
                rows.append(_emit_row([label]))
            last_arrow = False
    return '<div class="rv-flow">' + "".join(rows) + "</div>"


def _split_content(text: str):
    """Split markdown into ('md', chunk) and ('diagram', html) segments."""
    lines = text.split("\n")
    idx = [i for i, l in enumerate(lines) if l.strip()]
    units = [lines[i].strip() for i in idx]
    in_region = [False] * len(lines)

    u = 0
    while u < len(units):
        if _is_connector(units[u]) or _is_mixed_connector(units[u]):
            start = end = u
            j = u
            while j < len(units):
                s = units[j]
                if _is_connector(s) or _is_mixed_connector(s):
                    end = j
                    j += 1
                elif _is_nodeish(s) and j + 1 < len(units) and (
                    _is_connector(units[j + 1]) or _is_mixed_connector(units[j + 1])
                ):
                    end = j
                    j += 1
                elif _is_nodeish(s) and j == end + 1:  # trailing node
                    end = j
                    j += 1
                    break
                else:
                    break
            if start > 0 and _is_nodeish(units[start - 1]) and not in_region[idx[start - 1]]:
                start -= 1
            for k in range(start, end + 1):
                in_region[idx[k]] = True
            u = end + 1
        else:
            u += 1

    segs, buf, i = [], [], 0
    while i < len(lines):
        if lines[i].strip() and in_region[i]:
            if buf:
                segs.append(("md", "\n".join(buf)))
                buf = []
            region_units = []
            while i < len(lines) and (not lines[i].strip() or in_region[i]):
                if lines[i].strip():
                    region_units.append(lines[i].strip())
                if (
                    not lines[i].strip()
                    and i + 1 < len(lines)
                    and lines[i + 1].strip()
                    and not in_region[i + 1]
                ):
                    break
                i += 1
            segs.append(("diagram", _region_to_html(region_units)))
        else:
            buf.append(lines[i])
            i += 1
    if buf:
        segs.append(("md", "\n".join(buf)))
    return segs


def render_content(text: str) -> None:
    for kind, chunk in _split_content(text):
        if kind == "diagram":
            st.markdown(chunk, unsafe_allow_html=True)
        else:
            st.markdown(chunk)


# ================================================================ loading
_here = Path(__file__).resolve().parent
CONTENT_DIR = _here.parent / "research_vision_content"
if not CONTENT_DIR.exists():
    CONTENT_DIR = _here / "research_vision_content"


@st.cache_data
def _read(path_str: str) -> str:
    return Path(path_str).read_text(encoding="utf-8")


def load(name: str) -> str:
    path = CONTENT_DIR / name
    if not path.exists():
        return f"*Content file not found: `{name}` (looked in `{CONTENT_DIR}`)*"
    return _read(str(path))


# ================================================================ header
st.markdown(
    """
    <div class="rv-hero">
      <h1>🔬 Research Vision</h1>
      <div class="rv-sub">Understanding Organization, Intelligence, Discovery
      and the Future of Science</div>
      <div class="rv-tag">“Exploring the universal principles that organize life,
      intelligence, scientific discovery, and artificial intelligence.”</div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.divider()

# ================================================================ sections
PROGRAMS = [
    ("Program I — Indian Knowledge Systems and the Future of Science", "p3_program1.md"),
    ("Program II — Thinking Machines, Ancient Minds", "p3_program2.md"),
    ("Program III — Cognitive Ecology of Scientific Discovery", "p3_program3.md"),
    ("Program IV — Toward a Unified Science", "p3_program4.md"),
    ("Program V — Frontiers of Scientific Inquiry", "p3_program5.md"),
    ("Program VI — Future of Humanity", "p3_program6.md"),
]

CHAPTERS = [
    ("Chapters 1–2 · The Framework & the Research Cube", "p4_ch1_2.md"),
    ("Chapter 3 · The Universal Scientific Workflow", "p4_ch3.md"),
    ("Chapter 4 · The Scientific Coordinate System", "p4_ch4.md"),
    ("Chapter 5 · The Universal Research Matrix", "p4_ch5.md"),
]

SECTIONS = [
    ("📖  Part 1 · Research Philosophy", "part1_philosophy.md", None),
    ("🌐  Part 2 · The Grand Research Ecosystem", "part2_ecosystem.md", None),
    ("🧭  Part 3 · The Six Grand Research Programs", "p3_intro.md", PROGRAMS),
    ("🧩  Part 4 · The Universal Research Framework", None, CHAPTERS),
    ("🗺️  Part 5 · Research Roadmap — Evolution of the Ecosystem", "part5_roadmap.md", None),
    ("🔬  Part 6 · Current Research — Research Portfolio", "part6_current_research.md", None),
    ("📚  Part 7 · Publications and Scholarly Contributions", "part7_publications.md", None),
    ("🧰  Part 8 · Resources", "part8_resources.md", None),
    ("🤝  Part 9 · Collaboration", "part9_collaboration.md", None),
]

for label, intro_file, tabs in SECTIONS:
    with st.expander(f"**{label}**", expanded=False):
        if intro_file:
            render_content(load(intro_file))
        if tabs:
            st.markdown("")
            tab_objs = st.tabs([t[0].split("·")[0].split("—")[0].strip() for t in tabs])
            for tab, (tab_label, fname) in zip(tab_objs, tabs):
                with tab:
                    render_content(load(fname))

st.divider()
st.caption(
    "Science is one of humanity's greatest collaborative enterprises. "
    "Each generation inherits questions from the past, contributes new ideas in the "
    "present, and leaves foundations for future investigators."
)
