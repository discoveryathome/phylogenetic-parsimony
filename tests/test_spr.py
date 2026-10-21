import unittest
from phylo.tree import enumerate_trees, newick, validate
from phylo.search import nni, patterns, fitch
from phylo.scoring import sankoff
from phylo.spr import neighbors, search


class SPRChecks(unittest.TestCase):
    def test_small_neighborhoods_reverse_nni_and_scoring(self):
        alignment = dict(a='AACG', b='ACGT', c='CCGA', d='CTAT', e='TTAG')
        trees = list(enumerate_trees(alignment))
        all_keys = {newick(t) for t in trees}
        neighborhoods = {}
        for tree in trees:
            key = newick(tree)
            adjacent = list(neighbors(tree))
            keys = {k for k, _ in adjacent}
            self.assertEqual(len(keys), len(adjacent))
            self.assertNotIn(key, keys)
            self.assertLessEqual(keys, all_keys)
            self.assertLessEqual({newick(t) for t in nni(tree)}, keys)
            for k, t in adjacent:
                validate(t, alignment)
                self.assertEqual(fitch(t, patterns(alignment)), sum(sankoff(t, alignment)))
            neighborhoods[key] = keys
        for key, keys in neighborhoods.items():
            for other in keys:
                self.assertIn(key, neighborhoods[other])

    def test_budget_replay_and_global_small_control(self):
        alignment = dict(a='AACG', b='ACGT', c='CCGA', d='CTAT', e='TTAG')
        start = next(enumerate_trees(alignment))
        exact = min(sum(sankoff(t, alignment)) for t in enumerate_trees(alignment))
        for plateau in (False, True):
            for budget in (1, 3, 1000):
                t, r = search(alignment, start, budget, 1729, plateau)
                u, s = search(alignment, start, budget, 1729, plateau)
                self.assertEqual((newick(t), r), (newick(u), s))
                self.assertLessEqual(r['evaluations'], budget)
                self.assertEqual(r['score'], sum(sankoff(t, alignment)))
            self.assertEqual(r['score'], exact)


if __name__ == '__main__':
    unittest.main(verbosity=2)
