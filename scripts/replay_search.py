"""Read-only full seed replay; checks trees and counters, ignores variable wall time."""
from pathlib import Path
import json,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from phylo.alignment import load_dataset
from phylo.tree import parse,newick
from phylo.search import search
from phylo.advanced import search_two
ROOT=Path(__file__).resolve().parents[1]
records=[]
for path in ('results/benchmark.json','results/expansion-benchmark.json'):
    records+=json.loads((ROOT/path).read_text())['records']
for record in records:
    case,a=load_dataset(ROOT,record['dataset'])
    start=parse((ROOT/case['baseline_tree']).read_text(),a) if record['initialization']=='supplied-first' else None
    fn=search_two if record.get('method')=='two-nni' else search
    t,r=fn(a,record['seed'],record['restarts'],record['max_evaluations'],start)
    for key,value in r.items():
        if value!=record[key]:raise SystemExit('Replay mismatch: '+record['dataset']+' '+key)
    if newick(t)!=(ROOT/record['tree']).read_text().strip():raise SystemExit('Replay topology mismatch')
    print(record['dataset'],record['seed'],'replayed',flush=True)
print('PASS: all seed runs reproduce trees, scores, traces and evaluation counts')
