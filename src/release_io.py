"""Resolve packaged tables, including losslessly compressed CSVs."""
from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TABLES = json.loads((ROOT / 'results/TABLE_INDEX.json').read_text(encoding='utf-8'))


def read_table(name, **kwargs):
    kwargs.setdefault('float_precision', 'round_trip')
    return pd.read_csv(ROOT / TABLES[name], **kwargs)


def local_paths():
    path = ROOT / '.local_paths.json'
    if not path.exists():
        raise FileNotFoundError('Copy local_paths.example.json to .local_paths.json and configure authorized local inputs.')
    return json.loads(path.read_text(encoding='utf-8'))
