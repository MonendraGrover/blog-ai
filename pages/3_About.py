import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))

import theme

theme.page_setup("About")
theme.masthead()

# ─────────────────────────────────────────────────────────────────────────────
# Hero
# ─────────────────────────────────────────────────────────────────────────────
theme.field_label("About")
st.markdown(
    """
<h1 style="max-width:24ch;">Exploring the Organisation of Knowledge Across Science,
Intelligence and Civilisation</h1>
<p style="font-family:'Source Serif 4',serif;font-style:italic;font-size:1.08rem;
          color:#2C3B33;max-width:58ch;">
Every scientific discipline reveals a different aspect of reality. My research seeks to
understand the universal principles that connect them.
</p>
""",
    unsafe_allow_html=True,
)
st.write("")

# ─────────────────────────────────────────────────────────────────────────────
# Welcome + journey  |  specimen sidebar
# ─────────────────────────────────────────────────────────────────────────────
left, right = st.columns([2.6, 1], gap="large")

with left:
    theme.field_label("Welcome", muted=True)
    st.markdown(
        """
<p style="max-width:66ch;text-align:justify;">
Welcome to my research website. I am <b>Dr Monendra Grover</b>, a molecular biologist by
training and a computational biologist by profession. My academic journey has gradually
expanded from molecular biology and computational genomics toward broader questions
concerning artificial intelligence, scientific discovery, Indian Knowledge Systems,
systems science, and the future organisation of knowledge.
</p>
<p style="max-width:66ch;text-align:justify;">
Although my research spans diverse disciplines, it is guided by a single objective:
</p>
<p style="max-width:60ch;font-family:'Bricolage Grotesque',sans-serif;font-weight:700;
          font-size:1.12rem;line-height:1.4;border-left:4px solid #D8A11E;
          padding-left:16px;color:#12211B;">
To understand how universal principles of organisation, information, intelligence, and
discovery operate across biological, artificial, cognitive, and societal systems.
</p>
<p style="max-width:66ch;">This website documents that continuing journey.</p>
""",
        unsafe_allow_html=True,
    )

    st.write("")
    theme.field_label("My scientific journey", muted=True)
    st.markdown(
        """
<p style="max-width:66ch;text-align:justify;">
Scientific careers often begin within a single discipline. Mine began with molecular
biology and gradually expanded through computational biology and bioinformatics into
increasingly interdisciplinary questions.
</p>
<p style="max-width:66ch;text-align:justify;">
Rather than viewing these as separate interests, I regard them as complementary
perspectives for exploring common scientific questions. This progression has naturally
led to the development of an interdisciplinary research ecosystem that integrates
multiple domains of knowledge while maintaining the methodological rigor of individual
disciplines.
</p>
""",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="tagrow">'
        + "".join(
            f'<span class="tag">{t}</span>'
            for t in [
                "Agricultural Bioinformatics",
                "Systems Biology",
                "Artificial Intelligence",
                "Cognitive Ecology",
                "Information Theory",
                "Complexity Science",
                "Indian Knowledge Systems",
                "Scientific Discovery",
                "Philosophy of Science",
            ]
        )
        + "</div>",
        unsafe_allow_html=True,
    )

with right:
    st.markdown(
        """
<div class="specimen">
  <dl>
    <dt>Researcher</dt><dd>Dr Monendra Grover</dd>
    <dt>Training</dt><dd>Molecular Biology</dd>
    <dt>Profession</dt><dd>Computational Biology</dd>
    <dt>Institute</dt><dd>ICAR–IASRI, Pusa, New Delhi</dd>
    <dt>Programmes</dt><dd>06 Grand Research Programs</dd>
  </dl>
</div>
""",
        unsafe_allow_html=True,
    )
    st.write("")
    if st.button("Browse the blogs", type="primary", use_container_width=True):
        st.switch_page("pages/1_Blogs.py")

