import itertools
import random
import sys
import tempfile
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from phylo.tree import Tree, parse, newick, validate, edges, enumerate_trees, prune
from phylo.alignment import read_fasta, load_dataset
from phylo.scoring import sankoff, lower_bound
from phylo.search import fitch, patterns, nni, exhaustive, search


def brute_site(t, a):
    internal = [v for v in t.adj if v not in t.labels]
    best = len(t.adj)
    for states in itertools.product('ACGT', repeat=len(internal)):
        assignment = dict(zip(internal,states))
        assignment.update({v:a[label] for v,label in t.labels.items()})
        best = min(best,sum(assignment[u]!=assignment[v] for u,v in edges(t)))
    return best


class TestScoring(unittest.TestCase):
    def test_all_quartet_patterns_against_brute_ancestral_assignments(self):
        pats = list(itertools.product('ACGT',repeat=4))
        a = {name:''.join(p[i] for p in pats) for i,name in enumerate('ABCD')}
        for t in enumerate_trees(a):
            expected = [brute_site(t,dict(zip('ABCD',p))) for p in pats]
            self.assertEqual(sankoff(t,a),expected)
            self.assertEqual(fitch(t,patterns(a)),sum(expected))

    def test_random_multistate_patterns(self):
        rng = random.Random(51927)
        for n in range(3,8):
            a = {chr(65+i):''.join(rng.choice('ACGT') for _ in range(20)) for i in range(n)}
            for t in itertools.islice(enumerate_trees(a),30):
                self.assertEqual(sum(sankoff(t,a)),fitch(t,patterns(a)))
                self.assertLessEqual(lower_bound(a),sum(sankoff(t,a)))

    def test_published_scores_and_exhaustive_optima(self):
        for dataset,score,count in [('phylip-dnapars',19,15),('phylip-dnapenny',8,10395)]:
            row,a=load_dataset(ROOT,dataset)
            self.assertEqual(sum(sankoff(parse((ROOT/row['baseline_tree']).read_text(),a),a)),score)
            best = None; seen=set(); minimum_count=0
            compiled=patterns(a)
            for t in enumerate_trees(a):
                key=newick(t); self.assertNotIn(key,seen); seen.add(key)
                s=fitch(t,compiled)
                self.assertEqual(s,sum(sankoff(t,a)))
                if best is None or s<best: best=s; minimum_count=1
                elif s==best: minimum_count+=1
            self.assertEqual(len(seen),count); self.assertEqual(best,score)
            if dataset=='phylip-dnapenny': self.assertEqual(minimum_count,9)

    def test_exhaustive_count_formula(self):
        for n,count in [(3,1),(4,3),(5,15),(6,105),(7,945)]:
            self.assertEqual(len({newick(t) for t in enumerate_trees([str(i) for i in range(n)])}),count)
        with self.assertRaises(ValueError): list(enumerate_trees('ABCDEFGHI'))

    def test_identical_constant_and_informative_sites(self):
        t=parse('(A,B,(C,D));')
        self.assertEqual(sankoff(t,dict(A='AA',B='AA',C='AC',D='AC')),[0,1])
        self.assertEqual(sum(sankoff(parse('(A,C,(B,D));'),dict(A='A',B='A',C='C',D='C'))),2)


