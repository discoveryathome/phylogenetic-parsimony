#!/usr/bin/env python3
"""Pinned PHYLIP comparison; no change to accepted or working frontier files."""
import argparse, hashlib, json, platform, re, subprocess, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src'))
from phylo.alignment import load_dataset
from phylo.tree import parse
from phylo.scoring import sankoff
OUT=Path(__file__).resolve().parent

def convert(raw, mapping):
    # PHYLIP emits only generated safe names, lengths, numeric tree weights.
    clean=re.sub(r'\[[0-9.eE+\-]+\]', '', raw)
    clean=re.sub(r':[0-9.eE+\-]+', '', clean)
    toks=re.findall(r'T\d{8}|[(),;]',clean)
    if ''.join(toks) != re.sub(r'\s','',clean): raise ValueError('unexpected output syntax')
    at=0; refinements=0
    def subtree(depth=0):
        nonlocal at,refinements
        if toks[at]!='(':
            value=mapping[toks[at]];at+=1;return value
        at+=1;children=[subtree(depth+1)]
        while toks[at]==',':at+=1;children.append(subtree(depth+1))
        if toks[at]!=')':raise ValueError('bad output')
        at+=1
        # Deterministic zero-length resolution. Every resulting witness is rescored.
        while len(children)>(3 if depth==0 else 2):
            children[:2]=['('+children[0]+','+children[1]+')'];refinements+=1
        return '('+','.join(children)+')'
    result=subtree()+';\n'
    if toks[at:]!=[';']:raise ValueError('extra output')
    return result,refinements

def main():
    p=argparse.ArgumentParser();p.add_argument('--binary',type=Path,required=True);p.add_argument('--timeout',type=float,default=60);a=p.parse_args()
    binary=a.binary.resolve()
    rows=json.loads((ROOT/'discover/working-frontier-rows.json').read_text())
    results=[]
    for row in rows:
        meta,alignment=load_dataset(ROOT,row['dataset'])
        mapping={f'T{i:08d}':name for i,name in enumerate(alignment)}
        for seed in (13,37,101):
            run=OUT/'runs'/row['dataset']/str(seed);run.mkdir(parents=True,exist_ok=False)
            infile=f'{len(alignment)} {meta["nchar"]}\n'+''.join(f'{key:10s}{alignment[name]}\n' for key,name in mapping.items())
            (run/'infile').write_text(infile);(run/'labels.json').write_text(json.dumps(mapping,indent=2)+'\n')
            menu=f'V\n100\nJ\n{seed}\n10\n2\nY\n'
            (run/'menu.txt').write_text(menu)
            start=time.perf_counter()
            result={'dataset':row['dataset'],'alignment_sha256':meta['sha256'],'profile':meta['profile'],'seed':seed,'jumbles':10,'saved_tree_cap':100,'timeout_seconds':a.timeout,'previous_score':row['score'],'lower_bound':row['lower_bound']}
            try:
                proc=subprocess.run([str(binary)],input=menu,text=True,cwd=run,capture_output=True,timeout=a.timeout)
                (run/'console.txt').write_text(proc.stdout+proc.stderr)
                if proc.returncode:raise ValueError(f'exit {proc.returncode}')
                scores=[];resolutions=[]
                raw=(run/'outtree').read_text();trees=[x+';' for x in raw.split(';') if x.strip()]
                claimed=re.findall(r'requires a total of\s+([0-9.]+)',(run/'outfile').read_text())
                if not claimed:raise ValueError('missing PHYLIP score')
                reported={float(x) for x in claimed}
                for i,tree in enumerate(trees):
                    newick,n=convert(tree,mapping);score=sum(sankoff(parse(newick,alignment),alignment))
                    if score>max(reported):raise ValueError('resolved witness worse than reported score')
                    if not n and score not in reported:raise ValueError('binary witness score mismatch')
                    (run/f'tree-{i:03d}.nwk').write_text(newick);scores.append(score);resolutions.append(n)
                if not scores:raise ValueError('no trees')
                best=min(range(len(scores)),key=scores.__getitem__)
                result.update(status='verified',score=scores[best],reported_scores=sorted(reported),all_scores=scores,resolution_counts=resolutions,tree=str((run/f'tree-{best:03d}.nwk').relative_to(ROOT)),tree_sha256=hashlib.sha256((run/f'tree-{best:03d}.nwk').read_bytes()).hexdigest())
            except subprocess.TimeoutExpired as e:
                (run/'console.txt').write_bytes(e.stdout or b'');result.update(status='timeout')
            result['wall_seconds']=round(time.perf_counter()-start,6);results.append(result)
            (OUT/'results.json').write_text(json.dumps({'software':'PHYLIP dnapars 3.697','source_url':'https://phylipweb.github.io/phylip/download/phylip-3.697.tar.gz','binary_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'platform':platform.platform(),'runs':results},indent=2)+'\n')
            print(row['dataset'],seed,result['status'],result.get('score'),result['wall_seconds'],flush=True)
if __name__=='__main__':main()
