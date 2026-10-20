from pathlib import Path
import argparse,datetime,json,sys,time
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src'))
from phylo.alignment import load_dataset,sha256,PROFILE
from phylo.tree import parse,newick
from phylo.scoring import sankoff
from spr import search

p=argparse.ArgumentParser()
p.add_argument('--budget',type=int,default=5000)
p.add_argument('--seed',type=int,default=1729)
p.add_argument('--plateau',action='store_true')
p.add_argument('--name',required=True)
args=p.parse_args()
output=ROOT/'results/donor-trial-001'
case,alignment=load_dataset(ROOT,'pythonidae-16s-12')
start_path=output/'start.nwk'
start=parse(start_path.read_text(),alignment)
begin=time.monotonic()
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
events=[]
def improved(t,score,evaluations):
    check_start=time.monotonic()
    exact=sum(sankoff(t,alignment))
    if exact!=score:raise ValueError('independent score disagreement')
    path=output/f'{args.name}-score-{score}.nwk'
    path.write_text(newick(t)+'\n')
    event=dict(at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        elapsed_seconds=time.monotonic()-begin,score=score,evaluations=evaluations,
        verifier_seconds=time.monotonic()-check_start,tree=str(path.relative_to(ROOT)),tree_sha256=sha256(path))
    events.append(event)
    (output/f'{args.name}-events.json').write_text(json.dumps(events,indent=2)+'\n')
    print(json.dumps(event),flush=True)
tree,result=search(alignment,start,args.budget,args.seed,args.plateau,improved)
score=sum(sankoff(tree,alignment))
if score!=result['score']:raise ValueError('independent score disagreement')
path=output/f'{args.name}.nwk';path.write_text(newick(tree)+'\n')
result.update(dataset=case['id'],alignment_sha256=case['sha256'],profile=PROFILE,
    algorithm_sha256=sha256(Path(__file__).with_name('spr.py')),
    start_tree_sha256=sha256(start_path),verified_score=score,tree=str(path.relative_to(ROOT)),
    tree_sha256=sha256(path),started_at=started,finished_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    elapsed_seconds=time.monotonic()-begin,events=events)
(output/f'{args.name}.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result),flush=True)
