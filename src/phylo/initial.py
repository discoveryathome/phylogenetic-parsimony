"""Deterministic neighbor joining from uncorrected Hamming distances (topology only)."""
from fractions import Fraction
from .tree import Tree,validate


def neighbor_joining(alignment):
    names=sorted(alignment); labels=dict(enumerate(names));adj={i:set() for i in labels}
    active=list(labels);distance={}
    for i in active:
        for j in active:
            distance[i,j]=Fraction(sum(x!=y for x,y in zip(alignment[names[i]],alignment[names[j]])))
    next_id=len(active)
    while len(active)>3:
        n=len(active);totals={i:sum(distance[i,k] for k in active) for i in active}
        _,i,j=min(((n-2)*distance[i,j]-totals[i]-totals[j],i,j) for i in active for j in active if i<j)
        u=next_id;next_id+=1;adj[u]={i,j};adj[i].add(u);adj[j].add(u)
        remaining=[k for k in active if k not in (i,j)]
        for k in remaining:distance[u,k]=distance[k,u]=(distance[i,k]+distance[j,k]-distance[i,j])/2
        distance[u,u]=Fraction(0);active=remaining+[u]
    adj[next_id]=set(active)
    for k in active:adj[k].add(next_id)
    return validate(Tree(adj,labels),alignment)
