"""
Research Vision page for a Streamlit multipage app.

How to use:
1. Copy this file into your app's `pages/` folder (e.g. pages/2_Research_Vision.py).
2. Copy the `research_vision_content/` folder into the ROOT of your app
   (same folder as your main app .py file, NOT inside pages/).

Layout: each section appears as a clickable option from top to bottom.
Clicking a section expands it and shows the full content of that part.
"""

from pathlib import Path
import streamlit as st

st.set_page_config(page_title="Research Vision", page_icon="🔬", layout="wide")

# Content folder lives in the app root (one level above pages/), with a
# fallback for running this file directly with `streamlit run`.
_here = Path(__file__).resolve().parent
CONTENT_DIR = _here.parent / "research_vision_content"
if not CONTENT_DIR.exists():
    CONTENT_DIR = _here / "research_vision_content"


@st.cache_data
def load(name: str) -> str:
    path = CONTENT_DIR / name
    if not path.exists():
        return f"*Content file not found: `{name}` (looked in `{CONTENT_DIR}`)*"
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------- header
st.title("Research Vision")
st.markdown(
    "#### Understanding Organization, Intelligence, Discovery and the Future of Science"
)
st.markdown(
    "*\u201cExploring the universal principles that organize life, intelligence, "
    "scientific discovery, and artificial intelligence.\u201d*"
)
st.divider()

# ------------------------------------------------- section definitions
# (label shown on the option, file(s) to render when clicked)
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
    ("Part 1 · Research Philosophy", "part1_philosophy.md", None),
    ("Part 2 · The Grand Research Ecosystem", "part2_ecosystem.md", None),
    ("Part 3 · The Six Grand Research Programs", "p3_intro.md", PROGRAMS),
    ("Part 4 · The Universal Research Framework", None, CHAPTERS),
    ("Part 5 · Research Roadmap — Evolution of the Ecosystem", "part5_roadmap.md", None),
    ("Part 6 · Current Research — Research Portfolio", "part6_current_research.md", None),
    ("Part 7 · Publications and Scholarly Contributions", "part7_publications.md", None),
    ("Part 8 · Resources", "part8_resources.md", None),
    ("Part 9 · Collaboration", "part9_collaboration.md", None),
]

# --------------------------------------------------------------- render
for label, intro_file, tabs in SECTIONS:
    with st.expander(f"**{label}**", expanded=False):
        if intro_file:
            st.markdown(load(intro_file))
        if tabs:
            st.markdown("---")
            tab_objs = st.tabs([t[0].split("·")[0].split("—")[0].strip() for t in tabs])
            for tab, (tab_label, fname) in zip(tab_objs, tabs):
                with tab:
                    st.markdown(f"##### {tab_label}")
                    st.markdown(load(fname))

st.divider()
st.caption(
    "Science is one of humanity's greatest collaborative enterprises. "
    "Each generation inherits questions from the past, contributes new ideas in the "
    "present, and leaves foundations for future investigators."
)
