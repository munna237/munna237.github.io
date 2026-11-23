"""Build the static site from content.py.

Usage (from the repository root):  python3 _source/build.py
Writes index.html, publications.html, gallery.html and cv.html to the repo root.
"""
import sys
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from content import *  # noqa: E402,F401,F403

ROOT = Path(__file__).resolve().parent.parent
SELF = "Munna, M. M. H."
TYPE_LABEL = {"journal": "Journal article", "conference": "Conference paper", "chapter": "Book chapter"}
NAV = [("index.html", "Home"), ("publications.html", "Publications"), ("gallery.html", "Gallery"), ("cv.html", "CV")]
UPDATED = "November 2026"


def e(s):
    return escape(str(s), quote=True)


def authors_html(a):
    return e(a).replace(e(SELF), f'<strong class="me">{e(SELF)}</strong>')


# ---------------------------------------------------------------- shell
def shell(page, title, desc, body, script=""):
    cur = ' aria-current="page"'
    nav = "".join(f'<a href="{href}"{cur if href == page else ""}>{label}</a>' for href, label in NAV)
    links = "".join(f'<a href="{e(u)}">{e(n)}</a>' for n, u in PERSON["links"])
    full_title = PERSON["name"] if page == "index.html" else f"{title} | {PERSON['name']}"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(full_title)}</title>
  <meta name="description" content="{e(desc)}">
  <meta property="og:title" content="{e(full_title)}">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:type" content="profile">
  <meta property="og:image" content="assets/munna-og.jpg">
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Ccircle cx='16' cy='16' r='13' fill='none' stroke='%233d3a8c' stroke-width='3'/%3E%3Ccircle cx='16' cy='16' r='4' fill='%23b83a64'/%3E%3C/svg%3E">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
</head>
<body class="page-{page.split('.')[0]}">
  <a class="skip" href="#main">Skip to content</a>
  <header class="site-head">
    <div class="wrap head-row">
      <a class="brand" href="index.html">{e(PERSON['name'])}</a>
      <nav class="site-nav" aria-label="Main">{nav}</nav>
    </div>
  </header>
  <main id="main" class="wrap">
{body}
  </main>
  <footer class="site-foot">
    <div class="wrap foot-row">
      <p><a href="mailto:{e(PERSON['email'])}">{e(PERSON['email'])}</a></p>
      <p class="foot-links">{links}</p>
      <p class="muted">Last updated {UPDATED}</p>
    </div>
  </footer>
{script}
</body>
</html>
"""


# ---------------------------------------------------------------- pieces
def pub_item(p):
    kind, year, authors, title, venue, doi, status = p
    badge = f' <span class="status">{e(status)}</span>' if status else ""
    return f"""
          <li class="pub" data-kind="{kind}">
            <p class="pub-title"><a href="https://doi.org/{e(doi)}">{e(title)}</a>{badge}</p>
            <p class="pub-authors">{authors_html(authors)}</p>
            <p class="pub-venue"><span class="kind">{TYPE_LABEL[kind]}</span> in <em>{e(venue)}</em></p>
          </li>"""


def timeline(items):
    """items: (when, title_html, body_html)"""
    rows = "".join(f"""
        <li>
          <div class="tl-when">{e(when)}</div>
          <div class="tl-body"><h3>{title}</h3>{body}</div>
        </li>""" for when, title, body in items)
    return f'<ol class="tl">{rows}\n      </ol>'


FILTER_JS = """
  <script>
    document.querySelectorAll('[data-filter-group]').forEach(function (bar) {
      var target = document.getElementById(bar.dataset.filterGroup);
      var buttons = bar.querySelectorAll('button');
      buttons.forEach(function (b) {
        b.addEventListener('click', function () {
          var f = b.dataset.filter;
          buttons.forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
          target.querySelectorAll('[data-match]').forEach(function (item) {
            item.hidden = !(f === 'all' || item.dataset.match.split('|').indexOf(f) !== -1);
          });
          target.querySelectorAll('[data-group]').forEach(function (g) {
            g.hidden = !g.querySelector('[data-match]:not([hidden])');
          });
        });
      });
    });
  </script>"""


def filter_bar(target, options, label):
    btns = "".join(
        f'<button type="button" data-filter="{e(k)}" aria-pressed="{str(i == 0).lower()}">{e(lab)} <span class="count">{n}</span></button>'
        for i, (k, lab, n) in enumerate(options))
    return f'<div class="chips filter" role="group" aria-label="{e(label)}" data-filter-group="{target}">{btns}</div>'


# ---------------------------------------------------------------- pages
def home():
    links = "".join(f'<li><a href="{e(u)}">{e(n)}</a></li>' for n, u in PERSON["links"] if n != "Credly badges")
    interests = "".join(f"<li>{e(i)}</li>" for i in INTERESTS)
    news = "".join(f'<li><span class="news-when">{e(d)}</span><span>{e(t)}</span></li>' for d, t in NEWS)
    work = "".join(f"""
          <li>
            <h3>{e(t)}</h3>
            <p>{e(d)}</p>
            <p class="work-status">{e(s)}</p>
          </li>""" for t, d, s in CURRENT_WORK)
    by_title = {p[3]: p for p in PUBS}
    selected = "".join(pub_item(by_title[t]) for t in SELECTED if t in by_title)
    collab = ""
    if COLLABORATORS:
        def person(n, a, r, u):
            name = f'<a href="{e(u)}">{e(n)}</a>' if u else e(n)
            return f'<li><h3>{name}</h3><p class="muted">{e(a)}</p><p>{e(r)}</p></li>'
        rows = "".join(person(*c) for c in COLLABORATORS)
        collab = f"""
    <section id="collaborators">
      <h2>Collaborators &amp; mentors</h2>
      <ul class="people">{rows}</ul>
    </section>"""
    n_pubs = len(PUBS)
    body = f"""
    <section class="hero">
      <figure class="field">
        <img src="assets/munna.jpg" alt="Portrait of {e(PERSON['name'])}" width="320" height="320">
        <svg class="reticle" viewBox="0 0 200 200" aria-hidden="true" focusable="false">
          <circle cx="100" cy="100" r="98"/>
          <g class="ticks"><line x1="100" y1="0" x2="100" y2="9"/><line x1="100" y1="191" x2="100" y2="200"/><line x1="0" y1="100" x2="9" y2="100"/><line x1="191" y1="100" x2="200" y2="100"/></g>
        </svg>
      </figure>
      <div class="hero-text">
        <h1>{e(PERSON['name'])}</h1>
        <p class="role">{e(PERSON['role'])}, {e(PERSON['place'])}</p>
        <p class="lede">{e(LEDE)}</p>
        <ul class="hero-links"><li><a href="mailto:{e(PERSON['email'])}">Email</a></li>{links}</ul>
      </div>
    </section>

    <section id="about" class="narrow">
      <h2>About</h2>
      <p class="bio">{e(ABOUT)}</p>
      <ul class="chips static">{interests}</ul>
    </section>

    <div class="split">
      <section id="news">
        <h2>News</h2>
        <ol class="news">{news}</ol>
      </section>
      <section id="now">
        <h2>Current work</h2>
        <ul class="work">{work}
        </ul>
      </section>
    </div>

    <section id="selected" class="narrow">
      <h2>Selected publications</h2>
      <ol class="pubs">{selected}
      </ol>
      <p class="more"><a href="publications.html">All {n_pubs} publications and 3 datasets</a></p>
    </section>
{collab}"""
    return shell("index.html", "Home", f"{PERSON['role']}. Research on medical image analysis, computer vision and embedded AI.", body)


def publications():
    counts = {k: sum(1 for p in PUBS if p[0] == k) for k in TYPE_LABEL}
    bar = filter_bar("pub-list", [("all", "All", len(PUBS)), ("journal", "Journals", counts["journal"]),
                                  ("conference", "Conferences", counts["conference"]),
                                  ("chapter", "Book chapter", counts["chapter"])], "Filter publications by type")
    groups = []
    for year in sorted({p[1] for p in PUBS}, reverse=True):
        items = "".join(pub_item(p).replace('<li class="pub"', '<li class="pub" data-match="' + p[0] + '"', 1)
                        for p in PUBS if p[1] == year)
        groups.append(f'<div class="year-group" data-group><h2 class="year">{year}</h2><ol class="pubs">{items}\n        </ol></div>')
    datasets = "".join(f"""
        <li class="dataset">
          <h3><a href="{e(u)}">{e(n)}</a></h3>
          <p>{e(d)}</p>
          <p class="pub-authors">{authors_html(a)} (2026). Mendeley Data.</p>
        </li>""" for n, d, a, u, _ in DATASETS)
    body = f"""
    <header class="page-head">
      <h1>Publications</h1>
      <p class="note">Peer-reviewed work, newest first. Titles link to the DOI. My name is in bold.</p>
    </header>
    <div class="narrow">
      {bar}
      <div id="pub-list">
{''.join(groups)}
      </div>
      <section id="datasets">
        <h2>Datasets</h2>
        <p class="note">Field-collected, annotated image datasets released openly on Mendeley Data.</p>
        <ul class="datasets">{datasets}
        </ul>
      </section>
    </div>"""
    return shell("publications.html", "Publications", f"{len(PUBS)} peer-reviewed publications and 3 datasets by {PERSON['name']}.", body, FILTER_JS)


def gallery():
    photos = [g for g in GALLERY if (ROOT / "assets" / "gallery" / g["file"]).is_file()]
    for g in GALLERY:
        if g not in photos:
            print("  gallery: waiting for assets/gallery/" + g["file"])
    if photos:
        tags = []
        for g in photos:
            for t in g.get("tags", []):
                if t not in tags:
                    tags.append(t)
        bar = filter_bar("gallery-grid", [("all", "All", len(photos))] +
                         [(t, t, sum(1 for g in photos if t in g.get("tags", []))) for t in tags], "Filter photos by tag")
        items = []
        for g in photos:
            meta = ", ".join(x for x in (g.get("place"), g.get("date")) if x)
            tag_html = "".join(f"<li>{e(t)}</li>" for t in g.get("tags", []))
            items.append(f"""
        <li class="shot" data-match="{e('|'.join(g.get('tags', [])))}">
          <figure>
            <button type="button" class="shot-open" data-src="assets/gallery/{e(g['file'])}" aria-label="View larger: {e(g['caption'])}">
              <img src="assets/gallery/{e(g['file'])}" alt="{e(g.get('alt', g['caption']))}" loading="lazy">
            </button>
            <figcaption>
              <p class="cap">{e(g['caption'])}</p>
              {f'<p class="meta">{e(meta)}</p>' if meta else ''}
              <ul class="tags">{tag_html}</ul>
            </figcaption>
          </figure>
        </li>""")
        content = f"""{bar}
    <ul class="gallery" id="gallery-grid">{''.join(items)}
    </ul>
    <dialog class="lightbox" id="lightbox" aria-label="Photo">
      <form method="dialog"><button class="lb-close" aria-label="Close">Close</button></form>
      <img alt="">
      <p class="lb-cap"></p>
    </dialog>"""
        script = FILTER_JS + """
  <script>
    (function () {
      var dlg = document.getElementById('lightbox');
      if (!dlg || !dlg.showModal) return;
      var img = dlg.querySelector('img'), cap = dlg.querySelector('.lb-cap');
      document.querySelectorAll('.shot-open').forEach(function (b) {
        b.addEventListener('click', function () {
          img.src = b.dataset.src;
          img.alt = b.querySelector('img').alt;
          cap.textContent = b.closest('figure').querySelector('.cap').textContent;
          dlg.showModal();
        });
      });
      dlg.addEventListener('click', function (ev) { if (ev.target === dlg) dlg.close(); });
    })();
  </script>"""
    else:
        content = """<p class="empty">Photos from conference presentations, events and awards will be added here.</p>"""
        script = ""
    body = f"""
    <header class="page-head">
      <h1>Gallery</h1>
      <p class="note">Presentations, events and awards.</p>
    </header>
    {content}"""
    return shell("gallery.html", "Gallery", f"Photos of {PERSON['name']} presenting research and at academic events.", body, script)


def cv():
    edu = timeline([(when, e(deg), f'<p class="where">{e(inst)}</p><p class="grade">{e(g)}</p>')
                    for inst, deg, when, g in EDUCATION])
    exp = timeline([(when, e(role), f'<p class="where">{e(org)}, {e(loc)}</p><ul class="points">'
                     + "".join(f"<li>{e(b)}</li>" for b in bullets) + "</ul>")
                    for role, org, loc, when, bullets in EXPERIENCE])
    dated = [c for c in CERTS if c[2]]
    undated = [c for c in CERTS if not c[2]]
    certs = timeline([(d, e(n), f'<p class="where">{e(by)}</p>' if by else "") for n, by, d in dated])
    certs_more = "".join(f"<li><span class=\"strong\">{e(n)}</span>{', ' + e(by) if by else ''}</li>" for n, by, _ in undated)
    awards = timeline([(y, e(t), f'<p class="where">{e(o)}</p>') for t, o, y in AWARDS])
    lead = timeline([(when, e(t), f"<p>{e(d)}</p>") for t, when, d in LEADERSHIP])
    service = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in SERVICE)
    skills = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in SKILLS)
    credly = dict(PERSON["links"]).get("Credly badges")
    jump = "".join(f'<li><a href="#{a}">{t}</a></li>' for a, t in [
        ("education", "Education"), ("experience", "Experience"), ("certifications", "Certifications"),
        ("awards", "Awards"), ("service", "Service"), ("leadership", "Leadership"), ("skills", "Skills")])
    body = f"""
    <header class="page-head">
      <h1>Curriculum vitae</h1>
      <nav aria-label="On this page"><ul class="jump">{jump}</ul></nav>
    </header>
    <div class="narrow">
      <section id="education"><h2>Education</h2>{edu}</section>
      <section id="experience"><h2>Research &amp; professional experience</h2>{exp}</section>
      <section id="certifications">
        <h2>Certifications</h2>{certs}
        <h3 class="minor">Also completed</h3>
        <ul class="plain">{certs_more}</ul>
        {f'<p class="more">Verified badges on <a href="{e(credly)}">Credly</a>.</p>' if credly else ''}
      </section>
      <section id="awards"><h2>Honors &amp; awards</h2>{awards}</section>
      <section id="service"><h2>Academic service</h2><dl class="pairs">{service}</dl></section>
      <section id="leadership"><h2>Leadership</h2>{lead}</section>
      <section id="skills"><h2>Technical skills</h2><dl class="pairs">{skills}</dl></section>
    </div>"""
    return shell("cv.html", "CV", f"Education, experience, certifications and service of {PERSON['name']}.", body)


if __name__ == "__main__":
    for name, fn in [("index.html", home), ("publications.html", publications), ("gallery.html", gallery), ("cv.html", cv)]:
        (ROOT / name).write_text(fn(), encoding="utf-8")
        print("wrote", name)
