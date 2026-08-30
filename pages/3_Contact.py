import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))

import theme

theme.page_setup("Contact")
theme.masthead()

theme.field_label("Get in touch")
st.markdown("# Contact")
st.markdown(
    "<p style='max-width:62ch;'>Questions about a blog, a request for the underlying data, or "
    "a correction — write to whichever office fits best.</p>",
    unsafe_allow_html=True,
)
st.write("")

OFFICES = [
    {
        "name": "Dr. Monendra Grover",
        "role": "Principal Scientist",
        "unit": "Discipline of Bioinformatics, Graduate School<br>ICAR-Indian Agricultural Research Institute<br>Pusa, New Delhi 110012",
        "mail": 'monendra.grover@gmail.com'
    },
  
]

for col, office in zip(st.columns(1, gap="medium"), OFFICES):
    with col:
        with st.container(border=True):
            st.markdown(
                f"""
<p class="postcard__meta">Office</p>
<p class="postcard__title">{office["role"]}</p>
<p style="font-size:.9rem;color:#2C3B33;">{office["unit"]}</p>
<p style="font-family:'IBM Plex Mono',monospace;font-size:.74rem;margin:0;">
  <a href="mailto:{office["mail"]}">{office["mail"]}</a>
</p>
""",
                unsafe_allow_html=True,
            )

st.write("")
theme.field_label("Where we are", muted=True)
st.markdown(
    "<p style='font-family:IBM Plex Mono,monospace;font-size:.8rem;color:#2C3B33;'>"
    "ICAR–Indian Agricultural Statistics Research Institute, Library Avenue, Pusa, "
    "New Delhi 110012, India</p>",
    unsafe_allow_html=True,
)

theme.footer()
