# Hong Liu 刘鸿

Personal academic website: **https://hongliu-math.github.io/**

The site uses **Hugo 0.167.0** with a small custom theme. All six sections from https://www.ibs.re.kr/ecopro/hongliu/ were preserved as downloaded on October 8, 2026. The published website needs no JavaScript.

## First publication

In GitHub, open **Settings → Pages → Build and deployment → Source** and choose **GitHub Actions**. The **Publish website** workflow deploys the site when changes are pushed to `main`. You can also run it manually under **Actions → Publish website → Run workflow**.

## Editing the site

Edit Markdown files in `content/`, either on GitHub or locally, and commit your changes. GitHub Actions builds and publishes the website automatically. Never edit or commit generated files in `public/`.

| Section | File |
| --- | --- |
| Home | `content/_index.md` |
| Coauthors | `content/coauthors.md` |
| Publications | `content/publications.md` |
| Students & Postdocs | `content/students-postdocs.md` |
| Talks | `content/talks.md` |
| Teaching | `content/teaching.md` |

The `+++` block at the top of each page contains its title. Below that, use Markdown headings, lists, and links. For example:

```markdown
## 2027

1. [Paper title](https://arxiv.org/abs/example), 20 pages.  
   *with Coauthor One, Coauthor Two*  
   Journal name, 2027.
```

Shared typography and colors are in `static/style.css`. Layouts are in `layouts/`, and navigation, contact information, and the site address are in `hugo.toml`. No external theme, Node.js, Ruby, or Python build framework is required.

## Papers, lecture notes, and portrait

122 public assets (about 377 MB) were copied locally into `static/assets/`. The website serves these at its own `/assets/` URLs. The first Hugo workflow restores missing assets using the copies already published on GitHub Pages, with IBS as a fallback, verifies their SHA-256 digests, and commits them to `static/assets/`. Subsequent builds use those archived files and do not need to contact IBS. Python is used only for this asset-restoration and verification step.

Five lecture PDFs already returned HTTP 404 on the original website. Their original links are retained: `fall10-tab.pdf`, `fall19-tab.pdf`, `fall21-tab.pdf`, `fall32-tab.pdf`, and `topic-comb-lecture14.pdf`. Replace them when copies become available.

`migration/` contains the original HTML pages, the content fragments used as the migration baseline, and a preservation report. All content text, all 299 content links, and all list numbering were preserved, with working IBS-hosted asset URLs rewritten to local copies. External scholarly and institutional links retain their original destinations. WordPress theme credits and interface chrome were replaced by the new layout.

Run `python3 scripts/verify-content.py` after `hugo` to check local links and confirm that unchanged content still matches the migration baseline. The workflow runs this automatically. Pages you deliberately edit in Markdown are allowed to change; their local file links are still checked.

## Local preview

Install Hugo from https://gohugo.io/installation/, then run:

```sh
hugo server
```

Open http://localhost:1313/. Saving changes to Markdown, templates, or CSS refreshes the preview. To create the published HTML without starting a server, run `hugo`; output goes to `public/`.
