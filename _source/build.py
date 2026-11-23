"""Build the static site from content.py (al-folio-inspired look).

Usage (from the repository root):  python3 _source/build.py
Writes index.html, publications.html, gallery.html, people.html and cv.html.
Add --preview-unconfirmed to include People entries not yet confirmed (local preview only).
"""
import sys
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from content import *  # noqa: E402,F401,F403

ROOT = Path(__file__).resolve().parent.parent
SELF = "Munna, M. M. H."
TYPE_LABEL = {"journal": "Journal article", "conference": "Conference paper", "chapter": "Book chapter"}
UPDATED = "November 2026"
PREVIEW = "--preview-unconfirmed" in sys.argv
PEOPLE_LIVE = [p for p in PEOPLE if p.get("confirmed") or PREVIEW]
NAV = [("index.html", "about"), ("publications.html", "publications"), ("gallery.html", "gallery")] \
    + ([("people.html", "people")] if PEOPLE_LIVE else []) + [("cv.html", "cv")]


def e(s):
    return escape(str(s), quote=True)


def authors_html(a):
    return e(a).replace(e(SELF), f"<em>{e(SELF)}</em>")


def name_html():
    first, rest = PERSON["name"].split(" ", 1)
    return f'<span class="strong">{e(first)}</span> {e(rest)}'


ICON_SUN = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4.5"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
ICON_MOON = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 14.5A8.5 8.5 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5z"/></svg>'

THEME_BOOT = """<script>
    (function () {
      var t = null;
      try { t = localStorage.getItem('theme'); } catch (err) {}
      if (!t) t = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
      document.documentElement.setAttribute('data-theme', t);
    })();
  </script>"""

SITE_JS = """
  <script>
    (function () {
      var root = document.documentElement;
      var btn = document.getElementById('theme-toggle');
      function sync() { btn.setAttribute('aria-label', root.getAttribute('data-theme') === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'); }
      sync();
      btn.addEventListener('click', function () {
        var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        root.setAttribute('data-theme', next);
        try { localStorage.setItem('theme', next); } catch (err) {}
        sync();
      });
      var menuBtn = document.getElementById('menu-toggle');
      var menu = document.getElementById('site-menu');
      root.classList.add('js');
      menuBtn.addEventListener('click', function () {
        var open = menuBtn.getAttribute('aria-expanded') === 'true';
        menuBtn.setAttribute('aria-expanded', String(!open));
        menu.classList.toggle('open', !open);
      });
    })();
  </script>"""

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


# ---------------------------------------------------------------- shell
def shell(page, title, desc, body, script=""):
    cur = ' aria-current="page"'
    nav = "".join(f'<li><a href="{h}"{cur if h == page else ""}>{lab}</a></li>' for h, lab in NAV)
    full_title = PERSON["name"] if page == "index.html" else f"{title} | {PERSON['name']}"
    return f"""<!doctype html>
<html lang="en" data-theme="light">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(full_title)}</title>
  <meta name="description" content="{e(desc)}">
  <meta property="og:title" content="{e(full_title)}">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:type" content="profile">
  <meta property="og:image" content="assets/munna-og.jpg">
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Ctext x='16' y='23' font-size='20' text-anchor='middle' font-family='Arial' font-weight='700' fill='%23b509ac'%3EM%3C/text%3E%3C/svg%3E">
  {THEME_BOOT}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="navbar">
    <div class="container nav-row">
      <a class="brand" href="index.html">{name_html()}</a>
      <button type="button" class="menu-toggle" id="menu-toggle" aria-expanded="false" aria-controls="site-menu" aria-label="Menu">
        <span></span><span></span><span></span>
      </button>
      <nav id="site-menu" class="menu" aria-label="Main">
        <ul>{nav}</ul>
        <button type="button" class="theme-toggle" id="theme-toggle" aria-label="Switch to dark mode"><span class="only-light">{ICON_MOON}</span><span class="only-dark">{ICON_SUN}</span></button>
      </nav>
    </div>
  </header>
  <main id="main" class="container">
{body}
  </main>
  <footer class="site-foot">
    <div class="container">
      &copy; Copyright 2026 {e(PERSON['name'])}. Design adapted from the <a href="https://github.com/alshedivat/al-folio">al-folio</a> theme. Last updated: {UPDATED}.
    </div>
  </footer>
{SITE_JS}
{script}
</body>
</html>
"""


