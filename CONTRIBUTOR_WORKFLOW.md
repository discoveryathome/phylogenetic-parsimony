# Contributor workflow — 21 October 2026

Start with `python3 scripts/pick.py`. The working table is
`discover/working-frontier-rows.json`; it includes the score-93 trial tree and four PHYLIP improvements.
The historical accepted table remains unchanged. A new score result on
pythonidae-16s-12 must beat 93, not 95, pending independent scientific acceptance.

```sh
python3 phylo.py verify pythonidae-16s-12 results/donor-trial-001/spr-plateau.nwk --claim 93
python3 phylo.py search pythonidae-16s-12 --method spr-plateau --start results/donor-trial-001/spr-plateau.nwk --seed 1729 --budget 5000 --out research/new-session/tree.nwk
```

Choose a fresh recorded seed for new work; 1729 above is a reproducible example.
The ordinary CLI now supports `spr` and `spr-plateau` from an explicit start tree.
The verifier independently recomputes the score. Evaluation caps are not wall-time
caps: additionally stop at the session budget and leave time for validation.
SPR local completion never proves a global optimum. Original trial source remains
frozen; the reusable method is covered by small exhaustive topology tests.

For tree-only contributions use the lightweight `phylo.py verify` command and
save its output. Full `python3 scripts/check.py` belongs in CI/review and is required
for scorer, parser, bound or algorithm changes. This keeps an ordinary witness
submission from spending most of its budget on whole-project verification.

The first mature baseline is complete: [PHYLIP comparison](research/scientific-audit-20261021/REPORT.md).
The mature-baselines card now asks for another established implementation against
the inherited targets. Record version, settings, seeds, input hashes and budgets.
Preserve all taxa and columns; explicitly reconcile gap/ambiguity semantics and
multifurcations. PHYLIP's 251 raw and converted scores were independently checked;
all explicit resolutions preserved their scores. Do not infer biological truth
or global optimality from a mature program's reported optimum.

Do not grow the collection solely because one donor session was quick. Establish
stronger baselines and cold-start outcomes across existing studies first. Lower
parsimony score alone does not establish biological truth or statistical support.

## Session receipt and review

Record the base commit, selected task and seed, input and output hashes, commands,
budget and elapsed time, successful and failed attempts, verification output,
and what remains unresolved. Check the live Handoffs Discussion before claiming
work. Post or open a focused PR only within the contributor's authorization.
A task draw is advisory; it does not reserve work.

A useful outcome can be a new witness, an independently checked result, a
source-backed correction, or a reproducible blocked handoff. Repeating a known
positive control is onboarding evidence. Review records must distinguish code
replay, independent implementation, scientific review and maintainer acceptance.

For the next monitored cohort, record cold-start orientation time, first useful
artifact, reviewer minutes, acceptance latency, duplicate work and unsuccessful
sessions. Later sessions inherit every known valid result. A lack of improvements
is evidence to revise the task pool, not a reason to reset it to weaker baselines.
