"""Check migrated content, hyperlinks, numbering, and generated local destinations."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import re, json, hashlib

root = Path(__file__).resolve().parents[1]

class Content(HTMLParser):
    def __init__(self, fragment=False):
        super().__init__(convert_charrefs=True)
        self.active = fragment
        self.div_depth = 0
        self.text = []
        self.links = []
        self.destinations = []
        self.lists = []
        self.list_stack = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'div':
            if self.active: self.div_depth += 1
            elif attrs.get('class') == 'prose':
                self.active = True
                self.div_depth = 1
        if tag in ('a', 'link') and 'href' in attrs: self.destinations.append(attrs['href'])
        if tag == 'img' and 'src' in attrs: self.destinations.append(attrs['src'])
        if not self.active: return
        if tag == 'a': self.links.append(attrs.get('href', ''))
        if tag in ('ul', 'ol'):
            self.lists.append([tag, attrs.get('start', '1'), 0])
            self.list_stack.append(self.lists[-1])
        if tag == 'li' and self.list_stack: self.list_stack[-1][2] += 1
    def handle_endtag(self, tag):
        if not self.active: return
        if tag == 'div':
            self.div_depth -= 1
            if self.div_depth == 0: self.active = False
        if tag in ('ul', 'ol') and self.list_stack: self.list_stack.pop()
    def handle_data(self, text):
        if self.active: self.text.append(text)

normal = lambda parts: re.sub(r'\s+', '', ''.join(parts))
results = []
baseline = json.loads((root / 'migration' / 'markdown-baseline.json').read_text())
for source in sorted((root / 'migration' / 'content-html').glob('*.html')):
    slug = source.stem
    generated = root / 'public' / ('index.html' if slug == 'home' else slug + '/index.html')
    old, new = Content(fragment=True), Content()
    old.feed(source.read_text())
    new.feed(generated.read_text())
    markdown = root / 'content' / ('_index.md' if slug == 'home' else slug + '.md')
    unchanged = hashlib.sha256(markdown.read_bytes()).hexdigest() == baseline[slug]
    if unchanged:
        assert normal(old.text) == normal(new.text), f'Text changed: {slug}'
        assert old.links == new.links, f'Links changed: {slug}'
        assert old.lists == new.lists, f'List numbering changed: {slug}'
    for url in new.destinations:
        parsed = urlsplit(url)
        if parsed.scheme or parsed.netloc or not parsed.path: continue
        path = root / 'public' / unquote(parsed.path.lstrip('/')) if parsed.path.startswith('/') else generated.parent / unquote(parsed.path)
        if path.is_dir(): path /= 'index.html'
        assert path.exists(), f'Missing local destination: {slug}: {url}'
    results.append({'page': slug, 'original_content_preserved': True if unchanged else 'intentionally edited', 'content_links': len(new.links), 'local_links_valid': True})
assert len(results) == 6, 'Missing content section'
print(json.dumps(results, ensure_ascii=False, indent=2))
