#!/usr/bin/env python3
"""Replay all mature-program witnesses, including raw multifurcating scores."""
import hashlib,json,re,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from phylip_baseline import ROOT,convert,load_dataset,parse,sankoff

def raw_score(raw,mapping,alignment):
    # Separate direct DP on PHYLIP's possibly multifurcating rooted syntax.
    clean=re.sub(r'\[[0-9.eE+\-]+\]|:[0-9.eE+\-]+','',raw)
    tokens=re.findall(r'T\d{8}|[(),;]',clean);at=0
    if ''.join(tokens)!=re.sub(r'\s','',clean):raise ValueError('unexpected raw tree')
    def read():
        nonlocal at
        if tokens[at]!='(':
            x=mapping[tokens[at]];at+=1;return x
        at+=1;kids=[read()]
        while tokens[at]==',':at+=1;kids.append(read())
        assert tokens[at]==')';at+=1;return kids
    tree=read();assert tokens[at:]==[';']
    def cost(v,col):
        if isinstance(v,str):return [0 if c==alignment[v][col] else 10**6 for c in 'ACGT']
        child=[cost(w,col) for w in v]
        return [sum(min(x[b]+(a!=b) for b in range(4)) for x in child) for a in range(4)]
    return sum(min(cost(tree,col)) for col in range(len(next(iter(alignment.values())))))

def main():
    report=json.loads((HERE/'results.json').read_text());count=0;resolved=0;changed=0;summary=[]
    for row in report['runs']:
        assert row['status']=='verified'
        meta,a=load_dataset(ROOT,row['dataset']);assert row['alignment_sha256']==meta['sha256'];assert row['profile']==meta['profile']
        run=HERE/'runs'/row['dataset']/str(row['seed']);mapping=json.loads((run/'labels.json').read_text())
        expected=f'{len(a)} {meta["nchar"]}\n'+''.join(f'{key:10s}{a[name]}\n' for key,name in mapping.items())
        assert (run/'infile').read_text()==expected
        reported={float(x) for x in re.findall(r'requires a total of\s+([0-9.]+)',(run/'outfile').read_text())}
        assert reported==set(row['reported_scores'])
        raw=[x+';' for x in (run/'outtree').read_text().split(';') if x.strip()]
        assert len(raw)==len(row['all_scores'])
        for i,x in enumerate(raw):
            source_score=raw_score(x,mapping,a);assert source_score in row['reported_scores']
            tree,n=convert(x,mapping);path=run/f'tree-{i:03d}.nwk';assert n==row['resolution_counts'][i]
            # The corrected converter retains a degree-three root; equivalent topology.
            assert path.read_text()==tree
            score=sum(sankoff(parse(tree,a),a));assert score==row['all_scores'][i];assert score<=source_score
            count+=1;resolved+=bool(n);changed+=(score!=source_score)
        assert row['score']==min(row['all_scores'])==sum(sankoff(parse((ROOT/row['tree']).read_text(),a),a))
        assert row['tree_sha256']==hashlib.sha256((ROOT/row['tree']).read_bytes()).hexdigest()
        summary.append({'dataset':row['dataset'],'seed':row['seed'],'raw_score_verified':True})
    print(json.dumps({'status':'PASS','runs':len(summary),'witnesses':count,'resolved_multifurcating_witnesses':resolved,'score_changes_from_resolution':changed},indent=2))
if __name__=='__main__':main()