class TestStructure(unittest.TestCase):
    def test_root_and_order_invariance(self):
        a=dict(A='ACGT',B='AGGT',C='CCGT',D='CCTA',E='GGTA')
        t=parse('((A,B),(C,(D,E)));',a)
        def subtree(v,p):
            if v in t.labels: return t.labels[v]
            return '('+','.join(subtree(w,v) for w in sorted(t.adj[v]) if w!=p)+')'
        for u,v in edges(t):
            q=parse('('+subtree(u,v)+','+subtree(v,u)+');',a)
            self.assertEqual(newick(q),newick(t)); self.assertEqual(sankoff(q,a),sankoff(t,a))
        self.assertEqual(newick(parse('(A:0.1,B:3e-9,(C:1,D:2):0);')),newick(parse('((D,C),B,A);')))
        self.assertEqual(newick(parse("('A',B,(C,D));")),newick(parse('(A,B,(C,D));')))

    def test_reject_newick(self):
        bad=['(A,A,(C,D));','(A,B,C,D);','(A,(B));','(A,B,(C,D))','(A,B,(C,D));garbage',
             '(A,B,(C,D));(A,B,C);','(A,B,(C,D)90);','(A,B,(C,D))[x];',
             '(A:-1,B,C);','(A:nan,B,C);','(A:inf,B,C);','(A:1e,B,C);','(A,,B);',
             "('unclosed,B,C);",'(A);','();','((A,B,C),(D,E));']
        for s in bad:
            with self.subTest(s=s),self.assertRaises(ValueError): parse(s)
        with self.assertRaises(ValueError): parse('(A,B,C);',{'A','B','D'})

    def test_graph_rejection(self):
        t=parse('(A,B,(C,D));'); t.adj[0].add(0)
        with self.assertRaises(ValueError): validate(t)
        t=parse('(A,B,(C,D));'); v=next(iter(t.adj)); w=next(iter(t.adj[v])); t.adj[v].remove(w)
        with self.assertRaises(ValueError): validate(t)

    def test_nni_degree_uniqueness_and_connectivity(self):
        for n in range(4,7):
            taxa=list('ABCDEF'[:n]); trees=list(enumerate_trees(taxa)); graph={}
            for t in trees:
                neighbors=list(nni(t))
                for q in neighbors: validate(q,taxa)
                keys={newick(q) for q in neighbors}
                self.assertEqual(len(keys),2*(n-3)); self.assertNotIn(newick(t),keys)
                graph[newick(t)]=keys
            seen=set(); pending=[newick(trees[0])]
            while pending:
                key=pending.pop()
                if key not in seen: seen.add(key); pending.extend(graph[key]-seen)
            self.assertEqual(seen,set(graph))

    def test_prune(self):
        t=parse('((A,B),(C,(D,(E,F))));')
        q=prune(t,{'A','C','F'}); self.assertEqual(set(q.labels.values()),{'A','C','F'})
        self.assertEqual(newick(q),'(A,(C,F));')


class TestInputsAndSearch(unittest.TestCase):
    def test_strict_fasta(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a.fa'
            for symbol in '-.?NRYSWKMBDHVXUacgt':
                p.write_text(f'>A\nA{symbol}\n>B\nAA\n>C\nAA\n')
                with self.subTest(symbol=symbol),self.assertRaises(ValueError): read_fasta(p)
            for s in ['>A\nA\n>A\nA\n>C\nA\n','>A\nA\n>B\nAA\n>C\nA\n','>A\nA\n>B\nA\n','>A bad\nA\n>B\nA\n>C\nA\n','A\n>B\nA\n>C\nA\n']:
                p.write_text(s)
                with self.assertRaises(ValueError): read_fasta(p)
            p.write_text('>A\nAU\n>B\nCU\n>C\nGU\n')
            self.assertEqual(read_fasta(p,'RNA'),dict(A='AT',B='CT',C='GT'))
            p.write_text('>A\nAT\n>B\nCU\n>C\nGU\n')
            with self.assertRaises(ValueError): read_fasta(p,'RNA')

    def test_reproducible_search(self):
        _,a=load_dataset(ROOT,'phylip-dnapars')
        t,r=search(a,1729,4,1000); t2,r2=search(a,1729,4,1000)
        self.assertEqual(newick(t),newick(t2)); self.assertEqual(r,r2)
        self.assertEqual(r['score'],19); self.assertEqual(sum(sankoff(t,a)),19)
        self.assertLessEqual(r['evaluations'],1000)
        for run in r['runs']:
            self.assertTrue(all(x>y for x,y in zip(run['history'],run['history'][1:])))
        baseline=parse((ROOT/'candidates/phylip-dnapars-baseline.nwk').read_text(),a)
        _,warm=search(a,0,1,100,start=baseline); self.assertEqual(warm['score'],19)
        _,small=search(a,1,3,3); self.assertEqual(small['evaluations'],3)
        with self.assertRaises(ValueError): search(a,1,0,1)

    def test_cli_rejects_wrong_score_and_taxa(self):
        import subprocess
        cmd=[sys.executable,str(ROOT/'phylo.py'),'verify','phylip-dnapars',str(ROOT/'candidates/phylip-dnapars-baseline.nwk'),'--claim','18']
        r=subprocess.run(cmd,capture_output=True,text=True)
        self.assertEqual(r.returncode,2); self.assertIn('exact score 19',r.stderr)

if __name__=='__main__': unittest.main()
