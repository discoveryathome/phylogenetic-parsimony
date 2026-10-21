"""Offline reproduction: data provenance, independent scoring, exact bounds, regression tests."""
from pathlib import Path
import json,sys,subprocess,math
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from phylo.alignment import load_dataset,sha256,PROFILE
from phylo.tree import parse,enumerate_trees,newick
from phylo.scoring import sankoff,lower_bound
from phylo.bounds import verify_paired_bound
ROOT=Path(__file__).resolve().parents[1]

def require(condition,message):
    if not condition:raise ValueError(message)

def main():
    subprocess.run([sys.executable,str(ROOT/'scripts/curate.py'),'--check'],check=True)
    source_index=json.loads((ROOT/'sources/index.json').read_text())
    for record in source_index:
        require(sha256(ROOT/record['path'])==record['sha256'],'source hash mismatch: '+record['path'])
    rows=json.loads((ROOT/'discover/frontier-rows.json').read_text())
    datasets=json.loads((ROOT/'data/manifest.json').read_text())['datasets']
    require({r['dataset'] for r in rows}=={r['id'] for r in datasets},'missing frontier row')
    keys=[(r['dataset'],r['alignment_sha256'],r['profile']) for r in rows]
    require(len(keys)==len(set(keys)),'duplicate frontier key')
    benchmarks=json.loads((ROOT/'results/benchmark.json').read_text())['records']
    benchmarks+=json.loads((ROOT/'results/expansion-benchmark.json').read_text())['records']
    for r in rows:
        case,a=load_dataset(ROOT,r['dataset'])
        require(r['alignment_sha256']==case['sha256'] and r['profile']==PROFILE,'row identity mismatch')
        require(sha256(ROOT/r['tree'])==r['tree_sha256'],'tree hash mismatch')
        t=parse((ROOT/r['tree']).read_text(),a)
        require(sum(sankoff(t,a))==r['score'],'frontier score mismatch')
        baseline_score=sum(sankoff(parse((ROOT/case['baseline_tree']).read_text(),a),a))
        require(baseline_score==r['baseline_score'],'baseline score mismatch')
        if case['published_score'] is not None:require(baseline_score==case['published_score'],'published score mismatch')
        if r['bound_method']=='exhaustive':
            # Unit suite cross-checks every 5/8-taxon tree; separately verify empirical 6.
            if case['kind']=='empirical-derived':
                scores=[sum(sankoff(q,a)) for q in enumerate_trees(a)]
                expected=math.prod(range(1,2*len(a)-4,2))
                record=json.loads((ROOT/r['bound_evidence']).read_text())
                require(len(scores)==record['trees']==expected,'incomplete enumeration')
                require(min(scores)==record['score']==r['lower_bound'],'wrong exhaustive optimum')
                require(scores.count(min(scores))==record['optimal_trees'],'wrong tie count')
            else:
                record=json.loads((ROOT/r['bound_evidence']).read_text())
                require(record['trees']==math.prod(range(1,2*len(a)-4,2)),'incomplete enumeration')
                require(record['score']==case['published_score']==r['lower_bound'],'wrong tutorial bound')
        elif r['bound_method']=='incompatible-pairs':
            certificate=json.loads((ROOT/r['bound_evidence']).read_text())
            require(certificate['dataset']==r['dataset'] and certificate['alignment_sha256']==case['sha256'] and certificate['profile']==PROFILE,'bound identity mismatch')
            require(verify_paired_bound(a,certificate)==r['lower_bound'],'pair bound mismatch')
        else:require(r['lower_bound']==lower_bound(a),'lower bound mismatch')
        require(r['lower_bound']<=r['score'],'score below lower bound')
        require(r['status']==('settled' if r['lower_bound']==r['score'] else 'open'),'incorrect optimum status')
        for b in [b for b in benchmarks if b['dataset']==r['dataset']]:
            require(b['alignment_sha256']==case['sha256'] and b['profile']==PROFILE,'benchmark identity mismatch')
            require(sha256(ROOT/b['tree'])==b['tree_sha256'],'benchmark tree hash mismatch')
            score=sum(sankoff(parse((ROOT/b['tree']).read_text(),a),a))
            require(score==b['score']==b['verified_score'],'benchmark score mismatch')
            require(b['evaluations']<=b['max_evaluations'],'budget exceeded')
        print(r['dataset'],r['score'],r['status'],flush=True)
    working=json.loads((ROOT/'discover/working-frontier-rows.json').read_text())
    require({r['dataset'] for r in working}=={r['dataset'] for r in rows}, 'working row coverage mismatch')
    require(len(working)==len(rows), 'duplicate working rows')
    historical={r['dataset']:r for r in rows}
    for r in working:
        case,a=load_dataset(ROOT,r['dataset'])
        require(r['alignment_sha256']==case['sha256'] and r['profile']==PROFILE, 'working identity mismatch')
        require(sha256(ROOT/r['tree'])==r['tree_sha256'], 'working tree hash mismatch')
        require(sum(sankoff(parse((ROOT/r['tree']).read_text(),a),a))==r['score'], 'working score mismatch')
        require(r['lower_bound']==historical[r['dataset']]['lower_bound']<=r['score']<=historical[r['dataset']]['score'], 'invalid working bounds')
    manifest=json.loads((ROOT/'discover.json').read_text())
    require(type(manifest.get('review',{}).get('paused')) is bool,'review pause status must be explicit')
    catalog=json.loads((ROOT/'discover/catalog.json').read_text())
    require(sum(t['weight'] for t in catalog['tracks'])==100,'track weights must sum to 100')
    subprocess.run([sys.executable,'-m','unittest','discover','-s',str(ROOT/'tests'),'-v'],check=True)
    print('PASS: fixed data, baseline and candidate scores, exhaustive bounds, structural/negative tests')
if __name__=='__main__':main()
