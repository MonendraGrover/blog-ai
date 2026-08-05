# EpiStackXpress — blog site

A Streamlit site that turns a folder of PDFs into a browsable blog. No model, no
database, no admin panel: drop a PDF into a category folder and it appears on the
Blogs page with a preview and a download button.

## Run it

```bash
pip install -r requirements.txt
streamlit run Home.py
```

## Add a blog

1. Put the PDF in a category folder under `static/blogs/`.
2. (Optional) Describe it in that folder's `meta.json`.
3. Refresh. The catalogue is cached for 30 seconds.

```
static/blogs/
├── categories.json                      optional — tab order, icons, blurbs
├── 01_Methylation-Biology/              becomes the tab "Methylation Biology"
│   ├── meta.json                        optional — titles, summaries, tags
│   ├── cpg-islands-in-rice.pdf          the blog
│   └── cpg-islands-in-rice.png          optional cover, same filename
├── 02_Machine-Learning/
└── 03_Protocols/
```

The `01_` prefix only controls sort order and is stripped from the tab label. A new
folder creates a new category tab automatically.

### meta.json

Keys are PDF filenames. Every field is optional.

```json
{
  "cpg-islands-in-rice.pdf": {
    "title": "CpG islands in rice promoters, revisited",
    "summary": "One or two sentences shown on the card.",
    "author": "Subham Ghosh",
    "date": "2026-05-12",
    "tags": ["methylation", "promoters", "rice"],
    "featured": true
  }
}
```

Missing `title` falls back to the filename; missing `date` falls back to the file's
modified date. `featured: true` pins the blog to the top of the home page.

### categories.json

```json
{
  "order": ["Methylation Biology", "Machine Learning", "Protocols"],
  "icons": { "Protocols": "🧪" },
  "descriptions": { "Protocols": "Step-by-step lab and pipeline notes." }
}
```

## Files

| File | Purpose |
|---|---|
| `Home.py` | Landing page: lead article, contents index, recent blogs |
| `pages/1_Blogs.py` | Category tabs, search, cards, and the in-page PDF reader |
| `pages/2_Publish_a_Blog.py` | Editor instructions and a live check of what's detected |
| `pages/3_Team.py` | Contributor profiles |
| `pages/4_Contact.py` | Office contacts |
| `theme.py` | Design tokens, CSS, masthead, footer |
| `blog_utils.py` | Filesystem catalogue loader and PDF viewer |

## Notes

- Put the institute logos at `static/images/icarlogo.png` and
  `static/images/iasri-logo.png`. The masthead degrades gracefully without them.
- The three PDFs currently in `static/blogs/` are placeholders. Delete them once
  real content is in.
- Every blog has a direct link: `?post=<slug>`, e.g.
  `.../Blogs?post=protocols-bismark-pipeline-walkthrough`.
