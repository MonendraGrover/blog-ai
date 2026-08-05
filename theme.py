"""
Shared look-and-feel for the EpiStackXpress reading room.

Design tokens
-------------
ink      #12211B   deep green-black, all body text
paper    #F1F4EE   pale sage page ground
surface  #FFFFFF   cards and panels
moss     #2E6B4F   primary (institution green, deepened)
turmeric #D8A11E   accent, used sparingly
indigo   #33427A   links and secondary marks
muted    #6B7A70   captions, metadata

Type: Bricolage Grotesque (display) / Source Serif 4 (body) / IBM Plex Mono (labels)
"""

import os
import streamlit as st

SITE_TITLE = "BioForge"
SITE_TAGLINE = "Forging the Future of AI and Biology."

INK = "#12211B"
PAPER = "#F1F4EE"
SURFACE = "#FFFFFF"
MOSS = "#2E6B4F"
TURMERIC = "#D8A11E"
INDIGO = "#33427A"
MUTED = "#6B7A70"
RULE = "#D6DED2"

LOGO_LEFT = "static/images/icarlogo.png"
LOGO_RIGHT = "static/images/iasri-logo.png"


def page_setup(subtitle: str = "") -> None:
    """Call once at the top of every page, before any other Streamlit call."""
    st.set_page_config(
        page_title=f"{SITE_TITLE} — {subtitle}" if subtitle else SITE_TITLE,
        page_icon="🌿",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_css()


def inject_css() -> None:
    st.markdown(
        f"""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,800&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">

<style>
:root {{
  --ink: {INK};
  --paper: {PAPER};
  --surface: {SURFACE};
  --moss: {MOSS};
  --turmeric: {TURMERIC};
  --indigo: {INDIGO};
  --muted: {MUTED};
  --rule: {RULE};
  --display: "Bricolage Grotesque", "Helvetica Neue", sans-serif;
  --body: "Source Serif 4", Georgia, serif;
  --mono: "IBM Plex Mono", ui-monospace, monospace;
}}

/* ---------- ground ---------- */
.stApp {{ background: var(--paper); }}
[data-testid="stHeader"] {{ background: transparent; }}
.block-container {{ padding-top: 2.2rem; padding-bottom: 1rem; max-width: 1320px; }}

html, body, [data-testid="stAppViewContainer"] {{
  font-family: var(--body);
  color: var(--ink);
  font-size: 17px;
}}

h1, h2, h3, h4 {{
  font-family: var(--display) !important;
  color: var(--ink) !important;
  letter-spacing: -0.02em;
  font-weight: 700;
}}

p, li {{ line-height: 1.62; }}
a {{ color: var(--indigo); text-decoration: none; border-bottom: 1px solid rgba(51,66,122,.3); }}
a:hover {{ border-bottom-color: var(--indigo); }}

/* ---------- masthead ---------- */
.masthead {{
  display: flex; align-items: center; gap: 22px;
  padding: 6px 0 18px 0;
  border-bottom: 2px solid var(--ink);
}}
.masthead__logo img {{ height: 58px; width: auto; display: block; }}
.masthead__text {{ flex: 1; min-width: 0; }}
.masthead__title {{
  font-family: var(--display);
  font-weight: 800;
  font-size: clamp(1.5rem, 3.1vw, 2.5rem);
  line-height: 1.02;
  letter-spacing: -0.035em;
  margin: 0;
}}
.masthead__title {{
    font-family: var(--display) !important;
    font-size: 4.8rem !important;
    font-weight: 900 !important;
    line-height: 0.9 !important;
    letter-spacing: -0.06em !important;
    color: var(--ink) !important;
    margin: 0 !important;
    padding: 0 !important;
}}
.masthead__tagline {{
  font-family: var(--mono);
  font-size: .72rem;
  letter-spacing: .16em;
  text-transform: uppercase;
  color: var(--muted);
  margin: 8px 0 0 0;
}}
.masthead__rule {{
  height: 4px; margin-bottom: 26px;
  background: linear-gradient(90deg, var(--moss) 0 34%, var(--turmeric) 34% 52%, var(--indigo) 52% 62%, transparent 62%);
}}

/* ---------- mono field labels (the signature device) ---------- */
.fieldlabel {{
  font-family: var(--mono);
  font-size: .68rem;
  font-weight: 500;
  letter-spacing: .18em;
  text-transform: uppercase;
  color: var(--moss);
  display: flex; align-items: center; gap: 10px;
  margin-bottom: 10px;
}}
.fieldlabel::after {{ content: ""; flex: 1; height: 1px; background: var(--rule); }}
.fieldlabel--muted {{ color: var(--muted); }}

/* ---------- cards ---------- */
[data-testid="stVerticalBlockBorderWrapper"] {{
  background: var(--surface);
  border: 1px solid var(--rule);
  border-radius: 2px;
  border-top: 3px solid var(--moss);
  transition: transform .18s ease, box-shadow .18s ease, border-top-color .18s ease;
  height: 100%;
}}
[data-testid="stVerticalBlockBorderWrapper"]:hover {{
  transform: translateY(-3px);
  box-shadow: 0 10px 26px -18px rgba(18,33,27,.55);
  border-top-color: var(--turmeric);
}}

.postcard__meta {{
  font-family: var(--mono);
  font-size: .68rem; letter-spacing: .1em; text-transform: uppercase;
  color: var(--muted); margin-bottom: 8px;
}}
.postcard__title {{
  font-family: var(--display); font-weight: 700;
  font-size: 1.16rem; line-height: 1.22; letter-spacing: -.02em;
  margin: 0 0 8px 0;
}}
.postcard__summary {{ font-size: .93rem; color: #2C3B33; margin: 0 0 12px 0; }}
.tagrow {{ display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 4px; }}
.tag {{
  font-family: var(--mono); font-size: .64rem; letter-spacing: .08em; text-transform: uppercase;
  color: var(--moss); background: rgba(46,107,79,.08);
  border: 1px solid rgba(46,107,79,.22); border-radius: 999px; padding: 2px 9px;
}}

/* ---------- specimen label (reader sidebar) ---------- */
.specimen {{
  background: var(--surface); border: 1px solid var(--rule);
  border-left: 4px solid var(--turmeric); border-radius: 2px;
  padding: 18px 18px 14px 18px; font-family: var(--mono); font-size: .78rem;
}}
.specimen dt {{
  font-size: .62rem; letter-spacing: .16em; text-transform: uppercase;
  color: var(--muted); margin-top: 12px;
}}
.specimen dt:first-child {{ margin-top: 0; }}
.specimen dd {{ margin: 3px 0 0 0; color: var(--ink); font-weight: 500; }}

/* ---------- category tabs ---------- */
.stTabs [data-baseweb="tab-list"] {{ gap: 4px; border-bottom: 1px solid var(--rule); }}
.stTabs [data-baseweb="tab"] {{
  font-family: var(--mono) !important; font-size: .74rem; letter-spacing: .1em; text-transform: uppercase;
  background: transparent; color: var(--muted); padding: 10px 16px; border-radius: 0;
}}
.stTabs [aria-selected="true"] {{ color: var(--ink) !important; background: rgba(46,107,79,.07); }}
.stTabs [data-baseweb="tab-highlight"] {{ background: var(--moss); height: 3px; }}

/* ---------- controls ---------- */
.stButton > button, .stDownloadButton > button {{
  font-family: var(--mono); font-size: .72rem; letter-spacing: .1em; text-transform: uppercase;
  border-radius: 2px; border: 1px solid var(--moss); color: var(--moss); background: transparent;
  padding: .42rem .9rem; transition: background .15s ease, color .15s ease;
}}
.stButton > button:hover, .stDownloadButton > button:hover {{
  background: var(--moss); color: #fff; border-color: var(--moss);
}}
.stButton > button[kind="primary"] {{ background: var(--moss); color: #fff; }}
.stButton > button[kind="primary"]:hover {{ background: var(--ink); border-color: var(--ink); }}
.stButton > button:focus-visible, .stDownloadButton > button:focus-visible {{
  outline: 3px solid var(--turmeric); outline-offset: 2px;
}}

[data-testid="stTextInput"] input, [data-testid="stSelectbox"] div[data-baseweb="select"] > div {{
  font-family: var(--mono); font-size: .82rem; border-radius: 2px;
}}

/* ---------- sidebar ---------- */
[data-testid="stSidebar"] {{ background: #EAEFE7; border-right: 1px solid var(--rule); }}
[data-testid="stSidebarNav"] a span {{ font-family: var(--mono); font-size: .78rem; letter-spacing: .06em; }}

/* ---------- footer ---------- */
.sitefooter {{
  margin-top: 46px; border-top: 2px solid var(--ink); padding: 16px 0 26px 0;
  display: flex; justify-content: space-between; gap: 16px; flex-wrap: wrap;
  font-family: var(--mono); font-size: .68rem; letter-spacing: .08em;
  text-transform: uppercase; color: var(--muted);
}}
.sitefooter b {{ color: var(--moss); }}

/* ---------- accessibility ---------- */
@media (prefers-reduced-motion: reduce) {{
  * {{ transition: none !important; animation: none !important; }}
}}
@media (max-width: 780px) {{
  .masthead {{ gap: 12px; }}
  .masthead__logo img {{ height: 40px; }}
}}
</style>
""",
        unsafe_allow_html=True,
    )


def _logo_html(path: str) -> str:
    import base64

    if not os.path.exists(path):
        return ""
    ext = "svg+xml" if path.endswith(".svg") else path.rsplit(".", 1)[-1]
    b64 = base64.b64encode(open(path, "rb").read()).decode()
    return f'<div class="masthead__logo"><img src="data:image/{ext};base64,{b64}" alt=""></div>'


def masthead() -> None:
    st.markdown(
        f"""
<div class="masthead">
  {_logo_html(LOGO_LEFT)}
  <div class="masthead__text">
    <h1 class="masthead__title">{SITE_TITLE}</h1>
    <p class="masthead__tagline">{SITE_TAGLINE}</p>
  </div>
  {_logo_html(LOGO_RIGHT)}
</div>
<div class="masthead__rule"></div>
""",
        unsafe_allow_html=True,
    )


def footer() -> None:
    st.markdown(
        """
<div class="sitefooter">
  <span>ICAR–Indian Agricultural Statistics Research Institute · Pusa, New Delhi 110012</span>
  <span>© 2026 · <b>All rights reserved</b></span>
</div>
""",
        unsafe_allow_html=True,
    )


def field_label(text: str, muted: bool = False) -> None:
    cls = "fieldlabel fieldlabel--muted" if muted else "fieldlabel"
    st.markdown(f'<div class="{cls}">{text}</div>', unsafe_allow_html=True)
