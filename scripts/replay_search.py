"""Read-only full seed replay; checks trees and counters, ignores variable wall time."""
from pathlib import Path
import json,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from phylo.alignment import load_dataset
from phylo.tree import parse,newick
from phylo.search import search
ROOT=Path(__file__).resolve().parents[1]
for record in json.loads((ROOT/'results/benchmark.json').read_text())['records']:
    case,a=load_dataset(ROOT,record['dataset'])
    start=parse((ROOT/case['baseline_tree']).read_text(),a) if record['initialization']=='supplied-first' else None
    t,r=search(a,record['seed'],record['restarts'],record['max_evaluations'],start)
    for key,value in r.items():
        if value!=record[key]:raise SystemExit('Replay mismatch: '+record['dataset']+' '+key)
    if newick(t)!=(ROOT/record['tree']).read_text().strip():raise SystemExit('Replay topology mismatch')
    print(record['dataset'],record['seed'],'replayed',flush=True)
print('PASS: all seed runs reproduce trees, scores, traces and evaluation counts')
