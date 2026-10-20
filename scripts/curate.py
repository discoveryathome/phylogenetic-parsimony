"""Offline deterministic curation from pinned source bytes; no network or tools."""
from pathlib import Path
import json
import re
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from phylo.alignment import PROFILE, sha256
from phylo.tree import parse, prune, newick
ROOT = Path(__file__).resolve().parents[1]

def build():
    output, rows = {}, []
    for name, alphabet, expected in [('dnapars','RNA',19),('dnapenny','DNA',8)]:
        source = ROOT/'sources'/f'{name}.html'
        text = source.read_text().split('TEST DATA SET')[1].split('</PRE>')[0]
        pairs = re.findall(r'^([A-Za-z0-9]+)\s+([ACGTU]+)\s*$',text,re.M)
        ident = 'phylip-'+name
        if len(pairs) != (5 if name == 'dnapars' else 8): raise ValueError('source example parse failed')
        path = f'data/{ident}.fasta'; output[path] = ''.join(f'>{n}\n{s}\n' for n,s in pairs)
        tree = '(Alpha,Beta,(Gamma,(Delta,Epsilon)));' if name == 'dnapars' else '(Alpha1,((Alpha2,((Epsilon,Delta),(Gamma2,Gamma1))),(Beta2,Beta1)));'
        baseline = f'candidates/{ident}-baseline.nwk'; output[baseline] = tree+'\n'
        rows.append(dict(id=ident,path=path,alphabet=alphabet,profile=PROFILE,ntax=len(pairs),nchar=len(pairs[0][1]),source=f'sources/{name}.html',source_sha256=sha256(source),source_url=f'https://phylipweb.github.io/phylip/doc/{name}.html',license='PHYLIP-document-permission + BSD-2-Clause; see THIRD_PARTY.md',baseline_tree=baseline,published_score=expected,published_scope='Exact unchanged tutorial alignment; documented tree transcribed from first figure',transformation='FASTA transcription only; RNA U to T only inside scorer',kind='published-synthetic'))
    raw, current = {}, None
    for line in (ROOT/'sources/pythonidae.fasta').read_text().splitlines():
        if line.startswith('>'):
            current = line[1:].strip(); raw[current] = ''
        elif line.strip(): raw[current] += line.strip().upper()
    if len(raw)!=33 or {len(s) for s in raw.values()} != {2716}: raise ValueError('source dimensions changed')
    mapping = {n:n.replace(' ','_') for n in raw}
    if len(set(mapping.values())) != len(raw): raise ValueError('taxon mapping collision')
    seqs = {mapping[n]:s for n,s in raw.items()}; names = sorted(seqs)
    source_tree = parse((ROOT/'sources/pythonidae-mle.nwk').read_text(),seqs)
    revision = (ROOT/'sources/dendropy-revision.txt').read_text().strip()
    for size in (6,12,24):
        keep = [names[i*len(names)//size] for i in range(size)]
        # Source annotation: CYTB = sites 733..1846 inclusive (1-based).
        sites = [i for i in range(732,1846) if all(seqs[n][i] in 'ACGT' for n in keep)]
        ident = f'pythonidae-cytb-{size}'; path = f'data/{ident}.fasta'
        output[path] = ''.join('>'+n+'\n'+''.join(seqs[n][i] for i in sites)+'\n' for n in keep)
        baseline = f'candidates/{ident}-baseline.nwk'
        output[baseline] = newick(prune(source_tree,set(keep)))+'\n'
        provenance = f'data/{ident}-selection.json'
        output[provenance] = json.dumps(dict(taxa=keep,source_labels={n:mapping[n] for n in raw if mapping[n] in keep},source_columns_1based=[i+1 for i in sites],source_interval_1based=[733,1846],removed_columns=1114-len(sites)),indent=2)+'\n'
        rows.append(dict(id=ident,path=path,alphabet='DNA',profile=PROFILE,ntax=size,nchar=len(sites),source='sources/pythonidae.fasta',source_sha256=sha256(ROOT/'sources/pythonidae.fasta'),source_url=f'https://github.com/jeetsukumaran/DendroPy/blob/{revision}/tests/unittests/data/chars/pythonidae.chars.fasta',license='BSD-3-Clause',study_doi='10.1111/j.1095-8312.2007.00904.x',baseline_tree=baseline,published_score=None,published_scope='No published MP score for this derived alignment; source MLE topology is only a documented comparator',transformation='Sorted taxa at floor(i*33/n); CYTB 733..1846; complete-case column filtering',selection=provenance,kind='empirical-derived'))
    from curate_expansion import expand
    expand(ROOT,output,rows,seqs,source_tree)
    for row in rows:
        if 'source_group' not in row:
            row['source_group']='phylip-tutorials' if row['kind']=='published-synthetic' else 'pythonidae-2008'
            row['marker']='synthetic' if row['kind']=='published-synthetic' else 'mitochondrial-CYTB'
            row['baseline_method']='published-tutorial' if row['kind']=='published-synthetic' else 'pruned-source-ML'
    import hashlib
    for row in rows: row['sha256'] = hashlib.sha256(output[row['path']].encode()).hexdigest()
    output['data/manifest.json'] = json.dumps(dict(schema='phylo-data/v1',datasets=rows),indent=2)+'\n'
    return output

if __name__ == '__main__':
    output = build()
    if '--check' in sys.argv:
        for path,text in output.items():
            if (ROOT/path).read_text()!=text: raise SystemExit('Curation mismatch: '+path)
        print('Curation replay: all derived bytes match')
    else:
        for path,text in output.items(): (ROOT/path).write_text(text)
        print('Curated',len(output),'files')
