"""Reproducible deterministic quality benchmark; timings are descriptive, not speed claims."""
from pathlib import Path
import sys,json,time,platform
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from phylo.alignment import load_dataset,sha256,PROFILE
from phylo.tree import parse,newick
from phylo.scoring import sankoff,lower_bound
from phylo.search import search,exhaustive
ROOT=Path(__file__).resolve().parents[1]

def main():
    cases=json.loads((ROOT/'data/manifest.json').read_text())['datasets']
    records,frontier=[],[]
    for case in cases:
        ident=case['id']; _,a=load_dataset(ROOT,ident)
        base=parse((ROOT/case['baseline_tree']).read_text(),a)
        base_score=sum(sankoff(base,a)); best=(base_score,newick(base)); records_for_case=[]
        for seed in (17,1729,20261020,0):
            start=time.perf_counter()
            tree,result=search(a,seed,restarts=1 if seed == 0 else 3,max_evaluations=1800,start=base if seed == 0 else None)
            elapsed=time.perf_counter()-start
            verified=sum(sankoff(tree,a))
            if result['score']!=verified: raise RuntimeError('search/reference disagreement')
            path=f'candidates/{ident}-seed-{seed}.nwk'; (ROOT/path).write_text(newick(tree)+'\n')
            result.update(dataset=ident,alignment_sha256=case['sha256'],profile=PROFILE,baseline_score=base_score,published_score=case['published_score'],tree=path,tree_sha256=sha256(ROOT/path),verified_score=verified,elapsed_seconds=round(elapsed,6))
            records_for_case.append(result)
            best=min(best,(verified,newick(tree)))
        bound=lower_bound(a); optimum=None
        if case['ntax']<=8:
            tree,exact=exhaustive(a)
            if exact['score']!=sum(sankoff(tree,a)): raise RuntimeError('exhaustive/reference disagreement')
            (ROOT/f'results/{ident}-exhaustive.json').write_text(json.dumps(exact,indent=2)+'\n')
            optimum=exact; bound=exact['score']; best=min(best,(exact['score'],newick(tree)))
        path=f'candidates/{ident}-best.nwk'; (ROOT/path).write_text(best[1]+'\n')
        row=dict(dataset=ident,alignment_sha256=case['sha256'],profile=PROFILE,score=best[0],lower_bound=bound,tree=path,tree_sha256=sha256(ROOT/path),baseline_score=base_score,published_score=case['published_score'],bound_method='exhaustive' if optimum else 'sum-distinct-states-minus-one',bound_evidence=f'results/{ident}-exhaustive.json' if optimum else 'src/phylo/scoring.py',status='settled' if best[0]==bound else 'open',evidence_level=['author-checked'],scope='Only this fixed alignment and scoring profile; not a claim of biological truth',reproduce=f'python3 phylo.py verify {ident} {path} --claim {best[0]}')
        frontier.append(row); records.extend(records_for_case)
        print(ident,'baseline',base_score,'NNI',[r['score'] for r in records_for_case],'best',best[0],'bound',bound,flush=True)
    (ROOT/'results/benchmark.json').write_text(json.dumps(dict(seeds=[17,1729,20261020,0],python=platform.python_version(),platform=platform.platform(),timing_note='Descriptive wall time only. No controlled speed comparison or quiet-machine assumption.',records=records),indent=2)+'\n')
    (ROOT/'discover/frontier-rows.json').write_text(json.dumps(frontier,indent=2)+'\n')
if __name__=='__main__':main()
