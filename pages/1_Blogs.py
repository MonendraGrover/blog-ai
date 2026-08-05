import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))

import blog_utils as bu
import theme

theme.page_setup("Blogs")
theme.masthead()

CATEGORIES = bu.load_catalog()


# ─────────────────────────────────────────────────────────────────────────────
# Reader view — opened with ?post=<slug>, so any article can be linked directly
# ─────────────────────────────────────────────────────────────────────────────
def open_post(slug: str) -> None:
    st.query_params["post"] = slug


def close_post() -> None:
    st.query_params.clear()


def reader(post: bu.Post) -> None:
    st.button("← All blogs", on_click=close_post, key="back_top")

    left, right = st.columns([2.6, 1])
    with left:
        theme.field_label(post.category)
        st.markdown(f"# {post.title}")
        if post.summary:
            st.markdown(
                f"<p style='font-size:1.06rem;color:#2C3B33;'>{post.summary}</p>",
                unsafe_allow_html=True,
            )
    with right:
        tags = "".join(f'<span class="tag">{t}</span>' for t in post.tags)
        st.markdown(
            f"""
<div class="specimen">
  <dl>
    <dt>Published</dt><dd>{post.date_label}</dd>
    <dt>Author</dt><dd>{post.author or "ICAR–IASRI"}</dd>
    <dt>Extent</dt><dd>{post.page_label} · {post.size_label}</dd>
    <dt>File</dt><dd>{post.path.name}</dd>
  </dl>
  <div class="tagrow" style="margin-top:14px;">{tags}</div>
</div>
""",
            unsafe_allow_html=True,
        )
        st.write("")
        st.download_button(
            "Download PDF",
            data=post.read_bytes(),
            file_name=post.path.name,
            mime="application/pdf",
            key=f"dl_reader_{post.slug}",
            type="primary",
            use_container_width=True,
        )

    st.write("")
    theme.field_label("Full text", muted=True)
    bu.render_pdf(post)

    related = [
        p
        for p in bu.all_posts(CATEGORIES)
        if p.category == post.category and p.slug != post.slug
    ][:3]
    if related:
        st.write("")
        theme.field_label(f"More in {post.category}", muted=True)
        for col, rel in zip(st.columns(len(related)), related):
            with col:
                card(rel, key_prefix="rel")

    theme.footer()


# ─────────────────────────────────────────────────────────────────────────────
# Card
# ─────────────────────────────────────────────────────────────────────────────
def card(post: bu.Post, key_prefix: str = "grid") -> None:
    with st.container(border=True):
        st.markdown('<div class="postcard"></div>', unsafe_allow_html=True)
        if post.cover:
            st.image(str(post.cover), use_container_width=True)

        byline = f" · {post.author}" if post.author else ""
        st.markdown(
            f'<p class="postcard__meta">{post.date_label} · {post.page_label}{byline}</p>'
            f'<p class="postcard__title">{post.title}</p>'
            f'<p class="postcard__summary">{post.summary or "No summary yet — open the PDF to read it."}</p>',
            unsafe_allow_html=True,
        )
        if post.tags:
            st.markdown(
                '<div class="tagrow">'
                + "".join(f'<span class="tag">{t}</span>' for t in post.tags)
                + "</div>",
                unsafe_allow_html=True,
            )

        act1, act2 = st.columns(2)
        with act1:
            st.button(
                "Read",
                key=f"{key_prefix}_read_{post.slug}",
                on_click=open_post,
                args=(post.slug,),
                use_container_width=True,
            )
        with act2:
            st.download_button(
                "Download",
                data=post.read_bytes(),
                file_name=post.path.name,
                mime="application/pdf",
                key=f"{key_prefix}_dl_{post.slug}",
                use_container_width=True,
            )


def grid(posts: list[bu.Post], key_prefix: str, per_row: int = 3) -> None:
    if not posts:
        st.markdown(
            '<p style="font-family:IBM Plex Mono,monospace;font-size:.82rem;color:#6B7A70;">'
            "Nothing matches that search. Clear the filters to see every blog.</p>",
            unsafe_allow_html=True,
        )
        return
    for start in range(0, len(posts), per_row):
        row = posts[start : start + per_row]
        cols = st.columns(per_row, gap="medium")
        for col, post in zip(cols, row):
            with col:
                card(post, key_prefix)
        st.write("")


# ─────────────────────────────────────────────────────────────────────────────
# Routing
# ─────────────────────────────────────────────────────────────────────────────
requested = st.query_params.get("post")
if requested:
    found = bu.find_post(requested)
    if found:
        reader(found)
        st.stop()
    st.warning("That blog is no longer available. Showing everything instead.")
    st.query_params.clear()

if not CATEGORIES:
    theme.field_label("Blogs")
    st.markdown(
        "### No blogs published yet\n"
        "Add a category folder inside `static/blogs/`, drop a PDF into it, and refresh — "
        "the article appears here automatically. See the **User Guide** page for the "
        "`meta.json` fields that add a summary, author and tags."
    )
    theme.footer()
    st.stop()


# ─────────────────────────────────────────────────────────────────────────────
# Filters
# ─────────────────────────────────────────────────────────────────────────────
theme.field_label("Blogs")

posts_all = bu.all_posts(CATEGORIES)
every_tag = sorted({t for p in posts_all for t in p.tags})

f1, f2, f3 = st.columns([2.4, 1.6, 1])
with f1:
    query = st.text_input(
        "Search", placeholder="Search titles, summaries, authors…", label_visibility="collapsed"
    )
with f2:
    picked_tags = st.multiselect(
        "Tags", every_tag, placeholder="Filter by tag", label_visibility="collapsed"
    )
with f3:
    order = st.selectbox(
        "Sort", ["Newest first", "Oldest first", "A–Z"], label_visibility="collapsed"
    )


def apply_filters(posts: list[bu.Post]) -> list[bu.Post]:
    out = posts
    if query:
        q = query.lower()
        out = [
            p
            for p in out
            if q in p.title.lower()
            or q in p.summary.lower()
            or q in p.author.lower()
            or any(q in t.lower() for t in p.tags)
        ]
    if picked_tags:
        out = [p for p in out if set(picked_tags) & set(p.tags)]
    if order == "Oldest first":
        out = sorted(out, key=lambda p: p.published)
    elif order == "A–Z":
        out = sorted(out, key=lambda p: p.title.lower())
    else:
        out = sorted(out, key=lambda p: p.published, reverse=True)
    return out


st.write("")

# ─────────────────────────────────────────────────────────────────────────────
# Category tabs
# ─────────────────────────────────────────────────────────────────────────────
labels = [f"All ({len(posts_all)})"] + [f"{c.label} ({len(c.posts)})" for c in CATEGORIES]
tabs = st.tabs(labels)

with tabs[0]:
    st.write("")
    grid(apply_filters(posts_all), "all")

for tab, category in zip(tabs[1:], CATEGORIES):
    with tab:
        if category.blurb:
            st.markdown(
                f"<p style='max-width:70ch;color:#2C3B33;'>{category.blurb}</p>",
                unsafe_allow_html=True,
            )
        st.write("")
        grid(apply_filters(category.posts), category.slug)

theme.footer()
