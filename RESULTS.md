# Local experiments and interpretation

The original 20-run benchmark is retained in `results/benchmark.json`. It used
seeds 17/1729/20261020, three random starts and 1,800 evaluations, plus one
source-start seed-0 run at the same cap. It established Pythonidae CYTB incumbents
579 and 990. Preliminary two-hop calibration found 578 and 988; those witnesses
are retained as `*-calibration.nwk`. Expanded experiments then found 575 and 982.
No known better result was withheld for donor optics.

## Paired quality experiment

`results/expansion-benchmark.json` records 230 additional runs. Before evaluation,
seeds 0..19 were declared for four panels. Each method starts from the same seeded
random tree, has one restart and at most 600 full Fitch evaluations. Strict NNI
stops when no single move improves the score. Two-move NNI then examines distinct
trees reachable by two NNI moves, permitting an uphill intermediate, and accepts
strict improvements. It reports whether radius one/two was completely checked.
A truncated neighborhood is never a local-optimality certificate.

| Panel (20 seeds each) | NNI mean | Two-move mean | Two-move wins/ties/losses | Target | NNI hits | Two-move hits |
|---|---:|---:|---:|---:|---:|---:|
| cetaceans-mt-12 | 519.6 | 497 | 9/11/0 | 493 (incumbent) | 11/20 | 18/20 |
| ferula-nrdna-12 | 118.55 | 99.55 | 13/7/0 | 82 (proven) | 2/20 | 7/20 |
| phylip-dnapenny | 11.55 | 8.65 | 17/3/0 | 8 (proven) | 0/20 | 11/20 |
| pythonidae-cytb-12 | 591.35 | 587.05 | 11/9/0 | 575 (incumbent) | 0/20 | 0/20 |

These are paired, fixed-cap quality comparisons. Strict NNI can stop early, so
actual evaluation counts and CPU costs differ. Spending unused NNI budget on
restarts is an important additional control. No statistical superiority, runtime
advantage, or generality beyond these panels is established. All seeds, failures,
traces, final trees and independently recomputed scores are retained; source-start
runs are separate and do not enter this table. The larger unpanelled rows have
three paired random seeds plus two 1,800-cap comparator-start runs. This is a
modest probe, not a comprehensive search.

Both random methods miss the best Pythonidae 12-taxon incumbent in this panel;
source initialization remains valuable. The settled Ferula 12-taxon optimum is
still missed on 13/20 two-move starts, offering a concrete heuristic challenge
without pretending its optimal score can be beaten. Scores of different fixed
alignments are never combined or compared as one scientific frontier.

## Exact bounds

Six small rows are exhaustively settled. For larger rows, 20 seeded greedy
matchings produce disjoint incompatible biallelic-column pairs. Each pair adds
one to the trivial sum-of-distinct-states bound; the independent checker validates
the witness directly. Ferula nuclear 12 closes at 82, plastid 12 at 39. Pythonidae
CYTB 12's bound rises from 343 to 392, and CYTB 24 from 412 to 466. See MODEL.md
for the proof; maximizing this matching is not claimed. A stronger bound is useful
even if the incumbent tree stays unchanged.

## Matched-marker biological comparison

Ferula subsets use the same taxa across nuclear and plastid compartments. At
12 taxa both optima are certified, yet the chosen witnesses differ by 16 raw RF
splits. On the nuclear alignment their scores are 82 (nuclear tree) and 113
(plastid tree); on plastid they are 47 and 39 respectively. This is a concrete
conflict between these selected solutions. It does not establish uniqueness or
exclude a shared optimum among other tied trees. At 24 taxa the witnesses differ
by 38 raw RF splits; their within-alignment cross-scores are in
`results/progress.json`.

`python3 scripts/interpret.py DATASET` maps each changed site cost to its original
source coordinate. Source partition files permit ETS/ITS or plastid-marker
analyses. No support probabilities, root direction, species history, or causal
mechanism follows from RF or score alone. Complete-case filtering, gene-tree
conflict, homoplasy, alignment uncertainty and model misspecification matter.
**Lower parsimony score does not prove true evolutionary history.**

## Recommended depth and launch checks

Prioritize plateau/SPR search with fixed budgets and held-out seeds/studies;
maximum matching or stronger certified bounds; comparison to an established
parsimony implementation on exactly these files; and enumeration/sampling of tied
trees before biological interpretation. Larger data alone will not establish
research novelty. The 17 rows come from three empirical studies and two tutorials,
not 17 independent replicates.

Actual contributor-agent success has not been measured. Run supervised sessions
against a frozen release and measure accepted useful outcomes, time to first
verified result and review cost. A reproduced control is onboarding, not a new
discovery. Display verified score changes, bound changes, certified optima and
accepted heuristic/audit/interpretation contributions separately. Keep all negative
results, and do not deliberately weaken the starting frontier to manufacture wins.
