from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent
HOME_PAGE = "pages/4_About.py"  # the page visitors see first


def page_title(stem: str) -> str:
    """Turn '1_Blogs' or '2_User_Guide' into 'Blogs' / 'User Guide'."""
    head, _, rest = stem.partition("_")
    name = rest if head.isdigit() and rest else stem
    return name.replace("_", " ")


# About is the home page
pages = [st.Page(HOME_PAGE, title="About", default=True)]

# Every other page in pages/ is added automatically, in file-name order
for file in sorted((ROOT / "pages").glob("*.py")):
    path = f"pages/{file.name}"
    if path == HOME_PAGE:
        continue
    pages.append(st.Page(path, title=page_title(file.stem)))

st.navigation(pages).run()
