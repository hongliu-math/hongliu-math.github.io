"""Build dependency-free static pages from editable content fragments."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).parent
PAGES = {'home': 'Home', 'coauthors': 'Coauthors', 'publications': 'Publications', 'students-postdocs': 'Students & Postdocs', 'talks': 'Talks', 'teaching': 'Teaching'}
for slug, title in PAGES.items():
    prefix = '.' if slug == 'home' else '..'
    nav = ''
    for key, label in PAGES.items():
        route = '' if key == 'home' else key + '/'
        current = 'aria-current="page"' if key == slug else ''
        nav += f'<a href="{prefix}/{route}" {current}>{escape(label)}</a>'
    content = (ROOT / 'content' / (slug + '.html')).read_text()
    # Relative asset links also work when previewing from a subdirectory.
    content = content.replace('href="/assets/', f'href="{prefix}/assets/').replace('src="/assets/', f'src="{prefix}/assets/')
    intro = '<div class="identity"><p class="eyebrow">MATHEMATICIAN</p><h1>Hong Liu <span lang="zh">刘鸿</span></h1><p class="affiliation">Institute for Basic Science · ECOPRO</p></div>' if slug == 'home' else f'<div class="page-heading"><p class="eyebrow">HONG LIU · MATHEMATICS</p><h1>{escape(title)}</h1></div>'
    document = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{"Hong Liu 刘鸿 — Mathematician" if slug == "home" else escape(title) + " — Hong Liu 刘鸿"}</title>
<meta name="description" content="Hong Liu, mathematician at the Institute for Basic Science. Research in extremal and probabilistic combinatorics, publications, teaching, and talks.">
<link rel="canonical" href="https://hongliu-math.github.io/{"" if slug == "home" else slug + "/"}">
<link rel="icon" href="{prefix}/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{prefix}/style.css"></head>
<body><a class="skip" href="#main">Skip to content</a><header class="site-header"><div class="header-inner"><a class="brand" href="{prefix}/">Hong Liu <span lang="zh">刘鸿</span></a><nav aria-label="Main navigation">{nav}</nav></div></header>
<main id="main" class="layout {"home" if slug == "home" else ""}"><article>{intro}<div class="prose">{content}</div></article>
<aside class="profile"><img src="{prefix}/assets/hong-liu.jpg" alt="Hong Liu" width="1024" height="934"><div class="profile-caption"><p>Hong Liu <span lang="zh">刘鸿</span></p><span>Mathematician</span></div><a class="contact" href="mailto:hongliu@ibs.re.kr">hongliu@ibs.re.kr</a><a class="group" href="https://www.ibs.re.kr/ecopro/">ECOPRO research group</a></aside></main>
<footer><span>© 2026 Hong Liu 刘鸿</span><a href="mailto:hongliu@ibs.re.kr">Contact</a><a href="https://www.ibs.re.kr/ecopro/">ECOPRO</a></footer></body></html>'''
    destination = ROOT / ('index.html' if slug == 'home' else slug + '/index.html')
    destination.parent.mkdir(exist_ok=True)
    destination.write_text(document)
print('Built all six pages.')