st.markdown("<div style='height:34px;'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Research philosophy
# ─────────────────────────────────────────────────────────────────────────────
theme.field_label("Research philosophy")
st.markdown(
    """
<p style="max-width:72ch;text-align:justify;">
I believe that many of the most important scientific challenges of the twenty-first
century lie at the intersection of disciplines. Artificial Intelligence cannot be
understood through computer science alone. Modern biology increasingly depends upon
computation, systems thinking, and information theory. Education, governance,
sustainability, healthcare, and innovation similarly require interdisciplinary
perspectives.
</p>
<p style="max-width:72ch;text-align:justify;">
My research therefore seeks to identify recurring scientific principles that appear
across diverse fields while respecting the unique methods and evidence standards of each
discipline. This approach emphasizes <b>integration rather than fragmentation</b> and
<b>dialogue rather than disciplinary isolation</b>.
</p>
""",
    unsafe_allow_html=True,
)

st.markdown("<div style='height:26px;'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# The research ecosystem — six Grand Research Programs as cards
# ─────────────────────────────────────────────────────────────────────────────
theme.field_label("The research ecosystem")
st.markdown(
    "<p style='max-width:72ch;'>My work is organised around six interconnected "
    "<b>Grand Research Programs</b>. Rather than representing independent projects, they "
    "form components of a single evolving research ecosystem exploring intelligence, "
    "scientific creativity, interdisciplinary research, emerging technologies, and the "
    "long-term evolution of science.</p>",
    unsafe_allow_html=True,
)
st.write("")

PROGRAMS = [
    ("01", "Indian Knowledge Systems and the Future of Science"),
    ("02", "Thinking Machines, Ancient Minds"),
    ("03", "Cognitive Ecology of Scientific Discovery"),
    ("04", "Toward a Unified Science"),
    ("05", "Frontiers of Scientific Inquiry"),
    ("06", "Future of Humanity"),
]

for start in range(0, len(PROGRAMS), 3):
    row = PROGRAMS[start : start + 3]
    cols = st.columns(3, gap="medium")
    for col, (num, name) in zip(cols, row):
        with col:
            with st.container(border=True):
                st.markdown(
                    f'<p class="postcard__meta">Grand Research Program · {num}</p>'
                    f'<p class="postcard__title">{name}</p>',
                    unsafe_allow_html=True,
                )
    st.write("")

# ─────────────────────────────────────────────────────────────────────────────
# Domains + current interests, side by side
# ─────────────────────────────────────────────────────────────────────────────
dom_col, cur_col = st.columns(2, gap="large")

with dom_col:
    theme.field_label("Domains of inquiry", muted=True)
    st.markdown(
        "<p style='max-width:56ch;text-align:justify;'>The research ecosystem extends "
        "across a broad range of domains. The objective is not to become an expert in "
        "every field but to explore how universal scientific principles may illuminate "
        "questions across different domains.</p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="tagrow">'
        + "".join(
            f'<span class="tag">{t}</span>'
            for t in [
                "Natural Sciences",
                "Engineering & Technology",
                "Life Sciences",
                "Agriculture",
                "Artificial Intelligence",
                "Education",
                "Policy & Governance",
                "Social Sciences",
                "Humanities",
                "Arts, Culture & Human Performance",
                "Indian Knowledge Systems",
            ]
        )
        + "</div>",
        unsafe_allow_html=True,
    )

with cur_col:
    theme.field_label("Current academic interests", muted=True)
    st.markdown(
        "<p style='max-width:56ch;text-align:justify;'>Current areas of investigation "
        "continue to evolve as new scientific questions emerge.</p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="tagrow">'
        + "".join(
            f'<span class="tag">{t}</span>'
            for t in [
                "Bioinformatics & Computational Biology",
                "Artificial Intelligence",
                "Systems Biology",
                "Cognitive Ecology",
                "Information Theory",
                "Scientific Discovery",
                "Indian Knowledge Systems",
                "Complexity Science",
                "Interdisciplinary Research Methodology",
            ]
        )
        + "</div>",
        unsafe_allow_html=True,
    )

st.markdown("<div style='height:34px;'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Open science + beyond research
# ─────────────────────────────────────────────────────────────────────────────
os_col, br_col = st.columns(2, gap="large")

with os_col:
    theme.field_label("Open science")
    st.markdown(
        """
<p style="max-width:56ch;text-align:justify;">
I believe that scientific ideas become stronger through discussion, constructive
criticism, collaboration, and empirical evaluation. Accordingly, many ideas presented on
this website are shared at different stages of development — published research, review
articles, conceptual essays, working papers, educational resources, and visual
frameworks.
</p>
<p style="max-width:56ch;text-align:justify;">
Readers are encouraged to engage critically with these ideas and to contribute
alternative perspectives.
</p>
""",
        unsafe_allow_html=True,
    )

with br_col:
    theme.field_label("Beyond research")
    st.markdown(
        """
<p style="max-width:56ch;text-align:justify;">
Science is one of humanity's most creative endeavours. Accordingly, this research
ecosystem also explores relationships among science, education, culture, language,
architecture, music, dance, martial traditions, policy, and other forms of organised
human knowledge.
</p>
<p style="max-width:56ch;text-align:justify;">
These domains are not treated as isolated subjects but as complementary perspectives
through which recurring principles of organisation, information, intelligence,
creativity, and discovery may be investigated.
</p>
""",
        unsafe_allow_html=True,
    )

st.markdown("<div style='height:34px;'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Looking forward + closing thought
# ─────────────────────────────────────────────────────────────────────────────
theme.field_label("Looking forward")
st.markdown(
    """
<p style="max-width:72ch;text-align:justify;">
This website represents an evolving programme of interdisciplinary scientific inquiry
rather than a completed body of work. Its purpose is to document ideas, share research,
encourage collaboration, and contribute to ongoing conversations concerning the future of
science and human knowledge.
</p>
<p style="max-width:72ch;text-align:justify;">
I hope it serves not only as a record of my own research but also as a resource for
students, researchers, educators, and collaborators who share an interest in
interdisciplinary thinking and scientific exploration.
</p>
""",
    unsafe_allow_html=True,
)

st.write("")
st.markdown(
    """
<div style="border-top:2px solid #12211B;border-bottom:2px solid #12211B;
            padding:28px 8px;margin-top:10px;text-align:center;">
  <p style="font-family:'IBM Plex Mono',monospace;font-size:.66rem;letter-spacing:.2em;
            text-transform:uppercase;color:#6B7A70;margin:0 0 10px 0;">One final thought</p>
  <p style="font-family:'Bricolage Grotesque',sans-serif;font-weight:800;
            font-size:clamp(1.2rem,2.4vw,1.7rem);line-height:1.3;letter-spacing:-.02em;
            max-width:44ch;margin:0 auto;color:#12211B;">
    The future of science may depend not only on discovering new facts, but also on
    discovering better ways of connecting existing knowledge.
  </p>
</div>
""",
    unsafe_allow_html=True,
)

theme.footer()
