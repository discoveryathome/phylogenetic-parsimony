"""Rebuild expansion evidence while preserving every known incumbent.

Twenty predeclared paired seeds on four controls; three paired seeds on other
new open rows. Evaluation caps, not wall time, define the comparison.
"""
from pathlib import Path
import json,sys,time,argparse,platform
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from phylo.alignment import load_dataset,sha256,PROFILE
from phylo.tree import parse,newick
from phylo.scoring import sankoff
from phylo.search import search,exhaustive
from phylo.advanced import search_two
from phylo.bounds import paired_bound,verify_paired_bound
ROOT=Path(__file__).resolve().parents[1]
PANELS={'phylip-dnapenny','pythonidae-cytb-12','cetaceans-mt-12','ferula-nrdna-12'}

def save(path,value):
    (ROOT/path).parent.mkdir(parents=True,exist_ok=True)
    (ROOT/path).write_text(json.dumps(value,indent=2)+'\n')

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--datasets',nargs='+',help='Recompute only these rows, preserving all other expansion evidence')
    args=parser.parse_args()
    cases=json.loads((ROOT/'data/manifest.json').read_text())['datasets']
    if args.datasets and not set(args.datasets)<={c['id'] for c in cases}:parser.error('unknown dataset')
    old={r['dataset']:r for r in json.loads((ROOT/'discover/frontier-rows.json').read_text())}
    records=[];rows=[]
    if args.datasets:
        records=[r for r in json.loads((ROOT/'results/expansion-benchmark.json').read_text())['records'] if r['dataset'] not in args.datasets]
    for case in cases:
        if args.datasets and case['id'] not in args.datasets:
            rows.append(old[case['id']]);continue
        ident=case['id'];_,a=load_dataset(ROOT,ident)
        baseline=parse((ROOT/case['baseline_tree']).read_text(),a)
        base=sum(sankoff(baseline,a));best=(base,newick(baseline))
        if ident in old:
            previous=old[ident]
            if previous['alignment_sha256']!=case['sha256']:raise ValueError('changed alignment')
            t=parse((ROOT/previous['tree']).read_text(),a)
            score=sum(sankoff(t,a))
            if score!=previous['score']:raise ValueError('invalid incumbent')
            best=min(best,(score,newick(t)))
        for path in sorted((ROOT/'candidates').glob(ident+'-calibration.nwk')):
            t=parse(path.read_text(),a);best=min(best,(sum(sankoff(t,a)),newick(t)))
        # Every paired run uses the same random start, one restart, and a cap of 600.
        seeds=range(20) if ident in PANELS else range(3) if case['ntax']>8 else []
        for seed in seeds:
            for method,fn in [('nni',search),('two-nni',search_two)]:
                begin=time.perf_counter();t,result=fn(a,seed,1,600)
                verified=sum(sankoff(t,a))
                if verified!=result['score']:raise ValueError('independent score mismatch')
                path=f'candidates/{ident}-{method}-paired-{seed}.nwk'
                (ROOT/path).write_text(newick(t)+'\n')
                result.update(dataset=ident,alignment_sha256=case['sha256'],profile=PROFILE,
                              method=method,tree=path,tree_sha256=sha256(ROOT/path),
                              verified_score=verified,elapsed_seconds=round(time.perf_counter()-begin,6),
                              panel=ident in PANELS)
                records.append(result);best=min(best,(verified,newick(t)))
        # Honest seeded comparator-start baseline, also adopt every improvement.
        if case['ntax']>8:
            for method,fn in [('nni',search),('two-nni',search_two)]:
                t,result=fn(a,0,1,1800,baseline);verified=sum(sankoff(t,a))
                if verified!=result['score']:raise ValueError('independent score mismatch')
                path=f'candidates/{ident}-{method}-source-start.nwk'
                (ROOT/path).write_text(newick(t)+'\n')
                result.update(dataset=ident,alignment_sha256=case['sha256'],profile=PROFILE,
                              method=method,tree=path,tree_sha256=sha256(ROOT/path),
                              verified_score=verified,panel=False)
                records.append(result);best=min(best,(verified,newick(t)))
        if case['ntax']<=8:
            t,certificate=exhaustive(a)
            if sum(sankoff(t,a))!=certificate['score']:raise ValueError('exhaustive mismatch')
            bound=certificate['score'];best=min(best,(bound,newick(t)));method='exhaustive'
            evidence=f'results/{ident}-exhaustive.json';save(evidence,certificate)
        else:
            certificate=max((paired_bound(a,s) for s in range(20)),key=lambda c:c['bound'])
            if ident in old and old[ident]['bound_method']=='incompatible-pairs':
                previous=json.loads((ROOT/old[ident]['bound_evidence']).read_text())
                if (previous.get('dataset'),previous.get('alignment_sha256'),previous.get('profile'))!=(ident,case['sha256'],PROFILE):
                    raise ValueError('previous bound identity mismatch')
                if verify_paired_bound(a,previous)!=old[ident]['lower_bound']:raise ValueError('invalid previous bound')
                if previous['bound']>certificate['bound']:certificate=previous
            certificate.update(dataset=ident,alignment_sha256=case['sha256'],profile=PROFILE)
            bound=certificate['bound'];method='incompatible-pairs'
            evidence=f'results/{ident}-bound.json';save(evidence,certificate)
        path=f'candidates/{ident}-best.nwk';(ROOT/path).write_text(best[1]+'\n')
        row=dict(dataset=ident,alignment_sha256=case['sha256'],profile=PROFILE,score=best[0],
                 lower_bound=bound,tree=path,tree_sha256=sha256(ROOT/path),baseline_score=base,
                 published_score=case['published_score'],bound_method=method,bound_evidence=evidence,
                 status='settled' if best[0]==bound else 'open',evidence_level=['author-checked'],
                 scope='Only this fixed alignment and scoring profile; not a claim of biological truth',
                 reproduce=f'python3 phylo.py verify {ident} {path} --claim {best[0]}')
        rows.append(row)
        print(ident,'baseline',base,'best',best[0],'bound',bound,flush=True)
    save('results/expansion-benchmark.json',dict(schema='phylo-benchmark/v1',python=platform.python_version(),platform=platform.platform(),paired_seeds=list(range(20)),
         panel_datasets=sorted(PANELS),budget=600,restarts=1,
         caveat='Equal evaluation caps are not equal CPU cost or actual evaluations: strict NNI may stop early. Automated probes, not donor-session success measurements.',
         records=records))
    save('discover/frontier-rows.json',rows)

if __name__=='__main__':main()
