# Mohammad Mehedi Hasan Munna: research portfolio

A static, four-page portfolio site: **Home**, **Publications**, **Gallery** and **CV**. It is plain HTML and CSS with a few lines of JavaScript for the filters and the photo viewer. There is no framework.

```
index.html          Home: bio, news, current work, selected publications
publications.html   Journals, conferences, book chapter (filterable) and datasets
gallery.html        Photos with captions and tags (filterable, click to enlarge)
cv.html             Education, experience and certification timelines, awards, service, skills
style.css           All styling
assets/             Portrait, share image, and gallery/ for event photos
_source/            content.py (all text) and build.py (generates the HTML pages)
```

## Live site

**https://munna237.github.io**

GitHub Pages serves this repository from the `main` branch. If the site doesn't appear, open **Settings → Pages** and make sure the source is **Deploy from a branch**, branch **`main`**, folder **`/ (root)`**.

## Updating the site

All content lives in **`_source/content.py`**. Edit it, then regenerate the pages from the repository root:

```bash
python3 _source/build.py
```

Commit and push the changed `.html` files. Don't edit the `.html` files by hand, because the next build overwrites them.

### Adding a gallery photo

1. Put the image in `assets/gallery/`. A JPG about 1600 px wide is plenty.
2. Add an entry to `GALLERY` in `content.py`, newest first. Entries whose photo is missing are skipped, so the six captions already listed appear as soon as their photos (`iccit-2025.jpg`, `ieee-access.jpg`, `lab.jpg`, `icsc.jpg`, `best-intern.jpg`, `ieee-workshop.jpg`) are uploaded and the site is rebuilt:

```python
{"file": "iccit-2025-talk.jpg",
 "caption": "Presenting “Deep Learning for Reliable Healthcare” at ICCIT 2025",
 "place": "Dhaka, Bangladesh", "date": "Dec 2025",
 "tags": ["Paper presentation", "ICCIT 2025"]},
```

Tags become the filter buttons automatically.

### Other sections

- **News:** add `("Mon YYYY", "What happened.")` to the top of `NEWS`.
- **Current work:** `CURRENT_WORK` entries are `(title, one line, status)`.
- **Collaborators & mentors:** this section appears on the home page once `COLLABORATORS` has entries. Ask each person before listing them.
- **Publications:** add a tuple to `PUBS`. The filter counts update by themselves.
