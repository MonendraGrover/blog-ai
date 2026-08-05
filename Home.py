import datetime
import os
from pathlib import Path

import streamlit as st

import blog_utils as bu
import theme

theme.page_setup()
theme.masthead()

CATEGORIES = bu.load_catalog()
POSTS = bu.all_posts(CATEGORIES)


# ─────────────────────────────────────────────────────────────────────────────
# Lead article — the newest blog, or the one flagged "featured" in meta.json
# ─────────────────────────────────────────────────────────────────────────────
def lead_article(post: bu.Post) -> None:
    theme.field_label("Latest")
    left, right = st.columns([1.5, 1], gap="large")

    with left:
        st.markdown(
            f"""
<p style="font-family:'IBM Plex Mono',monospace;font-size:.7rem;letter-spacing:.16em;
          text-transform:uppercase;color:#6B7A70;margin-bottom:6px;">
  {post.category} · {post.date_label} · {post.page_label}
</p>
<h1 style="font-size:clamp(1.9rem,3.6vw,3rem);line-height:1.04;margin:0 0 14px 0;">{post.title}</h1>
<p style="font-size:=3.10rem;color:#2C3B33;max-width:35ch;text-align: justify;">
  {post.summary or "Open the PDF to read this piece in full."}
</p>
""",
            unsafe_allow_html=True,
        )
        b1, b2, _ = st.columns([1, 1, 1.4])
        with b1:
            if st.button("Read blog", type="primary", use_container_width=True):
                st.query_params["post"] = post.slug
                st.switch_page("pages/1_Blogs.py")
        with b2:
            st.download_button(
                "Download",
                data=post.read_bytes(),
                file_name=post.path.name,
                mime="application/pdf",
                use_container_width=True,
                key="lead_dl",
            )

    with right:
        if post.cover:
            st.image(str(post.cover), use_container_width=True)
        elif os.path.exists("static/images/Workflow.png"):
            st.image("static/images/Workflow.png", use_container_width=True)


featured = next((p for p in POSTS if p.featured), POSTS[0]) if POSTS else None
if featured:
    lead_article(featured)
    st.markdown("<div style='height:34px;'></div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# What this is
# ─────────────────────────────────────────────────────────────────────────────
about_col, index_col = st.columns([1.35, 1], gap="large")

with about_col:
    theme.field_label("About this library")
    st.markdown(
        """
<p style="max-width:62ch; text-align: justify;">
Artificial intelligence is accelerating biological research by uncovering patterns in complex datasets such as genomes, transcriptomes, proteins, and medical images, while biology continues to inspire the development of intelligent algorithms through concepts such as neural networks, evolution, and swarm behaviour. This library brings together our work at the intersection of AI and biology, including method notes, protocol walkthroughs, benchmarking studies, implementation guides, and review articles. Every entry is available as a freely accessible PDF that can be read online or downloaded without a login.
</p>
<p style="max-width:62ch;">
Every entry is a PDF you can read in the browser or take away with you. Nothing is
behind a login.
</p>
""",
        unsafe_allow_html=True,
    )
    if st.button("Browse all blogs", type="primary"):
        st.switch_page("pages/1_Blogs.py")

with index_col:
    theme.field_label("Contents")
    if CATEGORIES:
        rows = "".join(
            f"""<div style="display:flex;justify-content:space-between;gap:12px;
                        padding:11px 0;border-bottom:1px solid #D6DED2;">
                  <span style="font-family:'Source Serif 4',serif;font-size:1rem;">
                    {c.icon} {c.name}
                  </span>
                  <span style="font-family:'IBM Plex Mono',monospace;font-size:.72rem;
                               color:#6B7A70;letter-spacing:.1em;white-space:nowrap;">
                    {len(c.posts):02d}
                  </span>
                </div>"""
            for c in CATEGORIES
        )
        st.markdown(rows, unsafe_allow_html=True)
    else:
        st.markdown(
            '<p style="font-family:IBM Plex Mono,monospace;font-size:.82rem;color:#6B7A70;">'
            "No categories yet. Create a folder in <code>static/blogs/</code> and drop a PDF in it."
            "</p>",
            unsafe_allow_html=True,
        )

# ─────────────────────────────────────────────────────────────────────────────
# Recent blogs
# ─────────────────────────────────────────────────────────────────────────────
featured = POSTS[0] if POSTS else None
recent = POSTS[1:4]
if recent:
    st.markdown("<div style='height:34px;'></div>", unsafe_allow_html=True)
    theme.field_label("Recently published")
    for col, post in zip(st.columns(3, gap="medium"), recent):
        with col:
            with st.container(border=True):
                st.markdown(
                    f'<p class="postcard__meta">{post.category} · {post.date_label}</p>'
                    f'<p class="postcard__title">{post.title}</p>'
                    f'<p class="postcard__summary">{post.summary[:150] or "Open the PDF to read it."}</p>',
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
