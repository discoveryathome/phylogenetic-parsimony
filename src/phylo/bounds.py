"""Disjoint incompatible biallelic-site pairs give independently checkable bounds."""
import random
from .scoring import lower_bound


def paired_bound(alignment, seed=0):
    """Greedy matching, using bit masks. No optimality claim for the matching."""
    names=sorted(alignment); columns=list(zip(*(alignment[n] for n in names)))
    binary=[]; masks={}; full=(1<<len(names))-1
    for i,col in enumerate(columns):
        states=sorted(set(col))
        if len(states)==2:
            binary.append(i); masks[i]=sum(1<<j for j,x in enumerate(col) if x==states[0])
    rng=random.Random(seed);rng.shuffle(binary)
    used=set();pairs=[]
    for i in binary:
        if i in used:continue
        a=masks[i]
        for j in binary:
            if j==i or j in used:continue
            b=masks[j]
            if a&b and a&(~b&full) and (~a&full)&b and (~a&full)&(~b&full):
                pairs.append([i+1,j+1]);used.update((i,j));break
    certificate={'schema':'phylo-incompatible-pairs/v1','seed':seed,'pairs_1based':pairs,'base_bound':lower_bound(alignment),'bound':lower_bound(alignment)+len(pairs)}
    verify_paired_bound(alignment,certificate)
    return certificate


def verify_paired_bound(alignment, certificate):
    """Checks characters directly, independently of generator's bit representation."""
    if certificate.get('schema')!='phylo-incompatible-pairs/v1':raise ValueError('unknown bound certificate')
    width=len(next(iter(alignment.values())));used=set()
    pairs=certificate.get('pairs_1based')
    if not isinstance(pairs,list):raise ValueError('pairs must be a list')
    for pair in pairs:
        if not isinstance(pair,list) or len(pair)!=2:raise ValueError('pair needs two columns')
        i,j=pair
        if any(type(k) is not int or k<1 or k>width or k in used for k in pair) or i==j:raise ValueError('invalid/repeated bound column')
        left={s[i-1] for s in alignment.values()};right={s[j-1] for s in alignment.values()}
        observed={(s[i-1],s[j-1]) for s in alignment.values()}
        if len(left)!=2 or len(right)!=2 or len(observed)!=4:raise ValueError('pair is not incompatible biallelic characters')
        used.update(pair)
    base=lower_bound(alignment);bound=base+len(pairs)
    if certificate.get('base_bound')!=base or certificate.get('bound')!=bound:raise ValueError('wrong bound arithmetic')
    return bound
