"""Execute the released notebook top-to-bottom with all scientific stages off."""
from pathlib import Path
import json
import os
import subprocess
import sys
import argparse
import re
import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preflight',action='store_true',help='Validate included processed inputs in a runtime copy, without fitting.')
    args=parser.parse_args()
    runtime = ROOT / 'validation/runtime'
    runtime.mkdir(parents=True, exist_ok=True)
    prefix = runtime / 'kernel'
    subprocess.run([sys.executable, '-m', 'ipykernel', 'install', '--prefix', str(prefix),
        '--name', 'hotspot-main-validation', '--display-name', 'Main scheme validation'],
        check=True, capture_output=True, text=True)
    os.environ['JUPYTER_PATH'] = str(prefix / 'share/jupyter') + os.pathsep + os.environ.get('JUPYTER_PATH', '')
    book = nbformat.read(ROOT / 'Hotspot_SameDay_Main.ipynb', as_version=4)
    nbformat.validate(book)
    controls=next(c for c in book.cells if c.cell_type=='code' and 'RUN_PREFLIGHT = False' in c.source)
    stages=['RUN_PREFLIGHT','RUN_MAIN','RUN_ABLATION','RUN_ROLLING','RUN_TEST','RUN_REPORTS']
    assert all(re.search(rf'^{stage} = False$',controls.source,re.M) for stage in stages), 'Validation requires distributed stage switches off.'
    if args.preflight:
        controls.source=controls.source.replace('RUN_PREFLIGHT = False','RUN_PREFLIGHT = True',1)
        original="OUTPUT_ROOT = globals().get('OUTPUT_ROOT', str(REPO / 'outputs_main'))"
        assert original in controls.source
        controls.source=controls.source.replace(original,'OUTPUT_ROOT = '+repr(str(runtime/'preflight_outputs')),1)
    client = NotebookClient(book, kernel_name='hotspot-main-validation', timeout=240,
        resources={'metadata': {'path': str(ROOT)}})
    executed = client.execute()
    nbformat.write(executed, runtime / ('preflight_execution.ipynb' if args.preflight else 'default_execution.ipynb'))
    errors = [o for c in executed.cells if c.cell_type == 'code' for o in c.outputs if o.output_type == 'error']
    assert not errors
    result = dict(passed=True, mode='top-to-bottom; processed preflight only' if args.preflight else 'top-to-bottom; all scientific stages off',
        code_cells_executed=sum(c.cell_type == 'code' for c in executed.cells),
        raw_data_loaded=False, estimator_fits=0, scientific_training_not_repeated=True)
    output='notebook_preflight_execution.json' if args.preflight else 'notebook_execution.json'
    (ROOT / 'validation'/output).write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
