import base64
import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))

import theme

theme.page_setup("Contact")
theme.masthead()

theme.field_label("Get in touch")
st.markdown("# Contact")

st.write("")

PHOTO = Path("static/images/Monendra_grover.jpeg")


def photo_html() -> str:
    """Circular photo, embedded at full quality; empty string if file missing."""
    if not PHOTO.exists():
        return ""
    ext = PHOTO.suffix.lstrip(".").lower()
    mime = "jpeg" if ext in ("jpg", "jpeg") else ext
    b64 = base64.b64encode(PHOTO.read_bytes()).decode()
    return (
        f'<img src="data:image/{mime};base64,{b64}" alt="Monendra Grover" '
        'style="width:84px;height:84px;border-radius:50%;object-fit:cover;'
        'border:2px solid #12211B;flex-shrink:0;"/>'
    )


OFFICES = [
    {
        "name": "Monendra Grover",
        "role": "Principal Scientist",
        "unit": "Division of Agricultural Bioinformatics, Graduate School<br>ICAR-Indian Agricultural Research Institute<br>Pusa, New Delhi 110012",
        "mail": "monendra.grover@gmail.com",
    },
]

for col, office in zip(st.columns(1, gap="medium"), OFFICES):
    with col:
        with st.container(border=True):
            st.markdown(
                f"""
<p class="postcard__meta">Office</p>
<div style="display:flex;align-items:center;gap:16px;margin:6px 0 12px 0;">
  {photo_html()}
  <div>
    <p style="font-family:'Bricolage Grotesque',sans-serif;font-weight:800;
              font-size:1.25rem;line-height:1.2;margin:0;color:#12211B;">
      {office["name"]}
    </p>
    <p class="postcard__title" style="margin:2px 0 0 0;">{office["role"]}</p>
  </div>
</div>
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
