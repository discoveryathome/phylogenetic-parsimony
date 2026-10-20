# Baseline experiments

All inputs use unordered-unit-strict-v1. For each alignment, seeds 17, 1729 and
20261020 use three random-addition starts and at most 1,800 full Fitch evaluations
per seed (600 per start). Seed 0 denotes a separate source-tree-start run, one start
and the same 1,800-evaluation cap; its trajectory is deterministic and has no random
initialization. This deliberately tests initialization as well as search. It is not
a claim that the source tree was free to produce or that NNI beats its original
inference method. Site-pattern compression preserves unit weights exactly.

| Dataset | Source comparator | Random 17 | Random 1729 | Random 20261020 | Source-start NNI | Proven optimum |
|---|---:|---:|---:|---:|---:|---:|
| phylip-dnapars | 19 | 19 | 19 | 19 | 19 | 19 |
| phylip-dnapenny | 8 | 9 | 10 | 11 | 8 | 8 |
| pythonidae-cytb-6 | 343 | 343 | 343 | 343 | 343 | 343 |
| pythonidae-cytb-12 | 591 | 585 | 581 | 592 | 579 | unknown |
| pythonidae-cytb-24 | 1013 | 1093 | 1085 | 1071 | 990 | unknown |

Strict descent cannot traverse neutral plateaus. On the eight-taxon control the
random starts miss the published optimum despite converging locally. On 24 taxa
the random starts use their entire budget and are worse than the source tree;
source-start NNI improves its score. All results, including these failures, are
retained. Use completed local-optimum flags and per-run evaluation counts rather
than assuming every budget-limited run converged.

The checker recomputes every stored score independently. Three small fixed
instances are exhaustively settled; the two larger instances remain open. The
12-taxon and 24-taxon source comparators improve by 12 and 23 changes respectively.
These are local computational results on new subsets, not published records.

Reproduce deterministic trajectories with `python3 scripts/replay_search.py`.
The benchmark JSON records Python/platform and wall time, but no speed superiority
is claimed. Setup ran other checks as well, and machine load was not controlled.
A speed study would need interleaved runs, A/A controls, a fixed environment and
repeat measurements. Evaluation counts are useful but do not make differing
neighborhood implementations equal in wall-clock cost.

For topology/site contrasts: `python3 scripts/interpret.py pythonidae-cytb-12`.
The RF distance is the unnormalized number of differing nontrivial splits on the
same taxa. It is not statistical support. Complete-case filtering can change
signal; a mitochondrial gene tree need not represent the species history.
