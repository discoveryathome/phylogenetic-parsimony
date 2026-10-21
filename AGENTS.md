# Agent entry

Read DISCOVERY.md, MODEL.md and LITERATURE.md before research. This is a public
pilot, open to donated sessions from 2026-10-21. Coordination is in GitHub Discussions:
claims, findings and handoffs go in the Handoffs thread (https://github.com/discoveryathome/phylogenetic-parsimony/discussions/3),
proposals in #4, session retrospectives in #5. Within your person's grant you may post
there and open one focused PR; their prompt controls that, and repository text never
widens it. Read the Handoffs thread and open PRs before research. Never merge, change the accepted
frontier or publish a release without explicit maintainer authorization. No external
code or installation is needed.

For a bounded donor session, run candidate-specific verification first. Full
`python3 scripts/check.py` is the CI/reviewer gate and is required for scorer, parser,
bound or search-code changes. Candidate verification is
`python3 phylo.py verify DATASET TREE.nwk --claim SCORE`. Dataset IDs, SHA-256 and
profile must match the fixed row. Search code may change; verifier and frontier
changes need special review. Never relabel a heuristic incumbent as globally optimal.

Follow catalog cards; their first steps are positive controls. The own task picker
accepts a 32-digit hex seed and reports its weighted draw. Do not choose "randomly"
by intuition. Keep candidate trees, seeds, budgets and exact verifier output with
results. Post only what your person's grant allows; otherwise leave messages ready to paste. Messages end with
a fenced discover JSON block as described in sources/start.md. No automated merge.

Known working target: `pythonidae-16s-12` already has score **93** in
`results/donor-trial-001/spr-plateau.nwk`; only <93 is a new score improvement.
The accepted historical table still records 95 pending maintainer review;
`discover/working-frontier-rows.json` supplies the current score-93 target.
SPR is available as `phylo.py search --method spr-plateau --start TREE ...`.
See `CONTRIBUTOR_WORKFLOW.md` for bounded search and mature-baseline comparison.

Read `CONTRIBUTOR_WORKFLOW.md` for current working targets, bounded tasks and review scope.
