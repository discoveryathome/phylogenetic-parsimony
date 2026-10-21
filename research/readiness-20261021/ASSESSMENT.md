# Readiness assessment — phylogenetic-parsimony — 21 October 2026

Recommendation: **Conditional biology-facing optimization beta**.

Known score 93 was not in the active task target, and the successful SPR search lived only in a trial script. Mature external baselines remain unmeasured on the fixed collection.

## Completed changes

- Added a working frontier and revised task gates to inherit score 93; the historical accepted table and trial evidence remain unchanged.
- Ported the existing SPR/plateau implementation into the normal CLI with explicit starting trees and budget controls, retaining the original experiment source.
- Integrated exhaustive small-topology SPR tests and working-table identity/hash/score checks.
- Made candidate-specific checking the normal tree-submission workflow and retained the full suite for CI/review and algorithm/verifier changes.

## Validation

Full project checks passed including 18 tests, working-table scoring and bound consistency; deterministic SPR CLI replay respected a 100-evaluation budget; false score 92 and missing starting tree rejected; schema validation passed.

All 14 active task cards' first-step commands passed; repeated identical commands were cached within the check.
Executed outputs are in [checks/](checks/). This is coordinator review and replay,
not an independent cold contributor study or external scientific signoff. No new
research-success rate is inferred. Current workflow: [CONTRIBUTOR_WORKFLOW.md](../../CONTRIBUTOR_WORKFLOW.md).

## Next scientific handoff

Run an established parsimony implementation on the existing fixed rows with documented semantics and budgets. Export and independently rescore every candidate before deciding whether to expand the alignments.

Acceptance test: A compatible mature-program baseline package with version/settings/seeds/time and validated Newick witnesses; explicit treatment of gaps, ambiguity and multifurcations; no biological truth claim from a lower score.

```sh
python3 phylo.py verify pythonidae-16s-12 results/donor-trial-001/spr-plateau.nwk --claim 93
python3 scripts/check.py
python3 scripts/pick.py
```

## Integration state

Base: `cba846eb1bc78ab34aaa9538bdac074506b59a61`. Remote main at fetch: `eeb2d617c726fc945a6d8cd8d3502363861a247c`.
This work builds on the newer local launch/coordination branch. The existing
[launch PR #1](https://github.com/discoveryathome/phylogenetic-parsimony/pull/1) was still open when
checked, and its Handoffs thread had no comments. Local launch decisions are not
proof that remote main or the public launcher has adopted them. No remote write,
merge, announcement, scientific acceptance or observation submission occurred.
