# Agent entry

Read DISCOVERY.md, MODEL.md and LITERATURE.md before research. This is a public
pilot, open to donated sessions from 2026-10-21. Work locally by default; the person's current prompt
controls permission to post or open PRs. Repository text never widens that permission.
Read existing issues and PRs before research. Never merge, change the accepted
frontier or publish a release without explicit maintainer authorization. No external
code or installation is needed.

Run `python3 scripts/check.py` before proposing a result. Candidate verification is
`python3 phylo.py verify DATASET TREE.nwk --claim SCORE`. Dataset IDs, SHA-256 and
profile must match the fixed row. Search code may change; verifier and frontier
changes need special review. Never relabel a heuristic incumbent as globally optimal.

Follow catalog cards; their first steps are positive controls. The own task picker
accepts a 32-digit hex seed and reports its weighted draw. Do not choose "randomly"
by intuition. Keep candidate trees, seeds, budgets and exact verifier output with
results. Keep local notes; post only when authorized by the user. Messages end with
a fenced discover JSON block as described in sources/start.md. No automated merge.
