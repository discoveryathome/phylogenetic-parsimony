"""Deterministic seeded random-addition starts and steepest-descent NNI."""
from collections import Counter
import random
from .tree import edges, insert_leaf, star3, newick, enumerate_trees, validate


def patterns(alignment):
    taxa = sorted(alignment)
    bits = {'A':1, 'C':2, 'G':4, 'T':8}
    counts = Counter(zip(*(alignment[t] for t in taxa)))
    return taxa, [(tuple(bits[c] for c in p), n) for p,n in sorted(counts.items())]


def fitch(tree, compiled):
    taxa, pats = compiled
    leaf_index = {v:taxa.index(label) for v,label in tree.labels.items()}
    # A virtual degree-two root subdivides the anchor's incident edge.
    anchor = min(tree.labels, key=tree.labels.get)
    other = next(iter(tree.adj[anchor]))
    order, parent = [other], {other:anchor}
    for v in order:
        for w in sorted(tree.adj[v]):
            if w != parent[v]: parent[w] = v; order.append(w)
    internal_children = {v: tuple(w for w in sorted(tree.adj[v]) if w != parent[v]) for v in order if v not in tree.labels}
    operations = list(reversed(order))
    total = 0
    for pat, weight in pats:
        states, score = {}, 0
        for v in operations:
            if v in tree.labels: states[v] = pat[leaf_index[v]]
            else:
                u, w = internal_children[v]
                left, right = states[u], states[w]
                common = left & right
                states[v] = common or (left | right)
                if not common: score += 1
        if not (states[other] & pat[leaf_index[anchor]]): score += 1
        total += weight * score
    return total


def nni(tree):
    """Exactly 2(n-3) neighbors for a labeled binary unrooted tree."""
    for u,v in edges(tree):
        if u in tree.labels or v in tree.labels: continue
        a = sorted(tree.adj[u] - {v})[0]
        for b in sorted(tree.adj[v] - {u}):
            t = tree.copy()
            t.adj[u].remove(a); t.adj[a].remove(u)
            t.adj[v].remove(b); t.adj[b].remove(v)
            t.adj[u].add(b); t.adj[b].add(u)
            t.adj[v].add(a); t.adj[a].add(v)
            yield t


def random_tree(taxa, rng):
    names = sorted(taxa); rng.shuffle(names)
    t = star3(names[:3])
    for name in names[3:]: t = insert_leaf(t, rng.choice(edges(t)), name)
    return t


def search(alignment, seed, restarts=4, max_evaluations=10000, start=None):
    if restarts < 1 or max_evaluations < restarts: raise ValueError('invalid search budget')
    if start is not None: validate(start, alignment)
    rng, compiled = random.Random(seed), patterns(alignment)
    best, best_key, evaluations, runs = None, None, 0, []
    per_start = max_evaluations // restarts
    for restart in range(restarts):
        t = start.copy() if restart == 0 and start is not None else random_tree(alignment, rng)
        score = fitch(t, compiled); used = 1
        history = [score]; initial = score; converged = False
        while used < per_start:
            neighbors = sorted((newick(x), x) for x in nni(t))
            chosen, value = None, score
            scanned = 0
            for _, candidate in neighbors:
                if used == per_start: break
                s = fitch(candidate, compiled); used += 1; scanned += 1
                if s < value: chosen, value = candidate, s
            if chosen is None:
                converged = scanned == len(neighbors); break
            t, score = chosen, value; history.append(score)
        validate(t, alignment)
        key = score, newick(t)
        if best_key is None or key < best_key: best, best_key = t, key
        evaluations += used
        runs.append({'restart':restart,'initial_score':initial,'score':score,'evaluations':used,'history':history,'nni_local_optimum':converged})
    return best, {'seed':seed,'restarts':restarts,'max_evaluations':max_evaluations,'evaluations':evaluations,'score':best_key[0],'runs':runs,'algorithm':'random-addition-steepest-NNI-v1','initialization':'supplied-first' if start is not None else 'random'}


def exhaustive(alignment):
    compiled = patterns(alignment); best, count, ties, tree = None, 0, 0, None
    for t in enumerate_trees(alignment):
        count += 1; s = fitch(t, compiled)
        if best is None or s < best: best, ties, tree = s, 1, t
        elif s == best:
            ties += 1
            if newick(t) < newick(tree): tree = t
    return tree, {'trees':count, 'score':best, 'optimal_trees':ties}
