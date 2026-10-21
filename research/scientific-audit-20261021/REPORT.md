# Established-software baseline — 21 October 2026

PHYLIP improved **four of the nine open rows**. All eight settled controls matched
their known optima. None of the nine open rows has become globally solved.
The working table and contributor cards inherit these four stronger targets;
historical accepted results remain unchanged, and scientific acceptance is pending.

| Fixed alignment | Previous working score | PHYLIP best, independently rescored | Bound |
|---|---:|---:|---:|
| phylip-dnapars | 19 | 19 | 19 |
| phylip-dnapenny | 8 | 8 | 8 |
| pythonidae-cytb-6 | 343 | 343 | 343 |
| pythonidae-cytb-12 | 575 | 575 | 392 |
| pythonidae-cytb-24 | 982 | 980 | 466 |
| cetaceans-mt-6 | 291 | 291 | 291 |
| cetaceans-mt-12 | 493 | 493 | 398 |
| cetaceans-mt-22 | 1046 | 1045 | 595 |
| ferula-nrdna-6 | 61 | 61 | 61 |
| ferula-nrdna-12 | 82 | 82 | 82 |
| ferula-nrdna-24 | 141 | 141 | 138 |
| ferula-plastid-6 | 27 | 27 | 27 |
| ferula-plastid-12 | 39 | 39 | 39 |
| ferula-plastid-24 | 104 | 104 | 102 |
| pythonidae-12s-12 | 112 | 105 | 82 |
| pythonidae-16s-12 | 93 | 93 | 70 |
| pythonidae-cytb-29 | 2005 | 1993 | 799 |

## Method and evidence

We built the unmodified official [PHYLIP source archive](https://phylipweb.github.io/phylip/download/phylip-3.697.tar.gz)
with clang on macOS arm64. The downloaded archive and executable identify version
**3.697**, despite the download landing page advertising 3.698. `software.json`
records the exact archive hash, binary hash and build flags; `build.log` records
compilation. Do not substitute a different build without recording it.

All 17 immutable alignments were run with seeds 13, 37 and 101, ten randomized
addition-order jumbles per seed, default “More thorough search”, at most 100 saved
tied trees, and a 60-second process timeout. All 51 runs completed. Each run retains
the PHYLIP input, reversible label map, menu transcript, console output, report,
raw tree file and every converted witness. These were quality-baseline runs, not
a paired speed experiment against the Python optimizer. Logged wall times include
conversion/reference rescoring and shared-machine load.

The [Dnapars contract](https://phylipweb.github.io/phylip/doc/dnapars.html) requires
attention to character states and multifurcations. Here all input characters are
fully specified A/C/G/T (the RNA tutorial's U→T mapping is bijective). Every taxon
and every frozen column is retained, including constant/uninformative sites;
weights are one, with neither threshold nor transversion-only scoring. Short
synthetic taxon IDs are mapped back exactly. These inputs avoid PHYLIP's different
deletion/ambiguity conventions.

The raw output contained 251 trees. We removed only numeric tree-weight comments
and branch lengths, restored labels, and deterministically resolved multifurcations
in 88 witnesses. `verify_results.py` independently scores the original potentially
multifurcating trees with direct four-state dynamic programming and the resolved
binary trees with the repository's Sankoff checker. **All 251 raw scores agree with
PHYLIP, all converted scores agree with the raw scores, and no resolution improved
a score.** Resolution remains an explicit transformation, not an invisible parser
exception. The verifier checks original input bytes, alignment identities and best
witness hashes. Four adapter regressions cover binary/rooted/multifurcating and
unsupported output syntax.

## Reproduction

Read `software.json`; download its URL and verify the recorded SHA-256. Unpack into
an ignored directory, then run the recorded build command inside `src/`. The
source/binary are not vendored into this project. PHYLIP's source license remains
with its original distribution. This project retains only its own inputs and
research outputs.

```sh
# Standalone evidence replay: no PHYLIP install required
python3 research/scientific-audit-20261021/verify_results.py
python3 -m unittest discover -s research/scientific-audit-20261021 -p 'test_*.py' -v
python3 scripts/check_cards.py
python3 scripts/check.py
```

`phylip_baseline.py --binary /path/to/dnapars` documents the executable experiment.
It refuses existing run directories to protect receipts. For a fresh rerun, copy
the script into a fresh sibling directory under `research/`; it derives the repo
root from that location and writes evidence beside itself. Preserve the original
run package for comparison. Results include every declared seed and every tree;
only selecting the best tree for the working target is an explicit selection.

## Portfolio decision

The package now has a credible established-software floor. Four easy-to-obtain
improvements show why donated search must start from stronger targets. Matching
PHYLIP on the other rows does not prove exhaustion or biological validity.
Keep the current alignments for a controlled trial, prioritize a second mature
implementation (for example MPBoot, TNT or PAUP* with compatible settings), and
measure useful outcomes against these targets before expanding the collection.
Stronger lower bounds and careful tied-tree analysis remain useful even without
a lower tree score. No novelty claim relative to literature is made.

This is author/coordinator-run evidence using independent algorithms, not an
independent human scientific review. No remote publication, accepted-frontier
change, new alignment, or biological-history claim was made.
