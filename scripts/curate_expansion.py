"""Explicit source-specific curation. This is not a general NEXUS/PHYLIP importer."""
import re,json
from phylo.alignment import PROFILE,sha256
from phylo.tree import parse,prune,newick
from phylo.initial import neighbor_joining


def nexus_dna(path):
    text=path.read_text(encoding='cp1252')
    text=re.sub(r'\[[^\]]*\]','',text,flags=re.S)
    if not re.search(r'datatype\s*=\s*dna\b',text,re.I):raise ValueError('source must declare DNA')
    ntax=int(re.search(r'ntax\s*=\s*(\d+)',text,re.I)[1]);nchar=int(re.search(r'nchar\s*=\s*(\d+)',text,re.I)[1])
    matrix=re.search(r'\bmatrix\b(.*?);',text,re.I|re.S)[1];seqs={}
    for line in matrix.strip().splitlines():
        bits=line.split()
        if len(bits)!=2 or bits[0] in seqs:raise ValueError('unsupported source NEXUS row')
        seqs[bits[0]]=bits[1].upper()
    first=next(iter(seqs.values()))
    seqs={n:''.join(first[i] if c=='.' else c for i,c in enumerate(s)) for n,s in seqs.items()}
    if len(seqs)!=ntax or {len(s) for s in seqs.values()}!={nchar}:raise ValueError('source dimensions mismatch')
    return seqs


def phylip_dna(path):
    lines=path.read_text().splitlines();ntax,nchar=map(int,lines[0].split());seqs={}
    for line in lines[1:]:
        if not line.strip():continue
        bits=line.split()
        if len(bits)!=2 or bits[0] in seqs:raise ValueError('unsupported source PHYLIP row')
        seqs[bits[0]]=bits[1].upper()
    if len(seqs)!=ntax or {len(s) for s in seqs.values()}!={nchar}:raise ValueError('source dimensions mismatch')
    return seqs


def expand(root, output, rows, python_raw, python_tree):
    rev=(root/'sources/dendropy-revision.txt').read_text().strip()
    dendro='https://github.com/jeetsukumaran/DendroPy/blob/'+rev+'/tests/unittests/data/chars/'
    cet=nexus_dna(root/'sources/cetaceans.nex')
    ets=phylip_dna(root/'sources/ferula-ETS_ITS.phy');plastid=phylip_dna(root/'sources/ferula-plastid.phy')
    if set(ets)!=set(plastid):raise ValueError('paired Ferula source taxa differ')
    paired_eligible={n for n in ets if all(sum(c in 'ACGT' for c in seqs[n])/len(seqs[n])>=0.8 for seqs in (ets,plastid))}
    for seqs in [cet,ets,plastid]:
        if any(not re.fullmatch(r'[A-Za-z0-9_.-]+',n) for n in seqs):raise ValueError('source ID needs explicit mapping')
        if any(not set(s)<=set('ACGTRYSWKMBDHVN?-') for s in seqs.values()):raise ValueError('unexpected source symbol')
    def source_tree(file,seqs):
        # Source-only removal of numeric support labels. Candidate parser remains strict.
        s=(root/file).read_text().strip()
        s=re.sub(r'\)(?:\d+(?:\.\d+)?)(?=[:),;])',')',s)
        return parse(s,seqs)
    ets_tree=source_tree('sources/ferula-ETS_ITS-ML.nwk',ets)
    plastid_tree=source_tree('sources/ferula-plastid-ML.nwk',plastid)
    specs=[
      ('cetaceans-mt',cet,None,(6,12,22),1,1365,'sources/cetaceans.nex','BSD-3-Clause','10.1093/oxfordjournals.molbev.a040164','cetaceans-1994','mitochondrial-three-gene',dendro+'cetaceans.nex'),
      ('ferula-nrdna',ets,ets_tree,(6,12,24),1,1090,'sources/ferula-ETS_ITS.phy','CC0-1.0','10.1093/botlinnean/boaf050','ferula-2025','nuclear-ETS-ITS','https://doi.org/10.18150/UZC2YR'),
      ('ferula-plastid',plastid,plastid_tree,(6,12,24),1,3258,'sources/ferula-plastid.phy','CC0-1.0','10.1093/botlinnean/boaf050','ferula-2025','plastid-rpoC1-rpoB_trnC-rps16','https://doi.org/10.18150/UZC2YR'),
      ('pythonidae-12s',python_raw,python_tree,(12,),1847,2218,'sources/pythonidae.fasta','BSD-3-Clause','10.1111/j.1095-8312.2007.00904.x','pythonidae-2008','mitochondrial-12S',dendro+'pythonidae.chars.fasta'),
      ('pythonidae-16s',python_raw,python_tree,(12,),2219,2716,'sources/pythonidae.fasta','BSD-3-Clause','10.1111/j.1095-8312.2007.00904.x','pythonidae-2008','mitochondrial-16S',dendro+'pythonidae.chars.fasta'),
      ('pythonidae-cytb',python_raw,python_tree,(33,),733,1846,'sources/pythonidae.fasta','BSD-3-Clause','10.1111/j.1095-8312.2007.00904.x','pythonidae-2008','mitochondrial-CYTB',dendro+'pythonidae.chars.fasta')]
    for prefix,seqs,tree,sizes,lo,hi,source,license,doi,group,marker,url in specs:
        names=sorted(n for n,s in seqs.items() if sum(c in 'ACGT' for c in s[lo-1:hi])/(hi-lo+1)>=0.8)
        if group=='ferula-2025':names=sorted(set(names)&paired_eligible)
        excluded=sorted(set(seqs)-set(names))
        for requested_size in sizes:
            size=min(requested_size,len(names))
            if size<3:raise ValueError('too few eligible taxa: '+prefix)
            keep=[names[i*len(names)//size] for i in range(size)]
            sites=[i for i in range(lo-1,hi) if all(seqs[n][i] in 'ACGT' for n in keep)]
            if not sites:raise ValueError('empty curated alignment: '+prefix)
            selected={n:''.join(seqs[n][i] for i in sites) for n in keep}
            ident=f'{prefix}-{size}';path=f'data/{ident}.fasta';baseline=f'candidates/{ident}-baseline.nwk';selection=f'data/{ident}-selection.json'
            output[path]=''.join(f'>{n}\n{s}\n' for n,s in selected.items())
            output[baseline]=newick(prune(tree,set(keep)) if tree else neighbor_joining(selected))+'\n'
            output[selection]=json.dumps(dict(taxa=keep,source_labels={n:n for n in keep},source_columns_1based=[i+1 for i in sites],source_interval_1based=[lo,hi],minimum_taxon_complete_fraction=0.8,eligibility_scope='both Ferula source matrices' if group=='ferula-2025' else 'this source window',excluded_taxa=excluded,removed_columns=hi-lo+1-len(sites)),indent=2)+'\n'
            rows.append(dict(id=ident,path=path,alphabet='DNA',profile=PROFILE,ntax=size,nchar=len(sites),source=source,source_sha256=sha256(root/source),source_url=url,license=license,study_doi=doi,source_group=group,marker=marker,baseline_tree=baseline,baseline_method='pruned-source-ML' if tree else 'local-neighbor-joining-Hamming-v1',published_score=None,published_scope='No published MP score for this derived fixed alignment; comparator is locally rescored',transformation=f'Uppercase; exclude taxa <80% ACGT within window'+(' in either Ferula source matrix' if group=='ferula-2025' else '')+f'; sorted eligible taxa floor(i*{len(names)}/n); source sites {lo}..{hi}; complete-case columns only; numeric ML support labels removed before pruning',selection=selection,kind='empirical-derived'))
