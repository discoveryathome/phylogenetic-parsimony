"""Strict Newick subset and undirected binary topology operations. No dependencies."""
from dataclasses import dataclass
import re
from decimal import Decimal

@dataclass
class Tree:
    adj: dict
    labels: dict

    def copy(self):
        return Tree({v: set(ns) for v, ns in self.adj.items()}, dict(self.labels))


def validate(tree, taxa=None):
    a, labels = tree.adj, tree.labels
    if len(labels) < 3 or len(set(labels.values())) != len(labels):
        raise ValueError('need at least three distinct leaf labels')
    if not set(labels) <= set(a):
        raise ValueError('label refers to absent vertex')
    for v, ns in a.items():
        if v in ns or any(w not in a or v not in a[w] for w in ns):
            raise ValueError('invalid undirected adjacency')
        if len(ns) != (1 if v in labels else 3):
            raise ValueError('leaf degree must be 1 and internal degree 3')
    seen, stack = set(), [next(iter(a))]
    while stack:
        v = stack.pop()
        if v not in seen:
            seen.add(v)
            stack.extend(a[v] - seen)
    if len(seen) != len(a) or sum(map(len, a.values())) != 2 * (len(a) - 1):
        raise ValueError('graph must be connected and acyclic')
    if len(a) != 2 * len(labels) - 2:
        raise ValueError('incorrect binary tree vertex count')
    if taxa is not None and set(labels.values()) != set(taxa):
        raise ValueError('tree leaves must match alignment taxa exactly')
    return tree


def parse(text, taxa=None):
    if len(text) > 1_000_000:
        raise ValueError('Newick exceeds 1 MB limit')
    i, adj, labels = 0, {}, {}
    def ws():
        nonlocal i
        while i < len(text) and text[i].isspace(): i += 1
    def name():
        nonlocal i
        ws()
        if i < len(text) and text[i] == "'":
            i += 1
            value = ''
            while i < len(text):
                if text[i] == "'":
                    i += 1
                    if i < len(text) and text[i] == "'":
                        value += "'"; i += 1
                    else: return value
                else: value += text[i]; i += 1
            raise ValueError('unterminated quoted label')
        m = re.match(r'[A-Za-z0-9_.-]+', text[i:])
        if not m: raise ValueError('missing or unsupported label')
        i += len(m[0]); return m[0]
    def node(depth=0):
        nonlocal i
        if depth > 200: raise ValueError('Newick nesting limit exceeded')
        ws(); v = len(adj); adj[v] = set()
        if i < len(text) and text[i] == '(':
            i += 1
            while True:
                c = node(depth + 1); adj[v].add(c); adj[c].add(v); ws()
                if i < len(text) and text[i] == ',': i += 1; continue
                if i >= len(text) or text[i] != ')': raise ValueError('expected closing parenthesis')
                i += 1; break
            if len(adj[v]) not in (2, 3): raise ValueError('unary nodes/polytomies unsupported')
        else:
            labels[v] = name()
            if not labels[v]: raise ValueError('empty label')
        ws()
        if i < len(text) and text[i] == ':':
            i += 1; ws()
            m = re.match(r'(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?', text[i:])
            if not m or not Decimal(m[0]).is_finite(): raise ValueError('invalid branch length')
            i += len(m[0]); ws()
        return v
    root = node(); ws()
    if i >= len(text) or text[i] != ';' or text[i+1:].strip():
        raise ValueError('expected one tree with final semicolon; labels/comments unsupported internally')
    if len(adj[root]) == 2:
        u, v = sorted(adj.pop(root))
        adj[u].remove(root); adj[v].remove(root); adj[u].add(v); adj[v].add(u)
    return validate(Tree(adj, labels), taxa)


def edges(tree):
    return sorted((v, w) for v in tree.adj for w in tree.adj[v] if v < w)


def newick(tree):
    validate(tree)
    anchor = min(tree.labels, key=tree.labels.get)
    def quote(s):
        return s if re.fullmatch(r'[A-Za-z0-9_.-]+', s) else "'" + s.replace("'", "''") + "'"
    def descend(v, p):
        if v in tree.labels: return quote(tree.labels[v])
        return '(' + ','.join(sorted(descend(w, v) for w in tree.adj[v] if w != p)) + ')'
    other = next(iter(tree.adj[anchor]))
    return '(' + quote(tree.labels[anchor]) + ',' + descend(other, anchor) + ');'


def insert_leaf(tree, edge, label):
    t = tree.copy(); u, v = edge; x = max(t.adj) + 1; y = x + 1
    t.adj[u].remove(v); t.adj[v].remove(u)
    t.adj[u].add(x); t.adj[v].add(x)
    t.adj[x] = {u, v, y}; t.adj[y] = {x}; t.labels[y] = label
    return t


def star3(taxa):
    return Tree({0:{3},1:{3},2:{3},3:{0,1,2}}, dict(enumerate(taxa)))


def enumerate_trees(taxa):
    taxa = sorted(taxa)
    if not 3 <= len(taxa) <= 8: raise ValueError('exhaustive enumeration limited to 3..8 taxa')
    def grow(tree, k):
        if k == len(taxa): yield tree
        else:
            for edge in edges(tree): yield from grow(insert_leaf(tree, edge, taxa[k]), k+1)
    yield from grow(star3(taxa[:3]), 3)


def prune(tree, keep):
    t = tree.copy()
    if not set(keep) <= set(t.labels.values()) or len(keep) < 3: raise ValueError('invalid pruning taxa')
    for v in list(t.labels):
        if t.labels[v] not in keep:
            p = next(iter(t.adj[v])); t.adj[p].remove(v); del t.adj[v]; del t.labels[v]
            u, w = sorted(t.adj.pop(p))
            t.adj[u].remove(p); t.adj[w].remove(p); t.adj[u].add(w); t.adj[w].add(u)
    return validate(t, keep)
