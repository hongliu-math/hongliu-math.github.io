"""Restore archived public assets into Hugo's static directory before building."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib, json, subprocess

root = Path(__file__).parent
manifest = json.loads((root / 'assets-manifest.json').read_text())
(root / 'static' / 'assets').mkdir(exist_ok=True)
def restore(entry):
    dest = root / 'static' / entry['path']
    if not dest.exists():
        subprocess.run(['curl', '-L', '--fail', '--silent', '--show-error', '--retry', '5', '--retry-all-errors', '--connect-timeout', '20', '--max-time', '120', entry['url'], '-o', str(dest)], check=True)
    if hashlib.sha256(dest.read_bytes()).hexdigest() != entry['sha256']:
        raise RuntimeError('Source asset has changed: ' + entry['url'])
    print('Verified ' + entry['path'], flush=True)
with ThreadPoolExecutor(max_workers=3) as pool:
    list(pool.map(restore, manifest))
print(f'Hugo assets ready: {len(manifest)} verified files.')
