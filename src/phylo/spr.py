"""Experimental unrooted SPR and optional bounded traversal of equal-score trees.

Method background: https://phylipweb.github.io/phylip/doc/main.html
See "Global rearrangements". Original implementation; no external package.
"""
import random
from phylo.tree import edges, newick, validate
from phylo.search import patterns, fitch


def neighbors(tree):
    """Cut each oriented edge, suppress its parent, and regraft onto every remaining edge."""
    original = newick(tree)
    seen = {original}
    for left, right in edges(tree):
        for subtree, parent in ((left, right), (right, left)):
            if parent in tree.labels:
                continue  # Complement has one taxon and no regrafting edge.
            cut = tree.copy()
            cut.adj[subtree].remove(parent)
            cut.adj[parent].remove(subtree)
            a, b = sorted(cut.adj.pop(parent))
            cut.adj[a].remove(parent)
            cut.adj[b].remove(parent)
            cut.adj[a].add(b)
            cut.adj[b].add(a)
            # Regraft only into the complement, never into the detached subtree.
            complement = set()
            stack = [a]
            while stack:
                v = stack.pop()
                if v not in complement:
                    complement.add(v)
                    stack.extend(cut.adj[v] - complement)
            for x, y in edges(cut):
                if x not in complement or y not in complement:
                    continue
                t = cut.copy()
                t.adj[x].remove(y)
                t.adj[y].remove(x)
                t.adj[x].add(parent)
                t.adj[y].add(parent)
                t.adj[subtree].add(parent)
                t.adj[parent] = {x, y, subtree}
                key = newick(t)  # Includes the graph validator.
                if key not in seen:
                    seen.add(key)
                    yield key, t


def search(alignment, start, budget=5000, seed=1729, plateau=False, on_improvement=None):
    if budget < 1:
        raise ValueError('positive budget required')
    validate(start, alignment)
    rng = random.Random(seed)
    compiled = patterns(alignment)
    tree = start.copy()
    key = newick(tree)
    score = fitch(tree, compiled)
    cache = {key: score}
    initial = score
    history = [score]
    pending = [(key, tree)]
    queued = {key}
    expanded = set()
    complete = False
    while pending and len(cache) < budget:
        center_key, center = pending.pop(0)
        if center_key in expanded:
            continue
        expanded.add(center_key)
        candidates = sorted(neighbors(center))
        best = (score, key, tree)
        equal = []
        scanned_all = True
        for candidate_key, candidate in candidates:
            if candidate_key not in cache:
                if len(cache) >= budget:
                    scanned_all = False
                    break
                cache[candidate_key] = fitch(candidate, compiled)
            value = cache[candidate_key]
            if value < best[0] or (value == best[0] and value < score and candidate_key < best[1]):
                best = (value, candidate_key, candidate)
            elif value == score and candidate_key not in queued:
                equal.append((candidate_key, candidate))
        if best[0] < score:
            score, key, tree = best
            history.append(score)
            pending = [(key, tree)]
            queued = {key}
            expanded = set()
            if on_improvement is not None:
                on_improvement(tree, score, len(cache))
        elif plateau:
            rng.shuffle(equal)
            pending.extend(equal)
            queued.update(k for k, _ in equal)
        else:
            complete = scanned_all
            break
        if not scanned_all:
            break
        if not pending:
            complete = True
    validate(tree, alignment)
    return tree, dict(algorithm='experimental-SPR-plateau-v1' if plateau else 'experimental-SPR-strict-v1',
        seed=seed, budget=budget, evaluations=len(cache), initial_score=initial,
        score=score, history=history, expanded_topologies=len(expanded),
        completed_search_region=complete,
        completion_scope='reachable equal-score SPR component and outgoing SPR moves' if plateau else 'one SPR neighborhood')
