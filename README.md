# Personal academic website

Single-file static site. No build step, no dependencies.

## Put it online (GitHub Pages)

1. Create a new **public** repository named exactly `<your-github-username>.github.io`.
2. Upload `index.html` (and `cv.pdf`, if you want the CV link to work) to the root of that repo.
3. Go to **Settings → Pages**. Under *Build and deployment*, set Source to **Deploy from a branch**, branch `main`, folder `/ (root)`. Save.
4. Wait about a minute. The site is live at `https://<your-github-username>.github.io`.

Any repo works if you don't want the username URL — the site then lives at
`https://<username>.github.io/<repo-name>/`. Only the `<username>.github.io`
repo gives you the short address.

## Editing

Everything is in `index.html`: content in the HTML, styling in the `<style>` block
at the top. Colours and fonts are defined once as CSS variables in `:root`.

To add a publication, copy an existing `<li class="pub">` block and change the
text. The `data-type` attribute controls which filter it appears under:
`journal`, `review`, `conf`, or `chapter`.

## Before publishing — check these

- Add `cv.pdf` to the repo, or remove the CV link in the Contact section.
- Confirm the Google Scholar and ORCID links resolve correctly.
- Phone number, CGPA, date of birth, and referees' direct contact details were
  deliberately left off; add them back only if you want them public.
