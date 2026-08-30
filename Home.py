import datetime
from pathlib import Path

import streamlit as st

import blog_utils as bu
import theme

theme.page_setup()
theme.masthead()

CATEGORIES = bu.load_catalog()
POSTS = bu.all_posts(CATEGORIES)

COVER = "static/images/cover_page_infographic.png"

# ─────────────────────────────────────────────────────────────────────────────
# Hero — Rethinking Biology series
# ─────────────────────────────────────────────────────────────────────────────
left, right = st.columns([1.25, 1], gap="large")

with left:
    theme.field_label("A series by Dr Monendra Grover")
    st.markdown(
        """
<h1 style="font-size:clamp(2.2rem,4.4vw,3.4rem);line-height:1.02;margin:0 0 10px 0;">
Rethinking Biology</h1>
<p style="font-family:'IBM Plex Mono',monospace;font-size:.78rem;letter-spacing:.18em;
          text-transform:uppercase;color:#6B7A70;margin:0 0 16px 0;">
A journey from molecules to information</p>
<p style="font-family:'Source Serif 4',serif;font-style:italic;font-size:1.12rem;
          color:#2C3B33;max-width:46ch;">
Exploring life at the deepest level — from molecules to information.
</p>
<p style="max-width:56ch;text-align:justify;">
Biology is entering a new era. Rapid advances in genomics, computational power, and
information theory are transforming how we understand life. This series re-examines
fundamental biological questions through the lens of systems, computation and
information — bridging biology with physics, mathematics and AI. Each article is a
step in this journey.
</p>
""",
        unsafe_allow_html=True,
    )
    b1, b2, _ = st.columns([1, 1, 0.8])
    with b1:
        if st.button("Browse the blogs", type="primary", use_container_width=True):
            st.switch_page("pages/1_Blogs.py")
    with b2:
        if st.button("About me", use_container_width=True):
            st.switch_page("pages/4_About.py")

    st.write("")
    st.markdown(
        '<div class="tagrow">'
        + "".join(
            f'<span class="tag">{t}</span>'
            for t in [
                "Interdisciplinary",
                "Systems Thinking",
                "Information Centric",
                "Nature Inspired, Future Focused",
            ]
        )
        + "</div>",
        unsafe_allow_html=True,
    )

with right:
    if Path(COVER).exists():
        st.image(COVER, use_container_width=True)

st.markdown("<div style='height:34px;'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# The journey so far — the four series articles
# ─────────────────────────────────────────────────────────────────────────────
theme.field_label("The journey so far")

SERIES = [
    ("01", "Beyond Molecules",
     "Life as an Emergent Organization",
     "Why life cannot be understood by studying molecules in isolation. "
     "Emergence, organization and levels of complexity."),
    ("02", "The Cell as a System",
     "Information Flow, Networks and Regulation",
     "How cells process information through networks, feedback loops and "
     "dynamic regulation."),
    ("03", "Biology as Computation",
     "From Biological Processes to Algorithms",
     "Biological systems compute, adapt and learn. What can computation "
     "reveal about life?"),
    ("04", "The Quiet Revolution Called Quantum Biology",
     "Quantum Phenomena in Living Systems",
     "How quantum effects may influence key biological processes — from "
     "photosynthesis to olfaction."),
]

for col, (num, title, subtitle, blurb) in zip(st.columns(4, gap="medium"), SERIES):
    with col:
        with st.container(border=True):
            st.markdown(
                f'<p class="postcard__meta">Article · {num}</p>'
                f'<p class="postcard__title">{title}</p>'
                f'<p style="font-family:\'Source Serif 4\',serif;font-style:italic;'
                f'font-size:.88rem;color:#2C3B33;margin:0 0 8px 0;">{subtitle}</p>'
                f'<p class="postcard__summary">{blurb}</p>',
                unsafe_allow_html=True,
            )

st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# The vision
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
<div style="border-top:2px solid #12211B;border-bottom:2px solid #12211B;
            padding:28px 8px;text-align:center;">
  <p style="font-family:'IBM Plex Mono',monospace;font-size:.66rem;letter-spacing:.2em;
            text-transform:uppercase;color:#6B7A70;margin:0 0 10px 0;">The vision</p>
  <p style="font-family:'Bricolage Grotesque',sans-serif;font-weight:800;
            font-size:clamp(1.1rem,2.2vw,1.5rem);line-height:1.35;letter-spacing:-.02em;
            max-width:56ch;margin:0 auto 8px auto;color:#12211B;">
    To build a unifying framework where biology is understood as an
    information-processing reality, integrating insights from molecules to minds,
    from classical to quantum.
  </p>
  <p style="font-family:'Source Serif 4',serif;font-style:italic;font-size:1.02rem;
            color:#2C3B33;margin:0;">
    The goal is not just to understand life — but to rethink it.
  </p>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("<div style='height:34px;'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Latest from the library
# ─────────────────────────────────────────────────────────────────────────────
if POSTS:
    theme.field_label("Recently published")
    for col, post in zip(st.columns(3, gap="medium"), POSTS[:3]):
        with col:
            with st.container(border=True):
                st.markdown(
                    f'<p class="postcard__meta">{post.category} · {post.date_label}</p>'
                    f'<p class="postcard__title">{post.title}</p>'
                    f'<p class="postcard__summary">'
                    f'{post.summary[:150] or "Open the PDF to read it."}</p>',
                    unsafe_allow_html=True,
                )
                if st.button("Read", key=f"home_{post.slug}", use_container_width=True):
                    st.query_params["post"] = post.slug
                    st.switch_page("pages/1_Blogs.py")

# ─────────────────────────────────────────────────────────────────────────────
# Clock + visitor count
# ─────────────────────────────────────────────────────────────────────────────
COUNTER_FILE = Path("static/data/visitor_count.txt")


def read_count() -> int:
    try:
        return int(COUNTER_FILE.read_text().strip())
    except Exception:
        return 0


def bump_count() -> int:
    count = read_count() + 1
    try:
        COUNTER_FILE.parent.mkdir(parents=True, exist_ok=True)
        COUNTER_FILE.write_text(str(count))
    except Exception:
        pass
    return count


if "visited" not in st.session_state:
    st.session_state.visited = True
    visitors = bump_count()
else:
    visitors = read_count()

ist = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5, minutes=30)))

st.markdown(
    f"""
<div class="sitefooter" style="border-top:1px solid #D6DED2;margin-top:40px;padding-bottom:0;">
  <span>{ist.strftime("%d %B %Y · %I:%M %p IST")}</span>
  <span>{len(POSTS)} blogs · {len(CATEGORIES)} categories · <b>{visitors:,} visitors</b></span>
</div>
""",
    unsafe_allow_html=True,
)
theme.footer()
