# Maximum-parsimony phylogenetic trees — local pilot

Given a fixed nucleotide alignment, find a binary unrooted Newick tree minimizing
the total number of character-state changes. Each fixed alignment has its own
frontier. **A lower parsimony score does not prove that the tree reflects the true
evolutionary history.**

LOCAL mode: nothing has been published, pushed or posted. This is a complete local
pilot, with review paused until a maintainer agrees to take responsibility. The
UNASSIGNED ROLE manifest entry is a placeholder, not a consenting maintainer.

## Run it

Python 3.10+; standard library only. No install or network needed. From this folder:

```sh
python3 scripts/check.py
python3 phylo.py verify phylip-dnapars candidates/phylip-dnapars-baseline.nwk --claim 19
python3 phylo.py search pythonidae-cytb-12 --seed 1729 --restarts 4 --budget 10000 --start candidates/pythonidae-cytb-12-best.nwk --out .scratch/search.nwk
python3 phylo.py exhaustive pythonidae-cytb-6 --out .scratch/exact.nwk
python3 scripts/replay_search.py
```

The check prints five row verdicts and `PASS`, after data hashes, offline curation
replay, exact candidate/baseline scores, exhaustive bounds and the regression suite.
The full seed replay additionally reproduces saved trees, scores, traces and
operation counts; elapsed times are deliberately excluded. Expect about a minute
for both checks on an ordinary laptop; measurements depend on the machine.

## Current local frontier

| Alignment | Taxa × sites | Baseline | Best | Lower bound | Status |
|---|---:|---:|---:|---:|---|
| phylip-dnapars | 5 × 13 | 19 | 19 | 19 | settled |
| phylip-dnapenny | 8 × 6 | 8 | 8 | 8 | settled |
| pythonidae-cytb-6 | 6 × 1039 | 343 | 343 | 343 | settled |
| pythonidae-cytb-12 | 12 × 647 | 591 | 579 | 343 | open |
| pythonidae-cytb-24 | 24 × 631 | 1013 | 990 | 412 | open |

The tutorial baseline scores **19** and **8** are published in the
[PHYLIP Dnapars](https://phylipweb.github.io/phylip/doc/dnapars.html) and
[Dnapenny](https://phylipweb.github.io/phylip/doc/dnapenny.html) manuals. Enumeration
checks all 15 and 10,395 trees, respectively, and recovers Dnapenny's nine optimal
trees. The six-taxon empirical optimum comes from enumeration of 105 topologies.
For the larger rows, the lower bound is the sum of distinct observed states minus
one per site; the remaining gap is not a biological uncertainty measure.

Pythonidae rows are newly curated subsets of the BSD-licensed DendroPy fixture
attributed to [Rawlings et al. (2008)](https://doi.org/10.1111/j.1095-8312.2007.00904.x).
Their comparator is a pruned source maximum-likelihood tree, rescored locally.
No published parsimony score is claimed for these derived alignments. The complete
source, license, hashes, selection recipe and original site coordinates are included.

## Recommended starting challenges

1. **Beat 579** on `pythonidae-cytb-12`; use the incumbent as a starting tree.
2. **Beat 990** on `pythonidae-cytb-24`; test a broader neighborhood or plateau moves.
3. **Escape a known local minimum:** the seed-17 random NNI control scores 9 on
   `phylip-dnapenny`, whose proven optimum is 8. Compare 20 predeclared paired seeds.
4. **Audit acceptance:** find a parser/scorer counterexample or add an independent
   implementation check with minimized regression inputs.
5. **Interpret the changes:** map topology and site-score differences to the
   original CYTB columns without equating lower score with biological truth.

The weighted catalog has tracks for improved trees, heuristics, verifier audits and
biological interpretation. Every card has a runnable positive control and an
acceptance gate. Agent entry: [AGENTS.md](AGENTS.md) → [DISCOVERY.md](DISCOVERY.md).

## What is included

- [MODEL.md](MODEL.md): exact objective, RNA mapping, root invariance, strict gap,
  missing and ambiguity rejection, and accepted Newick syntax.
- [src/phylo/scoring.py](src/phylo/scoring.py): independent integer Sankoff checker;
  [search.py](src/phylo/search.py): Fitch scoring, seeded NNI and exact enumeration.
- [data/manifest.json](data/manifest.json): five fixed alignments and provenance;
  [THIRD_PARTY.md](THIRD_PARTY.md): redistribution terms and required attribution.
- [LITERATURE.md](LITERATURE.md): source-backed claims, benchmark research, known
  limitations and admission decisions.
- [results/benchmark.json](results/benchmark.json): all seed runs, including failures;
  [RESULTS.md](RESULTS.md): comparison and interpretation of those results.
- [discover/frontier.json](discover/frontier.json) and its per-alignment table;
  [catalog.json](discover/catalog.json): concrete starting challenges.

`python3 scripts/benchmark.py` regenerates the initialization benchmark and local
frontier files. It is a maintainer/init operation, not a verifier. Donor experiments
should write candidate files under `.scratch/` and use the verify command.

Original code/prose: MIT. Third-party data/documents retain their licenses.
No sensitive human genomic data is included. The verifier and frontier deserve
careful review; maintainer review capacity will determine any future donor pace.
