from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent


def page_title(stem: str) -> str:
    """Turn '1_Blogs' or '2_User_Guide' into 'Blogs' / 'User Guide'."""
    head, _, rest = stem.partition("_")
    name = rest if head.isdigit() and rest else stem
    return name.replace("_", " ")


# About is the home page
pages = [st.Page("About.py", title="About", default=True)]

# Every other page in pages/ is picked up automatically, in file-name order
for file in sorted((ROOT / "pages").glob("*.py")):
    pages.append(st.Page(f"pages/{file.name}", title=page_title(file.stem)))

st.navigation(pages).run()
