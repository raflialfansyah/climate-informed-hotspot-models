"""Inventory the local public-release candidate, excluding private/runtime files."""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]


def is_public(path):
    relative=path.relative_to(ROOT)
    parts=relative.parts
    if any(p in {'.git','__pycache__','.ipynb_checkpoints','.venv','venv'} for p in parts):return False
    if parts[0] in {'generated','outputs_main'}:return False
    if relative.is_relative_to('data/local') or relative.is_relative_to('validation/runtime'):return False
    if relative.is_relative_to('data/raw') and relative.as_posix()!='data/raw/README.md':return False
    if relative.as_posix() in {'.local_paths.json','provenance/RELEASE_MANIFEST.json'}:return False
    if path.name=='.env' or path.name.startswith('.env.') and path.name!='.env.example':return False
    if 'credentials' in path.name or path.name.endswith('token.json'):return False
    if path.suffix.lower() in {'.pkl','.pickle','.keras','.h5','.hdf5','.mat','.nc','.nc4','.zip','.pyc','.aux','.log','.out'}:return False
    return True


def main():
    entries=[]
    for path in sorted(ROOT.rglob('*')):
        if path.is_file() and is_public(path):
            entries.append(dict(path=path.relative_to(ROOT).as_posix(),bytes=path.stat().st_size,
                sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    assert not any(e['path']=='figures/main/study-area-integrated.pdf' for e in entries)
    manifest=dict(scheme='main',status='release_package_with_hotspot_extraction_source',created='2026-10-21',
        finalized='2026-10-22',repository='https://github.com/raflialfansyah/climate-informed-hotspot-models',
        contents='Option 2: code, processed aggregate inputs and saved results; source rights qualifications documented',files=entries)
    (ROOT/'provenance/RELEASE_MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print('Public candidate manifest records:',len(entries))


if __name__=='__main__':main()
