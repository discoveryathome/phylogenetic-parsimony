"""Bounded two-move NNI descent; deterministic seeded starts and exact budget accounting."""
import random
from .search import patterns,fitch,nni,random_tree
from .tree import newick,validate


def search_two(alignment, seed, restarts=3, max_evaluations=1800, start=None):
    if restarts<1 or max_evaluations<restarts:raise ValueError('invalid search budget')
    if start is not None:validate(start,alignment)
    rng=random.Random(seed);compiled=patterns(alignment);per=max_evaluations//restarts
    best=None;best_key=None;runs=[]
    for restart in range(restarts):
        t=start.copy() if restart==0 and start is not None else random_tree(alignment,rng)
        score=fitch(t,compiled);used=1;initial=score;history=[score];radius=0
        while used<per:
            center_key=newick(t);seen={center_key};neighbors=[];chosen=None;value=score;complete=True
            for key,q in sorted((newick(q),q) for q in nni(t)):
                if used>=per:complete=False;break
                seen.add(key);v=fitch(q,compiled);used+=1;neighbors.append((key,q))
                if v<value:chosen,value=q,v
            if chosen is not None:
                t,score=chosen,value;history.append(score);continue
            if not complete:break
            radius=1
            for _,q in neighbors:
                for key,u in sorted((newick(u),u) for u in nni(q)):
                    if key in seen:continue
                    if used>=per:complete=False;break
                    seen.add(key);v=fitch(u,compiled);used+=1
                    if v<value:chosen,value=u,v
                if not complete:break
            if chosen is None:
                if complete:radius=2
                break
            t,score=chosen,value;history.append(score);radius=0
        validate(t,alignment);key=score,newick(t)
        if best_key is None or key<best_key:best,best_key=t,key
        runs.append({'restart':restart,'initial_score':initial,'score':score,'evaluations':used,'history':history,'certified_local_radius':radius})
    return best,{'seed':seed,'restarts':restarts,'max_evaluations':max_evaluations,'evaluations':sum(r['evaluations'] for r in runs),'score':best_key[0],'runs':runs,'algorithm':'radius-two-NNI-v1','initialization':'supplied-first' if start is not None else 'random'}
