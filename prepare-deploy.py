"""Restore archived public assets into Hugo's static directory before building."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib, json, subprocess, tomllib

root = Path(__file__).parent
manifest = json.loads((root / 'assets-manifest.json').read_text())
base_url = tomllib.loads((root / 'hugo.toml').read_text())['baseURL'].rstrip('/')
(root / 'static' / 'assets').mkdir(exist_ok=True)
def restore(entry):
    dest = root / 'static' / entry['path']
    if not dest.exists():
        # Reuse verified copies from the previous deployment before contacting IBS.
        sources = [base_url + '/' + entry['path'], entry['url']]
        for source in sources:
            result = subprocess.run(['curl', '-L', '--fail', '--silent', '--show-error', '--retry', '3', '--retry-all-errors', '--connect-timeout', '20', '--max-time', '120', source, '-o', str(dest)])
            if result.returncode == 0 and hashlib.sha256(dest.read_bytes()).hexdigest() == entry['sha256']:
                break
        else:
            raise RuntimeError('Unable to restore archived asset: ' + entry['path'])
    if hashlib.sha256(dest.read_bytes()).hexdigest() != entry['sha256']:
        raise RuntimeError('Source asset has changed: ' + entry['url'])
    print('Verified ' + entry['path'], flush=True)
with ThreadPoolExecutor(max_workers=3) as pool:
    list(pool.map(restore, manifest))
print(f'Hugo assets ready: {len(manifest)} verified files.')
