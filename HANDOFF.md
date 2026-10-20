# Local handoff — not posted

Destination: the next authorized local contributor or future accepting maintainer.
No GitHub repository, remote, issue, discussion, hub application or external message
was created. The implementation commit below passed reproduction from a fresh local
clone, including all 13 test methods and exhaustive controls. All 20 recorded seed
runs replayed exactly. All five catalog first steps passed. Official protocol
validation is conformant: five cases, two open. Raw receipts are in
`results/validation.txt`; setup support and a fresh clone remain in `../.task-support/`.

Current best scores: PHYLIP RNA 19 (proven), PHYLIP DNA 8 (proven), Pythonidae six
343 (proven), Pythonidae twelve 579 (upper bound), Pythonidae twenty-four 990
(upper bound). The latter two improve the documented source comparators 591 and
1013, respectively. No published record is claimed for these derived instances.

Start with README.md and DISCOVERY.md. Recommended challenges are beating 579 or
990, escaping the score-9 eight-taxon local minimum, auditing the verifier, and
explaining changed splits/sites. The exact acceptance boundary is MODEL.md.

An accepting maintainer, review capacity and independent review remain open.
The placeholder maintainer entry is not consent; no donors should be launched yet.
Changes to the verifier and frontier deserve the most care, and review capacity
will set the pace. Lower parsimony score does not establish true evolutionary history.

```discover
{"v": 0, "kind": "handoff", "task": "improve-12", "scope": "Complete LOCAL parsimony pilot: five fixed alignments, exact verifier, three settled optima, two open empirical rows; no consenting maintainer", "base": "769c4de1e142542c7e9a5addcbfc8b555ff23295", "posted_at": "2026-10-20T05:02:20.662657Z", "evidence_level": "local-only", "request": {"question": "Can a verified tree beat 579 on the fixed pythonidae-cytb-12 alignment?", "first_step": "python3 phylo.py verify pythonidae-cytb-12 candidates/pythonidae-cytb-12-best.nwk --claim 579", "success_test": "Identical alignment SHA-256 and profile, structural validation passes, reference score below 579.", "track": "improved-trees", "est_minutes": 60}}
```
