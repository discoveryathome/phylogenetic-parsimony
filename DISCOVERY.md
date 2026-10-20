# Fixed-alignment parsimony pilot

Find binary unrooted trees minimizing total unordered unit-cost nucleotide changes
for each fixed alignment. A contribution is a Newick witness with an exactly
recomputed integer score. The primary measure is a smaller score on the identical
alignment hash and scoring profile; each alignment is a separate frontier row.
The objective, evidence profile and local build are authorized by the task request.
The public repository and hub registry PR were authorized by the project owner.
Donor admission remains paused; donated-session permissions remain explicit.

Read MODEL.md for all character and tree semantics, LITERATURE.md for the evidence
brief, and data/manifest.json plus THIRD_PARTY.md for provenance and redistribution.
The literature audit verifies the tutorial scores 19 and 8. Our exhaustive controls
also settle the six-taxon empirical subsets. Larger incumbents are local upper
bounds, not literature records. `discover/frontier-rows.json` is authoritative.

## Bottleneck and research tracks

The verifier is cheap; escaping local topology minima without losing reproducibility
is the research bottleneck. Score ties can conceal very different trees. NNI misses
the published eight-taxon optimum from the shipped random starts; more compute on
the same strict-descent path is not a guarantee of improvement.

- Improved trees (30%): search open rows across three empirical studies; keep exact witnesses.
- Better heuristics (25%): compare plateau handling, SPR or a ratchet with both NNI
  baselines using paired seeds and equal caps; report failures as well as wins.
- Stronger bounds (20%): improve disjoint incompatible-column pair certificates,
  or propose stronger bounds with a proof and independently tested checker.
- Verifier audits (15%): attack parser, graph, score and bound acceptance checks.
- Biological interpretation (10%): compare matched-taxon nuclear/plastid trees,
  source-coordinate site changes and ties without equating score with truth.

The concrete cards, first-step commands and acceptance gates are in
`discover/catalog.json`; weights and revision policy are in `discover/priority-log.md`.
The seeded picker is `python3 scripts/pick.py --seed 0123456789abcdef0123456789abcdef`.
All choices are local; no claims or messages are posted automatically.

## Evidence and review

Run `python3 scripts/check.py`. A fresh checkout needs only Python 3.10+ and no
network, packages, proprietary software or GPU. Each saved tree is rescored using
four-state Sankoff DP independent of the search Fitch code. Exhaustive 3–8 taxon
counts, brute-force internal-state quartet tests, root invariance, invalid-input
rejection, NNI connectivity, published site scores and data curation replay are
included. This is author-checked evidence, not formal proof or independent review.

Contributions must contain dataset ID/hash/profile, Newick, claimed score, command,
seed, budget, algorithm version/base commit and verifier output. The check confirms
the given topology's exact score. A global optimum additionally needs completed
exhaustive coverage or an independently checked lower bound meeting the score.
Heuristic comparisons must preserve inputs and report unsuccessful runs; timing
claims require interleaved/A–A controls and a documented environment. Existing
wall times are descriptive and may reflect other work on this machine.

Project maintainer: [@Mister-Meeseeks](https://github.com/Mister-Meeseeks). The
owner authorized repository publication and a hub registry PR. `discover.json`
permits listing by `discoveryathome/discover`; no hub push permissions are granted.
Review remains paused pending hub assessment, declared capacity and independent
verification. Naming a maintainer is not acceptance of the scientific frontier;
all present evidence remains author-checked.

Review gates: reproduce identity and score; inspect structural validity; audit
comparison scope and provenance; then have the maintainer decide acceptance. Do not
replace the verified frontier merely because a search program reports a lower score.
Review capacity, not donated compute, will set the pace. The verifier and frontier
are the most consequential files to review carefully.

## Credit

Original code and prose use MIT; third-party terms remain intact. Record human and
agent contributions honestly in CONTRIBUTORS.md and result provenance. Credit data
creators through the study and software citations. Acknowledge verification and
negative findings. Authorship is by substantive contribution and agreement, never
promised automatically for donated runtime. No independent reviewer or biological expert has endorsed the scientific claims.

Lower parsimony score does not prove that a tree reflects the true evolutionary
history. The fixed-alignment objective does not resolve alignment uncertainty,
long-branch attraction, gene/species-tree differences or statistical support.

## Launch progression and honest progress

The collection has 17 immutable alignment rows across three empirical studies,
plus published tutorial controls. Subsets from one study are not independent
replicates. The picker balances studies within the improved-tree track; settled
rows are reserved for verifier or heuristic controls, never advertised as beatable.

A first session should reproduce a control, make one bounded experiment, verify
its output, and leave an exact receipt. Useful accepted results include a better
witness, a stronger bound, improved all-seed heuristic performance, a minimized
verifier bug, or a careful mapped analysis. Merely rerunning a known result is
onboarding evidence, not a new discovery. Raw scores cannot be summed across rows
as a scientific measure; show row-specific changes, closed gaps, and accepted
artifacts separately. No known improvements are withheld to manufacture wins.

`results/expansion-benchmark.json` contains predeclared seeds 0..19 on four panels,
plus smaller probes elsewhere, and source-start runs. These automated probes
show attainable changes from the old baselines. They do not estimate the chance
of improving the newly updated frontier in a donated 30–60 minute agent session.
Before a public launch, run a small supervised contributor trial against a frozen
commit and measure verified useful outcomes, time to first result, review effort,
and failures. Do not promise every session a new lower tree score.

To deepen the work: compare an established parsimony package on the same inputs;
add SPR/plateau search and held-out seed/study evaluation; improve certified
bounds; examine tied trees and partition-specific conflict. These are separate
research claims with separate evidence gates. New ambiguity or gap semantics,
or new column selections, require new profiles/rows, never a silent score change.

## Donor workflow trial 001

A randomly selected, bounded contributor trial produced a verified proposal for
`pythonidae-16s-12`: **95 → 93**. The first improvement appeared after about three
minutes; the full session receipt and limitations are in
[the trial report](results/donor-trial-001/REPORT.md). The recorded frontier remains
frozen pending review. Score 93 is already known and must not be counted as a new
discovery in subsequent trials.

## Coordination while review is paused

GitHub Issues and PRs are the public coordination record. Read them before starting
work and check the known score-93 donor-trial proposal before claiming novelty.
Prepare local receipts while donor admission is paused. Posting requires explicit
authorization in the current session; the repository does not grant it by itself.
Historical HANDOFF.md and verification records describe their original local runs.
