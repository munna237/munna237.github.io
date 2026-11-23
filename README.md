# Mohammad Mehedi Hasan Munna: research portfolio

A static portfolio site with **about**, **publications**, **gallery**, **people** and **cv** pages. Its look is adapted from the [al-folio](https://github.com/alshedivat/al-folio) Jekyll theme (MIT), with a light/dark toggle. It is plain HTML and CSS with a few lines of JavaScript for the filters and the photo viewer. There is no framework.

```
index.html          Home: bio, news, current work, selected publications
publications.html   Journals, conferences, book chapter (filterable) and datasets
gallery.html        Photos with captions and tags (filterable, click to enlarge)
people.html         Mentors and collaborators (only generated once someone is confirmed)
cv.html             Education, experience and certification timelines, awards, service, skills
style.css           All styling
assets/             Portrait, share image, and gallery/ for event photos
_source/            content.py (all text) and build.py (generates the HTML pages)
```

## Live site

**https://munna237.github.io**

GitHub Pages serves this repository from the `main` branch. If the site doesn't appear, open **Settings → Pages** and make sure the source is **Deploy from a branch**, branch **`main`**, folder **`/ (root)`**.

## Updating the site

All content lives in **`_source/content.py`**. Styling is in `style.css`. Edit it, then regenerate the pages from the repository root:

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
- **People:** add a profile to `PEOPLE`. Only entries with `"confirmed": True` are published, and the **people** page and menu item appear once at least one is confirmed. Put photos in `assets/people/`. To preview unconfirmed entries locally, run `python3 _source/build.py --preview-unconfirmed`, but don't commit that output.
- **Venue badges:** the short label beside each paper comes from `VENUE_ABBR`, keyed by DOI.
- **Publications:** add a tuple to `PUBS`. The filter counts update by themselves.