def page_header(title, desc):
    return f"""
    <header class="post-header">
      <h1 class="post-title">{e(title)}</h1>
      <p class="post-description">{e(desc)}</p>
    </header>"""


# ---------------------------------------------------------------- pieces
def bib_item(p, match=False):
    kind, year, authors, title, venue, doi, status = p
    abbr = VENUE_ABBR.get(doi, TYPE_LABEL[kind])
    badge = f' <span class="award">{e(status)}</span>' if status else ""
    m = f' data-match="{kind}"' if match else ""
    return f"""
          <li{m}>
            <div class="bib-row">
              <div class="abbr"><abbr class="badge" title="{e(venue)}">{e(abbr)}</abbr></div>
              <div class="bib-body">
                <div class="title">{e(title)}{badge}</div>
                <div class="author">{authors_html(authors)}</div>
                <div class="periodical"><em>{e(venue)}</em>, {year}</div>
                <div class="links"><a class="btn" href="https://doi.org/{e(doi)}">DOI</a><span class="kind">{TYPE_LABEL[kind]}</span></div>
              </div>
            </div>
          </li>"""


def filter_bar(target, options, label):
    btns = "".join(
        f'<button type="button" data-filter="{e(k)}" aria-pressed="{str(i == 0).lower()}">{e(lab)} <span class="count">{n}</span></button>'
        for i, (k, lab, n) in enumerate(options))
    return f'<div class="filter" role="group" aria-label="{e(label)}" data-filter-group="{target}">{btns}</div>'


def cv_card(title, rows):
    """rows: (date, title_html, sub_html)"""
    items = "".join(f"""
          <li>
            <div class="cv-date"><span class="badge-date">{e(d)}</span></div>
            <div class="cv-body"><div class="cv-title">{t}</div>{s}</div>
          </li>""" for d, t, s in rows)
    return f"""
      <section class="card cv-card" id="{title.lower().split()[0].strip('&')}">
        <h2 class="card-title">{title}</h2>
        <ul class="cv-list">{items}
        </ul>
      </section>"""


# ---------------------------------------------------------------- pages
def home():
    by_title = {p[3]: p for p in PUBS}
    selected = "".join(bib_item(by_title[t]) for t in SELECTED if t in by_title)
    news = "".join(f'<tr><th scope="row">{e(d)}</th><td>{e(t)}</td></tr>' for d, t in NEWS)
    work = "".join(f'<li><span class="strong">{e(t)}</span>: {e(d[0].lower() + d[1:])} <span class="muted">({e(s)})</span></li>'
                   for t, d, s in CURRENT_WORK)
    def soft(term):
        # lowercase ordinary words, keep acronyms such as IoT, AI, TinyML, LLM
        return " ".join(w if any(c.isupper() for c in w[1:]) else w.lower() for w in term.split())
    terms = [soft(t) for t in INTERESTS]
    interests = ", ".join(terms[:-1]) + ", and " + terms[-1]
    socials = "".join(f'<a href="{e(u)}">{e(n)}</a>' for n, u in [("Email", "mailto:" + PERSON["email"])] + PERSON["links"])
    body = f"""
    <div class="post">
      <header class="post-header">
        <h1 class="post-title about-title">{name_html()}</h1>
        <p class="desc">{e(PERSON['role'])}. {e(LEDE)}</p>
      </header>
      <article>
        <div class="profile float-right">
          <img class="z-depth-1 rounded" src="assets/munna.jpg" alt="Portrait of {e(PERSON['name'])}" width="320" height="320">
          <div class="more-info"><p>Research Assistant</p><p>North South University</p><p>Dhaka, Bangladesh</p></div>
        </div>
        <div class="clearfix">
          <p>{e(ABOUT)}</p>
          <p>My research interests include {e(interests)}.</p>
        </div>

        <h2><a href="#news" id="news">news</a></h2>
        <div class="news"><table>{news}</table></div>

        <h2><a href="#current" id="current">current work</a></h2>
        <ul class="current">{work}</ul>

        <h2><a href="publications.html">selected publications</a></h2>
        <div class="publications"><ol class="bibliography">{selected}
        </ol></div>

        <div class="social">{socials}</div>
      </article>
    </div>"""
    return shell("index.html", "about", f"{PERSON['role']}. Research on medical image analysis, computer vision and embedded AI.", body)


