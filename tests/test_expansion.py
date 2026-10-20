import copy
import itertools
import unittest
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from phylo.advanced import search_two
from phylo.bounds import paired_bound, verify_paired_bound
from phylo.initial import neighbor_joining
from phylo.search import nni
from phylo.scoring import sankoff
from phylo.tree import enumerate_trees, newick, parse


class ExpansionTests(unittest.TestCase):
    def test_pair_bound_exhaustive_binary_columns(self):
        names='abcd'
        columns=list(itertools.product('AC',repeat=4))
        trees=list(enumerate_trees(names))
        for left in columns:
            for right in columns:
                a={n:left[i]+right[i] for i,n in enumerate(names)}
                cert=paired_bound(a)
                self.assertLessEqual(verify_paired_bound(a,cert),
                                     min(sum(sankoff(t,a)) for t in trees))
        a=dict(a='AA',b='AC',c='CA',d='CC')
        cert=paired_bound(a)
        self.assertEqual(cert['bound'],3)
        for mutation in ('repeat','arithmetic','compatible','boolean'):
            bad=copy.deepcopy(cert)
            if mutation=='repeat':bad['pairs_1based']*=2
            if mutation=='arithmetic':bad['bound']+=1
            if mutation=='compatible':bad['pairs_1based']=[[1,1]]
            if mutation=='boolean':bad['pairs_1based']=[[True,2]]
            with self.assertRaises(ValueError):verify_paired_bound(a,bad)

    def test_two_move_budget_determinism_and_local_certificate(self):
        a=dict(a='AACCGG',b='AACCGA',c='CCAGGT',d='CCAAGT',e='AGAGGT',f='TTAAGT')
        for budget in (1,3,30,1000):
            t,r=search_two(a,17,1,budget)
            t2,r2=search_two(a,17,1,budget)
            self.assertEqual((newick(t),r),(newick(t2),r2))
            self.assertLessEqual(r['evaluations'],budget)
            self.assertEqual(sum(sankoff(t,a)),r['score'])
            if r['runs'][0]['certified_local_radius']==2:
                for neighbor in nni(t):
                    self.assertGreaterEqual(sum(sankoff(neighbor,a)),r['score'])
                    for second in nni(neighbor):
                        self.assertGreaterEqual(sum(sankoff(second,a)),r['score'])
        self.assertEqual(r['runs'][0]['certified_local_radius'],2)

    def test_neighbor_joining_known_quartet_and_order(self):
        a=dict(a='AAAA',b='AAAC',c='CCCC',d='CCCA')
        t=neighbor_joining(a)
        self.assertEqual(newick(t),newick(parse('((a,b),c,d);',a)))
        self.assertEqual(newick(t),newick(neighbor_joining(dict(reversed(list(a.items()))))))
