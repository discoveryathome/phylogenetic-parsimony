# Fixed-alignment parsimony pilot

Find binary unrooted trees minimizing total unordered unit-cost nucleotide changes
for each fixed alignment. A contribution is a Newick witness with an exactly
recomputed integer score. The primary measure is a smaller score on the identical
alignment hash and scoring profile; each alignment is a separate frontier row.
The objective, evidence profile and local build are authorized by the task request.
No donor launcher, public repository or hub application is authorized.

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

No person has agreed to maintain this project or supplied review capacity.
`maintainers` contains an explicit unassigned-role placeholder because the v0
manifest schema requires at least one entry. It is not a consenting person.
Review is paused; no hubs consent record is present. Before inviting donors, appoint
an accepting maintainer, set review capacity, review the verifier and licenses,
replace the local URI with the approved repository and obtain explicit hub consent.
Do not set evidence to maintainer-reviewed without that review.

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
promised automatically for donated runtime. No maintainer or biological expert has
yet endorsed this pilot.

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
