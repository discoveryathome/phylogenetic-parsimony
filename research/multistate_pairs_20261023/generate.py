"""Greedy disjoint two-site bounds; Bruen & Bryant (2008), Theorem 4.2."""
import argparse
import json
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
from phylo.alignment import load_dataset, PROFILE


def pair_bonus(left, right):
    """Cycle rank of the bipartite state-intersection graph, using union/find."""
    observed = set(zip(left, right))
    parent = {(side, state): (side, state)
              for side, column in enumerate((left, right)) for state in column}

    def find(vertex):
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for a, b in sorted(observed):
        parent[find((0, a))] = find((1, b))
    components = len({find(vertex) for vertex in parent})
    return len(observed) - len(parent) + components


def generate(dataset, seeds=100):
    if type(seeds) is not int or seeds < 1:
        raise ValueError('seeds must be a positive integer')
    case, alignment = load_dataset(ROOT, dataset)
    columns = list(zip(*(alignment[name] for name in sorted(alignment))))
    base = sum(len(set(column)) - 1 for column in columns)
    variable = [i for i, column in enumerate(columns) if len(set(column)) > 1]
    edges = []
    for position, i in enumerate(variable):
        for j in variable[position + 1:]:
            weight = pair_bonus(columns[i], columns[j])
            if weight:
                edges.append((weight, i, j))
    best = None
    trials = []
    for seed in range(seeds):
        ordered = edges.copy()
        random.Random(seed).shuffle(ordered)
        ordered.sort(key=lambda edge: -edge[0])
        used, pairs, bonus = set(), [], 0
        for weight, i, j in ordered:
            if i not in used and j not in used:
                used.update((i, j))
                pairs.append([i + 1, j + 1])
                bonus += weight
        trials.append({'seed': seed, 'bound': base + bonus, 'pairs': len(pairs)})
        if best is None or base + bonus > best['bound']:
            best = {
                'schema': 'phylo-multistate-pairs/v1',
                'dataset': dataset,
                'alignment_sha256': case['sha256'],
                'profile': PROFILE,
                'base_bound': base,
                'bound': base + bonus,
                'pairs_1based': pairs,
                'seed': seed,
            }
    best['search'] = {
        'method': 'greedy-descending-cycle-rank/v1',
        'optimal_matching_claimed': False,
        'trials': trials,
    }
    return best


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('dataset')
    parser.add_argument('--seeds', type=int, default=100)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    certificate = generate(args.dataset, args.seeds)
    from verify import verify_certificate
    report = verify_certificate(certificate)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(certificate, indent=2) + '\n')
    print(json.dumps(report, sort_keys=True))


if __name__ == '__main__':
    main()
