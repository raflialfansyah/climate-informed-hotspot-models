"""Check release metadata, guide links, excluded files and bounded secret patterns."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess
from urllib.parse import unquote
from build_release_manifest import is_public

ROOT=Path(__file__).resolve().parents[1]


def main():
    public={p.relative_to(ROOT).as_posix():p for p in ROOT.rglob('*') if p.is_file() and is_public(p)}
    required=['README.md','LICENSE','CITATION.cff','Hotspot_SameDay_Main.ipynb',
        'docs/SOURCE_ATTRIBUTION.md','docs/PUBLICATION_CHECKLIST.md',
        'data/processed/regional_daily_inputs.csv.gz','data/processed/sst_context.csv.gz']
    assert all(name in public for name in required)
    assert not any(name.startswith(('data/local/','validation/runtime/','generated/','outputs_main/')) or name=='.local_paths.json' for name in public)
    assert 'figures/main/study-area-integrated.pdf' not in public
    guides=[ROOT/'README.md',*(ROOT/'docs').glob('*.md'),*(ROOT/'data').rglob('README.md')]
    links=0;bad=[]
    for path in guides:
        contents=path.read_text(encoding='utf-8')
        assert '\u2014' not in contents and '\ufffd' not in contents,path
        for raw in re.findall(r'!?\[[^\]]*\]\(([^\n)]+)\)',contents):
            target=raw.strip().strip('<>').split('#')[0]
            if not target or re.match(r'^(?:https?://|mailto:)',target):continue
            candidate=(path.parent/unquote(target)).resolve()
            if not candidate.is_relative_to(ROOT) or not candidate.exists():bad.append((path.relative_to(ROOT).as_posix(),target))
            links+=1
    assert not bad,bad
    cff=(ROOT/'CITATION.cff').read_text(encoding='utf-8')
    assert 'repository-code: "https://github.com/raflialfansyah/climate-informed-hotspot-models"' in cff
    assert 'license: MIT' in cff and 'family-names: Nurdiati' in cff
    assert len(re.findall(r'^  - family-names:',cff,re.M))==6
    source=(ROOT/'docs/SOURCE_ATTRIBUTION.md').read_text(encoding='utf-8')
    assert all(term in source for term in ['NOAA','OISST','ERA5','10.24381/cds.adbb2d47','Attribution 4.0','processing','00 UTC'])
    checks={}
    for name in ['result_checks','feature_export_checks','processed_input_checks','notebook_execution']:
        checks[name]=json.loads((ROOT/f'validation/{name}.json').read_text(encoding='utf-8'))
        assert checks[name]['passed'],name
    patterns={
        'github_token':r'\b(?:gh[pousr]_[A-Za-z0-9]{32,}|github_pat_[A-Za-z0-9_]{40,})\b',
        'google_key':r'\bAIza[A-Za-z0-9_-]{30,}\b',
        'aws_key':r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b',
        'private_key':r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
    }
    findings=[];scanned=0
    for name,path in public.items():
        if path.suffix.lower() not in {'.py','.md','.json','.ipynb','.cff','.yml','.yaml','.toml','.txt'}:continue
        content=path.read_text(encoding='utf-8',errors='replace');scanned+=1
        for label,pattern in patterns.items():
            if re.search(pattern,content):findings.append(dict(path=name,pattern=label))
    assert not findings,findings
    # Compare what Git would include without staging, writing objects or changing configuration.
    git=shutil.which('git');git_checks=None
    if git and (ROOT/'.git').exists():
        payload=subprocess.check_output([git,'-C',str(ROOT),'ls-files','--cached','--others','--exclude-standard'],text=True).splitlines()
        expected=set(public)|{'provenance/RELEASE_MANIFEST.json'}
        assert set(payload)==expected,{'extra_in_git':sorted(set(payload)-expected),'excluded_from_git':sorted(expected-set(payload))}
        for name in ['src/main_scheme.py','analysis/verify_package.py','Hotspot_SameDay_Main.ipynb']:
            filtered=subprocess.check_output([git,'-C',str(ROOT),'hash-object','--path',name,name],text=True).strip()
            raw=subprocess.check_output([git,'-C',str(ROOT),'hash-object','--no-filters',name],text=True).strip()
            assert filtered==raw,('Unexpected checkout normalization',name)
        git_checks=dict(candidate_files=len(payload),ignore_rules_match_manifest=True,source_newline_conversion_disabled=True)
    report=dict(passed=True,guide_files_checked=len(guides),relative_links_checked=links,citation_authors=6,
        text_files_scanned=scanned,bounded_secret_findings=findings,source_attribution_checked=True,
        scientific_checks_passed=True,git_checks=git_checks,new_fits=0,new_model_inference=0,
        public_upload_performed=False,scope='Local technical and source-notice checks; not author approval or public-access verification')
    (ROOT/'validation/release_readiness.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
