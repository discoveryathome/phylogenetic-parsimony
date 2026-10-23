"""Research-only two-site certificate checker; no generator or search imports."""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
from phylo.alignment import load_dataset, PROFILE


def two_site_score(left, right):
    """Exact TWO-character optimum via Prim's MST (Bruen & Bryant, Thm. 5.2)."""
    observed = sorted(set(zip(left, right)))
    distances = [3] * len(observed)
    distances[0] = 0
    used, total = set(), 0
    for _ in observed:
        cost, i = min((distances[i], i) for i in range(len(observed)) if i not in used)
        total += cost
        used.add(i)
        for j, target in enumerate(observed):
            distance = sum(a != b for a, b in zip(observed[i], target))
            distances[j] = min(distances[j], distance)
    return total


def binary_pair_ceiling(alignment):
    """Every old-style pair consumes two of these active biallelic columns."""
    columns = list(zip(*alignment.values()))
    binary = [i for i, column in enumerate(columns) if len(set(column)) == 2]
    active, edges = set(), 0
    for position, i in enumerate(binary):
        for j in binary[position + 1:]:
            if len(set(zip(columns[i], columns[j]))) == 4:
                active.update((i, j))
                edges += 1
    base = sum(len(set(column)) - 1 for column in columns)
    return {'biallelic_columns': len(binary), 'active_columns': len(active),
            'edges': edges, 'max_pairs_upper_bound': len(active) // 2,
            'bound_upper_limit': base + len(active) // 2}


def verify_certificate(certificate):
    if not isinstance(certificate, dict) or certificate.get('schema') != 'phylo-multistate-pairs/v1':
        raise ValueError('unknown bound certificate')
    dataset = certificate.get('dataset')
    if not isinstance(dataset, str):
        raise ValueError('dataset must be a string')
    case, alignment = load_dataset(ROOT, dataset)
    if certificate.get('alignment_sha256') != case['sha256'] or certificate.get('profile') != PROFILE:
        raise ValueError('certificate identity mismatch')
    columns = list(zip(*alignment.values()))
    singles = [len(set(column)) - 1 for column in columns]
    base = sum(singles)
    pairs = certificate.get('pairs_1based')
    if not isinstance(pairs, list):
        raise ValueError('pairs must be a list')
    used, bonuses = set(), []
    for pair in pairs:
        if not isinstance(pair, list) or len(pair) != 2:
            raise ValueError('pair needs exactly two columns')
        i, j = pair
        if (any(type(k) is not int or k < 1 or k > len(columns) or k in used for k in pair)
                or i == j):
            raise ValueError('invalid/repeated bound column')
        used.update(pair)
        joint = two_site_score(columns[i - 1], columns[j - 1])
        bonuses.append(joint - singles[i - 1] - singles[j - 1])
    bound = base + sum(bonuses)
    if any(type(certificate.get(key)) is not int or certificate[key] != value
           for key, value in [('base_bound', base), ('bound', bound)]):
        raise ValueError('wrong bound arithmetic')
    return {'valid': True, 'dataset': dataset, 'alignment_sha256': case['sha256'],
            'profile': PROFILE, 'base_bound': base, 'bound': bound,
            'pairs': len(pairs), 'bonus': sum(bonuses),
            'pair_bonus_counts': dict(sorted(Counter(bonuses).items())),
            'binary_pair_ceiling': binary_pair_ceiling(alignment)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate', type=Path)
    args = parser.parse_args()
    print(json.dumps(verify_certificate(json.loads(args.certificate.read_text())), sort_keys=True))


if __name__ == '__main__':
    main()