def publications():
    counts = {k: sum(1 for p in PUBS if p[0] == k) for k in TYPE_LABEL}
    bar = filter_bar("pub-list", [("all", "all", len(PUBS)), ("journal", "journals", counts["journal"]),
                                  ("conference", "conferences", counts["conference"]),
                                  ("chapter", "book chapter", counts["chapter"])], "Filter publications by type")
    groups = []
    for year in sorted({p[1] for p in PUBS}, reverse=True):
        items = "".join(bib_item(p, match=True) for p in PUBS if p[1] == year)
        groups.append(f'<div data-group><h2 class="bibliography">{year}</h2><ol class="bibliography">{items}\n        </ol></div>')
    datasets = "".join(f"""
          <li>
            <div class="bib-row">
              <div class="abbr"><abbr class="badge badge-data" title="Mendeley Data">Dataset</abbr></div>
              <div class="bib-body">
                <div class="title">{e(n)}</div>
                <div class="author">{authors_html(a)}</div>
                <div class="periodical">{e(d)} <em>Mendeley Data</em>, 2026</div>
                <div class="links"><a class="btn" href="{e(u)}">DATA</a></div>
              </div>
            </div>
          </li>""" for n, d, a, u, _ in DATASETS)
    body = f"""
    <div class="post">
      {page_header('publications', f'{len(PUBS)} peer-reviewed publications and 3 datasets, in reverse chronological order.')}
      <article class="publications">
        {bar}
        <div id="pub-list">
{''.join(groups)}
        </div>
        <h2 class="bibliography">datasets</h2>
        <ol class="bibliography">{datasets}
        </ol>
      </article>
    </div>"""
    return shell("publications.html", "publications", f"{len(PUBS)} peer-reviewed publications and 3 datasets by {PERSON['name']}.", body, FILTER_JS)


