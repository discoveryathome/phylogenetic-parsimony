import unittest
from phylip_baseline import convert,parse,sankoff
from verify_results import raw_score
class AdapterTests(unittest.TestCase):
    def setUp(self):self.mapping={f'T{i:08d}':c for i,c in enumerate('abcd')};self.a=dict(zip('abcd',['A','C','C','A']))
    def test_binary_keeps_score(self):
        raw='((T00000000:0,T00000003:0):1,T00000001:0,T00000002:0)[0.5];'
        tree,n=convert(raw,self.mapping);self.assertEqual(n,0)
        self.assertEqual(sum(sankoff(parse(tree,self.a),self.a)),raw_score(raw,self.mapping,self.a))
    def test_multifurcation_is_explicit(self):
        raw='(T00000000,T00000001,T00000002,T00000003);';tree,n=convert(raw,self.mapping)
        self.assertEqual(n,1);self.assertLessEqual(sum(sankoff(parse(tree,self.a),self.a)),raw_score(raw,self.mapping,self.a))
    def test_root_degree_two_no_false_resolution(self):
        _,n=convert('((T00000000,T00000001),(T00000002,T00000003));',self.mapping);self.assertEqual(n,0)
    def test_no_silent_unknown_syntax(self):
        with self.assertRaises(ValueError):convert('(T00000000,T00000001,T00000002)[arbitrary];',self.mapping)
if __name__=='__main__':unittest.main()
