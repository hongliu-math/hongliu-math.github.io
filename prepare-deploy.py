"""Assemble the static deployment and restore archived PDFs from their public sources."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib, json, shutil, subprocess

root = Path(__file__).parent
out = root / '_site'
out.mkdir(exist_ok=True)
for name in ('index.html', 'style.css', 'favicon.svg', '.nojekyll', '404.html'):
    shutil.copy2(root / name, out / name)
for name in ('coauthors', 'publications', 'students-postdocs', 'talks', 'teaching'):
    shutil.copytree(root / name, out / name, dirs_exist_ok=True)
manifest = json.loads((root / 'assets-manifest.json').read_text())
(out / 'assets').mkdir(exist_ok=True)
def restore(entry):
    dest = out / entry['path']
    local = root / entry['path']
    if local.exists():
        shutil.copy2(local, dest)
    else:
        subprocess.run(['curl', '-L', '--fail', '--silent', '--show-error', '--retry', '3', '--max-time', '120', entry['url'], '-o', str(dest)], check=True)
    if hashlib.sha256(dest.read_bytes()).hexdigest() != entry['sha256']:
        raise RuntimeError('Source asset has changed: ' + entry['url'])
with ThreadPoolExecutor(max_workers=8) as pool:
    list(pool.map(restore, manifest))
print(f'Deployment ready: six pages and {len(manifest)} archived assets.')
