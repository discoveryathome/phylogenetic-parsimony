"""Read-only evidence summary, paired comparisons, and matched-taxon gene conflict."""
from pathlib import Path
import json,sys,statistics
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from phylo.alignment import load_dataset
from phylo.tree import parse
from phylo.scoring import sankoff
from interpret import splits
ROOT=Path(__file__).resolve().parents[1]

def report():
    rows=json.loads((ROOT/'discover/frontier-rows.json').read_text())
    indexed={r['dataset']:r for r in rows}
    cases=json.loads((ROOT/'data/manifest.json').read_text())['datasets']
    bench=json.loads((ROOT/'results/expansion-benchmark.json').read_text())
    panels=[]
    for ident in bench['panel_datasets']:
        runs=[r for r in bench['records'] if r['dataset']==ident and r['panel']]
        a={r['seed']:r for r in runs if r['method']=='nni'}
        b={r['seed']:r for r in runs if r['method']=='two-nni'}
        if set(a)!=set(b) or set(a)!=set(bench['paired_seeds']):raise ValueError('incomplete paired panel')
        target=indexed[ident]['score']
        panels.append(dict(dataset=ident,seeds=len(a),cap=bench['budget'],
            nni_mean=statistics.mean(r['score'] for r in a.values()),
            two_nni_mean=statistics.mean(r['score'] for r in b.values()),
            two_nni_wins=sum(b[s]['score']<a[s]['score'] for s in a),
            ties=sum(b[s]['score']==a[s]['score'] for s in a),
            two_nni_losses=sum(b[s]['score']>a[s]['score'] for s in a),
            target=target,target_proven=indexed[ident]['status']=='settled',
            nni_hits=sum(r['score']==target for r in a.values()),
            two_nni_hits=sum(r['score']==target for r in b.values())))
    conflict=[]
    for n in (6,12,24):
        left=f'ferula-nrdna-{n}';right=f'ferula-plastid-{n}'
        _,a=load_dataset(ROOT,left);_,b=load_dataset(ROOT,right)
        if set(a)!=set(b):raise ValueError('cross-marker comparison requires identical taxa')
        t=parse((ROOT/indexed[left]['tree']).read_text(),a)
        u=parse((ROOT/indexed[right]['tree']).read_text(),b)
        conflict.append(dict(ntax=n,raw_rf_distance=len(splits(t)^splits(u)),
            nuclear_alignment=dict(nuclear_tree=sum(sankoff(t,a)),plastid_tree=sum(sankoff(u,a))),
            plastid_alignment=dict(nuclear_tree=sum(sankoff(t,b)),plastid_tree=sum(sankoff(u,b)))))
    return dict(fixed_alignments=len(rows),empirical_studies=len({c['source_group'] for c in cases if c['kind']=='empirical-derived'}),
        settled=sum(r['status']=='settled' for r in rows),open=sum(r['status']=='open' for r in rows),
        paired_panels=panels,ferula_comparison=conflict,
        caution='Scores are comparable only within one alignment. RF is descriptive, not support. Lower parsimony score does not prove true evolutionary history. These are automated probes, not observed donor-session success rates.')

if __name__=='__main__':print(json.dumps(report(),indent=2))
