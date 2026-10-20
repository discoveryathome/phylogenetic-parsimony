# Local verification record

Expanded 2026-10-20, Python 3.14.6, macOS arm64. Runtime dependencies remain Python
standard library only. Imported alignments, trees and metadata were parsed as data;
no external scoring package or global installation was used.

The exact reference remains four-state Sankoff DP, independent of search's
compressed Fitch recurrence. Both share the structural parser. Pair-certificate
checking uses direct state sets, independently of the generator's bit masks.
This is algorithmic independence, not independent human review.

The offline `scripts/check.py` reconstructs all 17 curated inputs and source
comparators, checks source/data/tree hashes, scores all 250 recorded search outputs
and incumbents, and verifies every bound certificate. For empirical six-taxon
controls it independently enumerates all 105 trees using the reference DP.
Tutorial exhaustive controls cover 15 and 10,395 trees, with published scores
19 and 8 and nine optima for the latter.

The 16 test methods include all quartet site patterns against brute ancestral-state
assignment, full small-tree differential checks, enumeration counts, graph/Newick
rejection, root invariance, strict nucleotide policy, seed reproducibility and
negative CLI controls. Expansion tests check pair bounds against every pair of
binary quartet columns and all three trees, reject malformed certificates, check
two-move budget/local-radius claims, and verify a known NJ quartet and taxon-order
invariance. The original five alignment hashes are unchanged.

`scripts/replay_search.py` replays all 20 original plus 230 expansion records,
checking trees, scores, traces and evaluation counts. Elapsed times are excluded.
Python version is recorded; other interpreter versions require testing rather than
assuming identical pseudo-random behavior. Evaluation caps are not equal wall time
or actual work: strict NNI can stop early.

`scripts/check_cards.py` runs all 13 catalog controls, including nine open-tree
checks and heuristic, bound, audit and biological controls. A fresh local clone
runs the complete offline check without any external dataset path or network.
Expansion receipts are in `results/validation-expansion.txt`; original initialization
receipts remain in `results/validation.txt` as historical evidence.

The Discovery@Home helper outside this repository matches the playbook SHA-256
`d0e9ce87016c42aea0082fa171e29992d9c84a70ca1de0f0713e660fd57e1ea4`.
Its format validation reports 17 cases, nine open; its screen reports no findings.
Missing public coordination/ledger/package locations are optional conventions.
Helper and reproduction commands run under a local sandbox blocking network and
other user folders, with writes restricted to the task workspace. No global
settings were changed. Protocol conformance does not establish scientific quality,
independent review, biological truth, or readiness to admit donors.

Review remains paused with an explicitly unassigned maintainer role. Eight rows
have proven optima; nine retain certified lower and witnessed upper bounds. No
published MP record is claimed for the derived empirical matrices.
