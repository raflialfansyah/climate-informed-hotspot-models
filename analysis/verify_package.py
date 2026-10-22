"""Verify packaged copies, gzip payloads, source syntax and release exclusions."""
from pathlib import Path
import ast
import gzip
import hashlib
import json
import re
from build_release_manifest import is_public

ROOT = Path(__file__).resolve().parents[1]


def digest(path, compressed=False):
    h = hashlib.sha256()
    opener = gzip.open if compressed else open
    with opener(path, 'rb') as f:
        for block in iter(lambda: f.read(8 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def main():
    source_manifest = json.loads((ROOT / 'provenance/COPY_MANIFEST.json').read_text(encoding='utf-8'))
    copies = source_manifest['files']
    transforms = json.loads((ROOT / 'provenance/CURRENT_TRANSFORMATIONS.json').read_text(encoding='utf-8'))['files']
    for record in copies:
        path = ROOT / record['destination']
        change = transforms.get(record['destination'])
        if change:
            assert change['original_sha256'] == record['destination_sha256'], path
            if change['operation'] == 'exclude_gadm_map_from_public_payload':
                assert not path.exists(), path
                continue
            assert change['operation'] == 'remove_gadm_geometry', path
            assert digest(path) == change['current_sha256'], path
            import numpy as np
            with np.load(path, allow_pickle=False) as data:
                assert 'coast' not in data.files and set(data.files) == set(change['retained_arrays'])
                for name, expected in change['retained_arrays'].items():
                    value=data[name]
                    assert list(value.shape)==expected['shape'] and str(value.dtype)==expected['dtype']
                    assert hashlib.sha256(value.tobytes()).hexdigest()==expected['sha256']
            continue
        assert path.is_file(), path
        assert digest(path) == record['destination_sha256'], path
        assert digest(path, record['compression'] != 'none') == record['source_sha256'], path
    syntax = []
    for path in list((ROOT / 'src').glob('*.py')) + list((ROOT / 'analysis').rglob('*.py')):
        ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
        syntax.append(path.relative_to(ROOT).as_posix())
    book = json.loads((ROOT / 'Hotspot_SameDay_Main.ipynb').read_text(encoding='utf-8'))
    code_cells = [c for c in book['cells'] if c['cell_type'] == 'code']
    for c in code_cells:
        compile(''.join(c['source']), '<cell>', 'exec')
        assert c['execution_count'] is None and not c['outputs']
    controls = ''.join(book['cells'][16]['source'])
    assert all(re.search(rf'^{name} = False$', controls, re.M) for name in
        ['RUN_PREFLIGHT','RUN_MAIN','RUN_ABLATION','RUN_ROLLING','RUN_TEST','RUN_REPORTS'])
    prohibited = {'.pkl', '.pickle', '.mat', '.nc', '.nc4', '.h5', '.hdf5', '.keras', '.zip'}
    unexpected = [p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*')
        if p.is_file() and p.suffix.lower() in prohibited and 'generated' not in p.relative_to(ROOT).parts
        and not p.is_relative_to(ROOT/'data/local') and not p.is_relative_to(ROOT/'outputs_main')
        and not p.is_relative_to(ROOT/'validation/runtime') and '.git' not in p.relative_to(ROOT).parts]
    assert not unexpected, unexpected
    docs = list((ROOT / 'docs').glob('*.md')) + [ROOT / 'README.md']
    assert all('\u2014' not in p.read_text(encoding='utf-8') for p in docs)
    assert 'lightweight' not in '\n'.join(''.join(c['source']) for c in book['cells']).lower()
    release=json.loads((ROOT/'provenance/RELEASE_MANIFEST.json').read_text(encoding='utf-8'))
    declared=[entry['path'] for entry in release['files']]
    assert len(declared)==len(set(declared)), 'Duplicate paths in release manifest'
    actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and is_public(p)}
    assert set(declared)==actual, {'unlisted':sorted(actual-set(declared)), 'missing':sorted(set(declared)-actual)}
    for entry in release['files']:
        relative=Path(entry['path'])
        assert not relative.is_absolute() and '..' not in relative.parts
        assert not relative.is_relative_to('data/local') and relative.as_posix()!='.local_paths.json'
        path=ROOT/relative
        assert path.stat().st_size==entry['bytes'] and digest(path)==entry['sha256'],relative
        assert entry['bytes'] < 100*1024*1024, ('GitHub single-file limit',relative)
    assert not any(e['path']=='figures/main/study-area-integrated.pdf' for e in release['files'])
    result = dict(passed=True, copied_files_verified=len(copies), python_files_compile=len(syntax),
        notebook_code_cells_compile=len(code_cells), stages_default_off=True, raw_data_and_model_binaries_absent=True,
        transformations_checked=len(transforms),coastline_geometry_excluded=True,
        manifest_files_verified=len(declared),manifest_coverage_complete=True,github_single_file_sizes_checked=True,
        new_fits=0,new_inference=0,repository_url=release['repository'],
        remote_publication_not_checked_by_this_validator=True)
    (ROOT / 'validation/package_checks.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
