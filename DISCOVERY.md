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
also settle the six-taxon empirical subset. Larger incumbents are local upper
bounds, not literature records. `discover/frontier-rows.json` is authoritative.

## Bottleneck and research tracks

The verifier is cheap; escaping local topology minima without losing reproducibility
is the research bottleneck. Score ties can conceal very different trees. NNI misses
the published eight-taxon optimum from the shipped random starts; more compute on
the same strict-descent path is not a guarantee of improvement.

- Improved trees (30%): search the open 12- and 24-taxon rows, keep exact witnesses.
- Better heuristics (30%): add plateau handling, SPR or a ratchet; compare paired
  seeds and equal evaluation budgets, report all runs and success rates.
- Verifier audits (25%): attack parser and graph checks, independently cross-check
  the scoring recurrence and exact enumeration; expand safe counterexample tests.
- Biological interpretation (15%): explain alternative splits and site conflicts,
  filtering and gene-tree limitations; do not equate a smaller score with truth.

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
