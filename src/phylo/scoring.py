"""Reference verifier: Sankoff DP, independent of the search's Fitch recurrence."""
from .tree import validate


def sankoff(tree, alignment):
    validate(tree, alignment)
    if not alignment or len({len(s) for s in alignment.values()}) != 1 or not all(set(s) <= set('ACGT') and s for s in alignment.values()):
        raise ValueError('invalid normalized alignment')
    # Root at a degree-three internal vertex. No Fitch sets or pattern compression.
    root = min(v for v in tree.adj if v not in tree.labels)
    parent, order = {root: None}, [root]
    for v in order:
        for w in sorted(tree.adj[v]):
            if w != parent[v]: parent[w] = v; order.append(w)
    result = []
    inf = len(tree.adj) + 1  # greater than any feasible per-site edge cost
    for site in range(len(next(iter(alignment.values())))):
        costs = {}
        for v in reversed(order):
            if v in tree.labels:
                observed = alignment[tree.labels[v]][site]
                costs[v] = [0 if c == observed else inf for c in 'ACGT']
            else:
                children = [w for w in tree.adj[v] if parent.get(w) == v]
                costs[v] = [sum(min(costs[w][b] + (a != b) for b in range(4)) for w in children) for a in range(4)]
        result.append(min(costs[root]))
    return result


def lower_bound(alignment):
    """Each site with d distinct observed states requires at least d-1 changes."""
    return sum(len(set(col))-1 for col in zip(*alignment.values()))
