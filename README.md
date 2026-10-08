# Hong Liu 刘鸿

Personal academic website: **https://hongliu-math.github.io/**

The site preserves all six content sections from https://www.ibs.re.kr/ecopro/hongliu/ as downloaded on October 8, 2026. It uses plain HTML and CSS and works without JavaScript.

## First publication

In GitHub, open **Settings → Pages → Build and deployment → Source** and choose **GitHub Actions**. The **Publish website** workflow deploys the site when changes are pushed to `main`. You can also run it manually under **Actions → Publish website → Run workflow**.

## Editing the site

For a quick update in GitHub, edit `index.html` or a section's `index.html`, then commit. For local editing, change the matching HTML fragment in `content/`, then run `python3 build.py`. The build script uses only Python's standard library. Commit both the fragment and the generated page. Shared appearance is in `style.css`.

## Papers, lecture notes, and portrait

122 public assets (about 377 MB) were successfully copied locally. The deployed site serves copies of these assets at its own `/assets/` URLs. To avoid a large initial upload through the connector, `prepare-deploy.py` downloads missing assets during deployment using `assets-manifest.json` and verifies each file's SHA-256 digest. Future deployments therefore require the original asset URLs to remain available unless the downloaded files are committed into `assets/`. The complete local backup is in the workspace's `assets/` folder. Committing that folder later makes builds independent of IBS.

Five lecture PDFs already returned HTTP 404 on the original website. Their original links are retained: `fall10-tab.pdf`, `fall19-tab.pdf`, `fall21-tab.pdf`, `fall32-tab.pdf`, and `topic-comb-lecture14.pdf`. Replace them when copies become available.

`migration/` contains the original HTML pages and a preservation report. All content text and all 299 content links were preserved, with working IBS-hosted asset URLs rewritten to local copies. External scholarly and institutional links retain their original destinations. WordPress theme credits and interface chrome were replaced by the new layout.

## Local preview

Run `python3 -m http.server 8000` and open http://localhost:8000/. No installation or build framework is required to preview the generated website.
