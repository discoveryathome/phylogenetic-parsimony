"""Compare two topologies on exactly the same accepted characters; no biology inference."""
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from phylo.alignment import load_dataset
from phylo.tree import parse,edges
from phylo.scoring import sankoff
ROOT=Path(__file__).resolve().parents[1]

def splits(t):
    all_taxa=frozenset(t.labels.values()); result=set()
    for u,v in edges(t):
        seen={v}; stack=[u]; side=set()
        while stack:
            w=stack.pop()
            if w in seen:continue
            seen.add(w)
            if w in t.labels: side.add(t.labels[w])
            stack.extend(t.adj[w]-seen)
        other=all_taxa-side
        if len(side)>1 and len(other)>1:
            result.add(min(tuple(sorted(side)),tuple(sorted(other))))
    return result

def report(dataset):
    row,a=load_dataset(ROOT,dataset)
    baseline=parse((ROOT/row['baseline_tree']).read_text(),a)
    frontier=next(r for r in json.loads((ROOT/'discover/frontier-rows.json').read_text()) if r['dataset']==dataset)
    best=parse((ROOT/frontier['tree']).read_text(),a)
    b,s=sankoff(baseline,a),sankoff(best,a)
    return dict(dataset=dataset,baseline_score=sum(b),best_score=sum(s),raw_rf_distance=len(splits(baseline)^splits(best)),sites_improved=sum(x<y for x,y in zip(s,b)),sites_worsened=sum(x>y for x,y in zip(s,b)),sites_tied=sum(x==y for x,y in zip(s,b)),caution='Lower parsimony score does not prove true evolutionary history. This is a filtered mitochondrial gene alignment; no support probabilities or species-tree inference follow.')
if __name__=='__main__':print(json.dumps(report(sys.argv[1]),indent=2))
