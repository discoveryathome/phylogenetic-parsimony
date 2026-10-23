"""Independent finite controls for the research two-character certificate."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'src'))
from phylo.alignment import load_dataset
from phylo.bounds import verify_paired_bound
from phylo.scoring import sankoff
from phylo.tree import enumerate_trees
from research.multistate_pairs_20261023.generate import pair_bonus
from research.multistate_pairs_20261023.verify import binary_pair_ceiling, two_site_score, verify_certificate

PACKAGE = ROOT / 'research/multistate_pairs_20261023'


def patterns(size, prefix=(0,)):
    """All partitions into at most four states, modulo state-name permutations."""
    if len(prefix) == size:
        yield ''.join('ACGT'[state] for state in prefix)
    else:
        for state in range(min(3, max(prefix) + 1) + 1):
            yield from patterns(size, prefix + (state,))


class MultistatePairTests(unittest.TestCase):
    def test_all_character_pairs_on_three_to_six_taxa(self):
        checked = 0
        for size, count in [(3, 5), (4, 15), (5, 51), (6, 187)]:
            columns = list(patterns(size))
            self.assertEqual(len(columns), count)
            names = 'abcdef'[:size]
            alignment = {name: ''.join(column[i] for column in columns)
                         for i, name in enumerate(names)}
            scores = list(zip(*(sankoff(tree, alignment) for tree in enumerate_trees(names))))
            for i, left in enumerate(columns):
                for j in range(i, len(columns)):
                    right = columns[j]
                    exact = min(a + b for a, b in zip(scores[i], scores[j]))
                    self.assertEqual(two_site_score(left, right), exact, (size, left, right))
                    separate = len(set(left)) + len(set(right)) - 2
                    self.assertEqual(separate + pair_bonus(left, right), exact, (size, left, right))
                    checked += 1
        self.assertEqual(checked, 19039)

    def test_disconnected_cycles_and_repeated_taxa(self):
        left, right = 'AACCGGTT', 'ACACGTGT'
        self.assertEqual(two_site_score(left, right), 8)
        self.assertEqual(pair_bonus(left, right), 2)
        self.assertEqual(two_site_score(left + left, right + right), 8)
        permutation = [7, 2, 0, 5, 3, 1, 6, 4]
        self.assertEqual(two_site_score(''.join(left[i] for i in permutation),
                                       ''.join(right[i] for i in permutation)), 8)

    def test_existing_binary_certificate_meets_its_ceiling(self):
        _, alignment = load_dataset(ROOT, 'pythonidae-cytb-12')
        certificate = json.loads((ROOT / 'results/pythonidae-cytb-12-bound.json').read_text())
        ceiling = binary_pair_ceiling(alignment)
        self.assertEqual(ceiling['active_columns'], 98)
        self.assertEqual(ceiling['edges'], 2568)
        self.assertEqual(verify_paired_bound(alignment, certificate), ceiling['bound_upper_limit'])
        self.assertEqual(ceiling['bound_upper_limit'], 392)

    def test_saved_certificate_and_failure_controls(self):
        certificate = json.loads((PACKAGE / 'pythonidae-cytb-12.json').read_text())
        report = verify_certificate(certificate)
        self.assertEqual((report['base_bound'], report['bonus'], report['bound']), (343, 103, 446))
        self.assertEqual(report['pairs'], 80)
        first = certificate['pairs_1based'][0]
        invalid = [
            ('schema', 'phylo-incompatible-pairs/v1'),
            ('dataset', 'ferula-nrdna-6'), ('dataset', '../outside'), ('dataset', None),
            ('profile', 'different-profile'), ('alignment_sha256', '0' * 64),
            ('base_bound', 344), ('base_bound', 343.0), ('bound', 447), ('bound', True),
            ('pairs_1based', None), ('pairs_1based', {}),
            ('pairs_1based', [first, first]), ('pairs_1based', [[first[0], first[0]]]),
            ('pairs_1based', [[True, 2]]), ('pairs_1based', [[1.0, 2]]),
            ('pairs_1based', [[0, 2]]), ('pairs_1based', [[1, 648]]),
            ('pairs_1based', [[1, '2']]), ('pairs_1based', [[1, 2, 3]]),
            ('pairs_1based', ['12']), ('pairs_1based', [[]]),
        ]
        for key, value in invalid:
            with self.subTest(key=key, value=value):
                bad = copy.deepcopy(certificate)
                bad[key] = value
                with self.assertRaises(ValueError):
                    verify_certificate(bad)
        with self.assertRaises(ValueError):
            verify_certificate([])


if __name__ == '__main__':
    unittest.main()