def gallery():
    photos = [g for g in GALLERY if (ROOT / "assets" / "gallery" / g["file"]).is_file()]
    for g in GALLERY:
        if g not in photos:
            print("  gallery: waiting for assets/gallery/" + g["file"])
    script = ""
    if photos:
        tags = []
        for g in photos:
            for t in g.get("tags", []):
                if t not in tags:
                    tags.append(t)
        bar = filter_bar("gallery-grid", [("all", "all", len(photos))] +
                         [(t, t, sum(1 for g in photos if t in g.get("tags", []))) for t in tags], "Filter photos by tag")
        items = []
        for g in photos:
            meta = ", ".join(x for x in (g.get("place"), g.get("date")) if x)
            tag_html = "".join(f'<span class="tag">{e(t)}</span>' for t in g.get("tags", []))
            items.append(f"""
        <li class="shot" data-match="{e('|'.join(g.get('tags', [])))}">
          <figure>
            <button type="button" class="shot-open" data-src="assets/gallery/{e(g['file'])}" aria-label="View larger: {e(g['caption'])}">
              <img class="z-depth-1 rounded" src="assets/gallery/{e(g['file'])}" alt="{e(g.get('alt', g['caption']))}" loading="lazy">
            </button>
            <figcaption>
              <p class="cap">{e(g['caption'])}</p>
              {f'<p class="meta">{e(meta)}</p>' if meta else ''}
              <p class="tags">{tag_html}</p>
            </figcaption>
          </figure>
        </li>""")
        content = f"""{bar}
      <ul class="gallery" id="gallery-grid">{''.join(items)}
      </ul>
      <dialog class="lightbox" id="lightbox" aria-label="Photo">
        <form method="dialog"><button class="lb-close" aria-label="Close">close</button></form>
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
        content = '<p class="empty">Photos from conference presentations, events and awards will be added here.</p>'
    body = f"""
    <div class="post">
      {page_header('gallery', 'presentations, events and awards')}
      <article>
      {content}
      </article>
    </div>"""
    return shell("gallery.html", "gallery", f"Photos of {PERSON['name']} presenting research and at academic events.", body, script)


def people():
    blocks = []
    for i, p in enumerate(PEOPLE_LIVE):
        side = "right" if i % 2 == 0 else "left"
        if p.get("photo") and (ROOT / "assets" / "people" / p["photo"]).is_file():
            pic = f'<img class="z-depth-1 rounded" src="assets/people/{e(p["photo"])}" alt="Portrait of {e(p["name"])}">'
        else:
            initials = "".join(w[0] for w in p["name"].replace("Dr. ", "").split()[:2])
            pic = f'<div class="initials z-depth-1 rounded" aria-hidden="true">{e(initials)}</div>'
        lines = "".join(f"<p>{e(l)}</p>" for l in p.get("lines", []))
        name = f'<a href="{e(p["url"])}">{e(p["name"])}</a>' if p.get("url") else e(p["name"])
        blocks.append(f"""
        <hr>
        <div class="profile float-{side}">
          {pic}
          <div class="more-info">{lines}</div>
        </div>
        <div class="clearfix">
          <h2 class="person-name">{name}</h2>
          <p>{e(p['bio'])}</p>
        </div>""")
    body = f"""
    <div class="post">
      {page_header('people', 'mentors and collaborators I have worked with')}
      <article>{''.join(blocks)}
      </article>
    </div>"""
    return shell("people.html", "people", f"Mentors and collaborators of {PERSON['name']}.", body)


def cv():
    edu = cv_card("Education", [(when, e(deg), f'<div class="cv-sub">{e(inst)}</div><div class="cv-sub muted">{e(g)}</div>')
                                for inst, deg, when, g in EDUCATION])
    exp = cv_card("Experience", [(when, e(role), f'<div class="cv-sub">{e(org)}, {e(loc)}</div><ul class="cv-points">'
                                  + "".join(f"<li>{e(b)}</li>" for b in bullets) + "</ul>")
                                 for role, org, loc, when, bullets in EXPERIENCE])
    certs = cv_card("Certifications", [(d or "undated", e(n), f'<div class="cv-sub">{e(by)}</div>' if by else "")
                                       for n, by, d in CERTS])
    awards = cv_card("Awards", [(y, e(t), f'<div class="cv-sub">{e(o)}</div>') for t, o, y in AWARDS])
    lead = cv_card("Leadership", [(when, e(t), f'<div class="cv-sub">{e(d)}</div>') for t, when, d in LEADERSHIP])
    service = "".join(f"<tr><th scope=\"row\">{e(k)}</th><td>{e(v)}</td></tr>" for k, v in SERVICE)
    skills = "".join(f"<tr><th scope=\"row\">{e(k)}</th><td>{e(v)}</td></tr>" for k, v in SKILLS)
    body = f"""
    <div class="post">
      {page_header('cv', 'education, experience, certifications and service')}
      <article class="cv">
        {edu}
        {exp}
        {certs}
        {awards}
        <section class="card cv-card" id="service"><h2 class="card-title">Academic service</h2><table class="kv">{service}</table></section>
        {lead}
        <section class="card cv-card" id="skills"><h2 class="card-title">Skills</h2><table class="kv">{skills}</table></section>
      </article>
    </div>"""
    return shell("cv.html", "cv", f"Education, experience, certifications and service of {PERSON['name']}.", body)


if __name__ == "__main__":
    pages = [("index.html", home), ("publications.html", publications), ("gallery.html", gallery), ("cv.html", cv)]
    if PEOPLE_LIVE:
        pages.insert(3, ("people.html", people))
    elif (ROOT / "people.html").exists():
        (ROOT / "people.html").unlink()
        print("removed people.html (no confirmed people yet)")
    for name, fn in pages:
        (ROOT / name).write_text(fn(), encoding="utf-8")
        print("wrote", name)
