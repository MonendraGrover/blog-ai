"""
Research Vision page for a Streamlit multipage app.

Location of files in your repo:
- This file:        pages/2_Research Vision.py
- Content folder:   research_vision_content/   (in the repo ROOT, replace the old files)

Each section appears as a clickable option top to bottom; clicking shows that part.
"""

from pathlib import Path
import streamlit as st

st.set_page_config(page_title="Research Vision", page_icon="🔬", layout="wide")

# ------------------------------------------------------------ styling
st.markdown(
    """
    <style>
    /* page width & typography */
    .block-container { max-width: 1000px; padding-top: 2.5rem; }
    [data-testid="stMarkdownContainer"] p {
        text-align: justify;
        line-height: 1.75;
        font-size: 1.02rem;
    }

    /* hero header */
    .rv-hero { text-align: center; padding: 0.5rem 0 1.2rem 0; }
    .rv-hero h1 {
        font-size: 2.6rem; letter-spacing: 0.5px; margin-bottom: 0.4rem;
    }
    .rv-hero .rv-sub {
        font-size: 1.15rem; font-weight: 600; opacity: 0.85; margin-bottom: 0.6rem;
    }
    .rv-hero .rv-tag {
        font-style: italic; opacity: 0.65; font-size: 1.0rem;
        max-width: 640px; margin: 0 auto;
    }

    /* headings inside sections */
    [data-testid="stExpander"] h2 {
        font-size: 1.55rem; text-align: center;
        padding-bottom: 0.6rem; margin-bottom: 0.8rem;
        border-bottom: 2px solid rgba(99, 110, 250, 0.45);
    }
    [data-testid="stExpander"] h4 {
        font-size: 1.15rem; margin-top: 1.6rem;
        color: #8ab4f8;
        border-left: 4px solid #636efa;
        padding-left: 0.6rem;
    }

    /* taglines & bold statements as callout cards */
    [data-testid="stExpander"] blockquote {
        border-left: 4px solid #f0b849;
        background: rgba(240, 184, 73, 0.07);
        padding: 0.7rem 1rem; border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }
    [data-testid="stExpander"] blockquote p { text-align: center; margin: 0; }

    /* the clickable section rows */
    [data-testid="stExpander"] {
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 12px;
        margin-bottom: 0.65rem;
        background: rgba(255,255,255,0.02);
    }
    [data-testid="stExpander"] summary {
        font-size: 1.06rem; padding: 0.85rem 1rem;
    }
    [data-testid="stExpander"] summary:hover { color: #8ab4f8; }

    /* tabs */
    button[data-baseweb="tab"] { font-weight: 600; }

    ul li { line-height: 1.7; margin-bottom: 0.3rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------ content loading
_here = Path(__file__).resolve().parent
CONTENT_DIR = _here.parent / "research_vision_content"
if not CONTENT_DIR.exists():
    CONTENT_DIR = _here / "research_vision_content"


@st.cache_data
def _read(path_str: str) -> str:
    """Cache only successful file reads."""
    return Path(path_str).read_text(encoding="utf-8")


def load(name: str) -> str:
    """Check the file fresh on every rerun; never cache the error message."""
    path = CONTENT_DIR / name
    if not path.exists():
        return f"*Content file not found: `{name}` (looked in `{CONTENT_DIR}`)*"
    return _read(str(path))


# ------------------------------------------------------------ hero header
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

# ------------------------------------------------------------ section map
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

# ------------------------------------------------------------ render
for label, intro_file, tabs in SECTIONS:
    with st.expander(f"**{label}**", expanded=False):
        if intro_file:
            st.markdown(load(intro_file))
        if tabs:
            st.markdown("")
            tab_objs = st.tabs([t[0].split("·")[0].split("—")[0].strip() for t in tabs])
            for tab, (tab_label, fname) in zip(tab_objs, tabs):
                with tab:
                    st.markdown(load(fname))

st.divider()
st.caption(
    "Science is one of humanity's greatest collaborative enterprises. "
    "Each generation inherits questions from the past, contributes new ideas in the "
    "present, and leaves foundations for future investigators."
)
