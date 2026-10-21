# Priority revision 3 — 2026-10-21

Donor intake opened. Added card `mature-baselines` to `better-heuristics`: run TNT,
PAUP* or MPBoot on the identical open rows and record verified scores as baselines,
first, so donated search doesn't chase gaps a standard tool closes. Weights unchanged.

# Priority revision 1 — 2026-10-20

30% improved trees: two empirical instances remain open, with cheap checks.
30% better heuristics: strict-descent NNI misses known small optima; escaping ties
and local minima is a concrete bottleneck, supported by the ratchet literature.
25% verifier audits: acceptance depends on exact scoring and a shared parser;
independent review is still missing despite exhaustive differential tests.
15% biological interpretation: explain what improvements do and do not establish,
particularly after complete-case filtering of one mitochondrial gene.

Weights total 100. Review after the first five accepted contributions or on
2026-11-03, whichever occurs first. This is a suggested review date, not a scheduled
automation. No automatic reweighting; an accepting maintainer must decide.


# Priority revision 2 — 2026-10-20

Expanded to 17 fixed alignments from three empirical studies and two tutorials.
30% improved trees; 25% heuristics; 20% certified bounds; 15% verifier audits;
10% biological interpretation. Bounds provide a separate exact progress measure,
and matched nuclear/plastid inputs add substantive interpretation work. All known
improved trees are promoted; settled rows are removed from tree-improvement cards.
Within the tree track the picker selects a study uniformly, then one open row,
so multiple subsets do not monopolize the launch queue.

Four predeclared 20-seed panels compare NNI and two-move NNI at equal 600-evaluation
caps. This is computational calibration, not donor-session yield. Review after
five accepted contributions or on 2026-11-03; assess useful verified outcomes,
time to first result and reviewer load. No automation or public launch is enabled.

## 2026-10-21 contributor readiness

Known results are inherited before new work; see CONTRIBUTOR_WORKFLOW.md and
research/readiness-20261021/ASSESSMENT.md. Updated task selection, bounded work
and review gates preserve scientific evidence status and the recorded launch decisions.
