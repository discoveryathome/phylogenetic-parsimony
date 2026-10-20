# Maximum-parsimony phylogenetic trees — local pilot

Given a fixed nucleotide alignment, find a binary unrooted Newick tree minimizing
character-state changes. **Lower parsimony score does not prove that the tree
reflects true evolutionary history.** Each fixed alignment has its own frontier.

LOCAL mode: nothing published, pushed or posted. Review remains paused pending
an accepting maintainer. The manifest's UNASSIGNED ROLE is a placeholder.

## Coverage

Expanded from five to **17 fixed alignments**, with **nine open rows and eight
proven optima**. There are **three empirical studies**, not 17 independent studies:

| Source | Rows | What is covered | Redistribution |
|---|---:|---|---|
| PHYLIP tutorials | 2 | Fully specified RNA/DNA; published scores 19 and 8 | Retained documentation permission/BSD notices |
| Pythonidae / Rawlings et al. | 6 | CYTB at 6/12/24/29 taxa; 12S and 16S at 12 taxa | DendroPy BSD-3-Clause |
| Cetaceans / Milinkovitch et al. | 3 | Adapted mitochondrial fixture at 6/12/22 taxa | DendroPy BSD-3-Clause |
| Ferula / Piwczyński et al. | 6 | Matched nuclear ETS/ITS and plastid subsets at 6/12/24 taxa | RePoD CC0-1.0 |

All inputs are public non-human animal or plant data, or tutorials. Source hashes,
license evidence, excluded taxa and original-column maps are retained. New rows
require ≥80% taxon coverage, then complete-case filtering; paired Ferula subsets
use a shared eligible taxon set. Old alignment bytes remain unchanged. These
choices can alter biological signal. See [MODEL.md](MODEL.md),
[LITERATURE.md](LITERATURE.md) and [THIRD_PARTY.md](THIRD_PARTY.md).

## Run it

Python 3.10+ standard library; no installation or network needed:

```sh
python3 scripts/check.py
python3 scripts/progress.py
python3 phylo.py search pythonidae-cytb-12 --method two-nni --seed 1729 --restarts 1 --budget 5000 --start candidates/pythonidae-cytb-12-best.nwk --out .scratch/search.nwk
python3 phylo.py verify-bound ferula-nrdna-12 results/ferula-nrdna-12-bound.json
python3 scripts/interpret.py ferula-nrdna-12
python3 scripts/replay_search.py
```

The offline check reconstructs all curated data, checks source identities,
independently scores every recorded tree, checks pair certificates, exhaustively
rescores six-taxon controls, and runs 16 regression tests. Full seed replay checks
saved trees, scores, traces and evaluation counts for all 250 historical/expanded
runs. Replay is longer than verification; allow several minutes on a laptop.
Wall times are not reproducibility targets or controlled speed measurements.

## Current local frontier

| Alignment | Taxa × sites | Comparator | Best | Lower bound | Status |
|---|---:|---:|---:|---:|---|
| phylip-dnapars | 5 × 13 | 19 | 19 | 19 | settled |
| phylip-dnapenny | 8 × 6 | 8 | 8 | 8 | settled |
| pythonidae-cytb-6 | 6 × 1039 | 343 | 343 | 343 | settled |
| pythonidae-cytb-12 | 12 × 647 | 591 | 575 | 392 | open |
| pythonidae-cytb-24 | 24 × 631 | 1013 | 982 | 466 | open |
| cetaceans-mt-6 | 6 × 1324 | 291 | 291 | 291 | settled |
| cetaceans-mt-12 | 12 × 1299 | 493 | 493 | 398 | open |
| cetaceans-mt-22 | 22 × 1277 | 1050 | 1046 | 595 | open |
| ferula-nrdna-6 | 6 × 1056 | 61 | 61 | 61 | settled |
| ferula-nrdna-12 | 12 × 1050 | 82 | 82 | 82 | settled |
| ferula-nrdna-24 | 24 × 1045 | 141 | 141 | 138 | open |
| ferula-plastid-6 | 6 × 3092 | 27 | 27 | 27 | settled |
| ferula-plastid-12 | 12 × 3045 | 39 | 39 | 39 | settled |
| ferula-plastid-24 | 24 × 3028 | 105 | 104 | 102 | open |
| pythonidae-12s-12 | 12 × 318 | 116 | 112 | 82 | open |
| pythonidae-16s-12 | 12 × 433 | 97 | 95 | 70 | open |
| pythonidae-cytb-29 | 29 × 994 | 2048 | 2005 | 799 | open |

The [PHYLIP Dnapars](https://phylipweb.github.io/phylip/doc/dnapars.html) and
[Dnapenny](https://phylipweb.github.io/phylip/doc/dnapenny.html) scores are published
optima. Six rows are settled exhaustively; two additional 12-taxon Ferula rows
have pair-bound certificates meeting their witnessed scores. All other bounds
are conservative. Their gaps are neither biological uncertainty nor a promise
that better trees exist.

Empirical matrices are newly derived instances with no claimed published MP
record. Pythonidae/Ferula comparators are pruned source ML trees; cetacean
comparators are local deterministic Hamming neighbor joining. Beating these does
not establish superiority over a mature parsimony program.

## Recommended starting challenges

1. **Improve search reliability:** at a 600-evaluation cap, two-move NNI reaches
   the known eight-taxon optimum on 11/20 seeds and the known Ferula nuclear
   12-taxon optimum on 7/20. Try plateau traversal, SPR or better budget allocation;
   retain every run and evaluate held-out seeds before generalizing.
2. **Close a small certified gap:** Ferula nuclear 24 has bounds 138–141; plastid
   24 has 102–104. Improve a tree, a bound, or both. Neither gap guarantees a win.
3. **Improve open trees:** Pythonidae CYTB 12 is now 575 (previously 579), CYTB 24
   is 982 (previously 990). The new 29-taxon row scores 2005 versus comparator 2048.
4. **Audit exact evidence:** test parser and bound certificates, or independently
   implement scoring and minimize disagreements.
5. **Investigate marker conflict:** matched Ferula nuclear/plastid solutions
   disagree even where both scores are globally optimal. Examine tied alternatives,
   source-coordinate site changes, partitions and filtering sensitivity.

All known improvements have been adopted. Controls at a proven optimum are not
advertised as beatable tree targets. These automated probes show tangible early
progress, not a measured donor-session success rate. Before public launch, run
supervised 30–60 minute contributor trials from a frozen commit and measure useful
verified outcomes, time to first result and review burden.

The five weighted tracks are trees (30%), heuristics (25%), bounds (20%), audits
(15%) and interpretation (10%). The picker balances source studies within tree
search. Each card has a runnable control and acceptance gate:

```sh
python3 scripts/pick.py --seed 0123456789abcdef0123456789abcdef
python3 scripts/check_cards.py
```

[RESULTS.md](RESULTS.md) explains the full paired experiment and biological
contrasts. [DISCOVERY.md](DISCOVERY.md) is the contributor entry and
[VERIFICATION.md](VERIFICATION.md) records the validation scope.

`python3 scripts/benchmark.py` regenerates expansion evidence while preserving
verified incumbents and the original benchmark. `scripts/refresh_catalog.py`
updates cards after authorized frontier changes. These are maintainer operations;
contributor experiments should write under `.scratch/` and verify their witnesses.
After changing evidence, regenerate `results/progress.json` with `scripts/progress.py`.

Original code/prose: MIT. Imported materials retain their own licenses. An accepting
maintainer and independent review remain necessary before donor admission.
