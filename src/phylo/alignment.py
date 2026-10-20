"""Fixed profile: strict four-state FASTA, explicit DNA/RNA alphabets."""
from pathlib import Path
import hashlib
import re
import json

PROFILE = 'unordered-unit-strict-v1'

def read_fasta(path, alphabet='DNA'):
    if alphabet not in ('DNA', 'RNA'): raise ValueError('alphabet must be DNA or RNA')
    seqs, current = {}, None
    for line in Path(path).read_text(encoding='utf8').splitlines():
        line = line.strip()
        if not line: continue
        if line.startswith('>'):
            current = line[1:]
            if not re.fullmatch(r'[A-Za-z0-9_.-]+', current) or current in seqs:
                raise ValueError('duplicate/unsupported FASTA ID; no descriptions or spaces')
            seqs[current] = ''
        else:
            if current is None: raise ValueError('sequence before FASTA header')
            if any(c not in ('ACGT' if alphabet == 'DNA' else 'ACGU') for c in line):
                raise ValueError('strict profile rejects gaps, missing, ambiguous, lowercase or mixed alphabet')
            seqs[current] += line.replace('U', 'T')
    if len(seqs) < 3 or len({len(s) for s in seqs.values()}) != 1 or not all(seqs.values()):
        raise ValueError('need >=3 taxa and equal, nonzero sequence lengths')
    return seqs


def sha256(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_dataset(root, dataset):
    rows = json.loads((root/'data/manifest.json').read_text())['datasets']
    matches = [r for r in rows if r['id'] == dataset]
    if len(matches) != 1: raise ValueError('unknown/nonunique dataset')
    row = matches[0]
    if row['profile'] != PROFILE: raise ValueError('unsupported scoring profile')
    if sha256(root/row['path']) != row['sha256']: raise ValueError('alignment hash mismatch')
    a = read_fasta(root/row['path'], row['alphabet'])
    if len(a) != row['ntax'] or len(next(iter(a.values()))) != row['nchar']:
        raise ValueError('alignment dimensions disagree with manifest')
    return row, a
