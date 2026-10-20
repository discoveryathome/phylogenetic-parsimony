import argparse
import json
from pathlib import Path
from .alignment import load_dataset, sha256
from .tree import parse, newick
from .scoring import sankoff, lower_bound
from .search import search, exhaustive
from .advanced import search_two
from .bounds import paired_bound, verify_paired_bound

ROOT = Path(__file__).resolve().parents[2]

def main():
    p = argparse.ArgumentParser(description='Exact strict nucleotide parsimony verifier and baseline search')
    sub = p.add_subparsers(dest='command', required=True)
    for name in ('verify','search','exhaustive','inspect','bound','verify-bound'):
        q = sub.add_parser(name); q.add_argument('dataset')
        if name == 'verify':
            q.add_argument('tree', type=Path); q.add_argument('--claim', type=int, required=True)
        if name == 'verify-bound': q.add_argument('certificate',type=Path)
        if name == 'bound': q.add_argument('--seed',type=int,default=0)
        if name in ('search','exhaustive','bound'):
            q.add_argument('--out', type=Path, required=True)
        if name == 'search':
            q.add_argument('--method',choices=['nni','two-nni'],default='nni')
            q.add_argument('--seed', type=int, required=True); q.add_argument('--restarts',type=int,default=4)
            q.add_argument('--budget',type=int,default=10000); q.add_argument('--start',type=Path)
    args = p.parse_args()
    try:
        row,a = load_dataset(ROOT,args.dataset)
        if args.command == 'inspect':
            print(json.dumps({**row,'site_lower_bound':lower_bound(a)},indent=2)); return
        if args.command == 'bound':
            result=paired_bound(a,args.seed)
            result.update(dataset=row['id'],alignment_sha256=row['sha256'],profile=row['profile'])
            args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(result,indent=2)+'\n')
            print(json.dumps(result,indent=2));return
        if args.command == 'verify-bound':
            result=json.loads(args.certificate.read_text())
            if result.get('dataset')!=row['id'] or result.get('alignment_sha256')!=row['sha256'] or result.get('profile')!=row['profile']:raise ValueError('bound identity mismatch')
            print(json.dumps({'valid':True,'bound':verify_paired_bound(a,result)}));return
        if args.command == 'verify':
            t = parse(args.tree.read_text(),a); sites = sankoff(t,a)
            if sum(sites) != args.claim: raise ValueError(f'claim {args.claim} differs from exact score {sum(sites)}')
            result = {'valid':True,'score':sum(sites),'site_scores':sites,'tree_sha256':sha256(args.tree)}
        else:
            t,result = exhaustive(a) if args.command == 'exhaustive' else (search if args.method=='nni' else search_two)(a,args.seed,args.restarts,args.budget,parse(args.start.read_text(),a) if args.start else None)
            verified = sum(sankoff(t,a))
            if verified != result['score']: raise ValueError('Fitch/Sankoff disagreement')
            args.out.parent.mkdir(parents=True,exist_ok=True); args.out.write_text(newick(t)+'\n')
            result['tree'] = str(args.out); result['verified_score'] = verified
            result['tree_sha256'] = sha256(args.out)
        result.update(dataset=row['id'],alignment_sha256=row['sha256'],profile=row['profile'])
        print(json.dumps(result,indent=2))
    except (ValueError,OSError,KeyError,RecursionError) as e:
        p.exit(2,'REJECTED: '+str(e)+'\n')
