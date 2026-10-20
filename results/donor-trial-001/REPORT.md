# Donor workflow trial 001

**Result: one new independently checked candidate, score 95 → 93, in a session
capped at 30 minutes.** The first verified improvement arrived at 3 minutes 6 seconds;
the final score arrived at 3 minutes 40 seconds. The submission package was ready
at 11 minutes 4 seconds. The session ended early after verification;
it did not consume a full 30 minutes.

This tests one workflow with an agent already familiar with the project. It is not
a blinded first-time onboarding study, an independent human review, or an estimate
of the population success rate of donors. No parallel agents were used.

## Frozen task and selection

- Base: `91d7005f18e5d9a7eb508c6dfdc69bc874a8af59`.
- OS-random picker seed: `00147e30ac32b66f7660ac6ba94f2e78`; exactly one draw, no reroll.
- Selected track/card: `improved-trees` / `improve-pythonidae-16s-12`.
- Dataset: `pythonidae-16s-12`, 12 taxa × 433 sites.
- Alignment SHA-256: `e8a029504a8a4fc2f843c84f743dc708ec17e502ca1c0488d79a6ce1e1c7fdc9`.
- Scoring profile: `unordered-unit-strict-v1`.
- Frozen incumbent: 95; certified lower bound: 70.
- Success criterion fixed before searching: valid Newick on identical input,
  independently recomputed score below 95. Reproducing a control alone does not count.

The final tree and provenance are in [submission.json](submission.json) and
[spr-plateau.nwk](spr-plateau.nwk). **The score-93 candidate is already known from
this trial; rediscovering it in a later session is not a new result.** It is a
proposal awaiting review, not an automatically accepted frontier change.

## What happened

| Attempt | Result | Fitch evaluations / cap | Interpretation |
|---|---:|---:|---|
| Verify shipped incumbent | 95 | reference checker | Positive control reproduced |
| Supplied two-move NNI | 95 | 207 / 5,000 | Completely checked radius two; no improvement |
| New strict SPR search | 94 | 593 / 5,000 | First new independently checked witness |
| New SPR with equal-score traversal | 93 | 8,510 / 20,000 | Further improvement; 33 score-93 plateau trees expanded |

The implementation cuts each oriented edge, suppresses the parent vertex in the
remaining component, and reattaches the subtree on each possible remaining edge.
It deduplicates canonical Newick strings. The second experiment explores connected
equal-scoring alternatives before stopping. SPR and searching tied trees are
established methods described in the [PHYLIP documentation](https://phylipweb.github.io/phylip/doc/main.html).
This is an original small implementation, not a claim of algorithmic novelty or
superiority to mature software. Different evaluation counts, caching and CPU load
prevent treating these runs as an equal-cost performance comparison.

The final search exhausted its reachable equal-score component and outgoing SPR
moves under this implementation. That does **not** establish global optimality.
The remaining certified interval is 70–93. Lower parsimony score does not prove
that the tree reflects true evolutionary history.

## Verification and observed effort

- Exact reference DP checked each improvement, and the separate unchanged CLI
  accepted 93. Claiming 92 for the same tree was correctly rejected.
- Both experiments replayed identical final trees, scores, histories, evaluation
  counts and completion flags.
- Two new tests cover all five-taxon tree neighborhoods: valid topology, distinct
  neighbors, NNI inclusion, reversibility and independent score agreement. They
  also check deterministic seeds, evaluation budgets and a known small optimum.
- The complete project check passed: curation replay, all recorded baseline
  witnesses and bounds, exhaustive controls, and all 16 existing test methods.
- Core scorer, validator, alignments, frontier and catalog were unchanged.

The final candidate's standalone CLI check took 0.60
seconds in this run. The full project check took 402.5
seconds. These are descriptive wall times with overlapping work, not speed claims.
No actual human review was performed or timed. Full-suite checking is affordable
inside this cap but much more expensive than verifying one candidate.

One setup attempt failed because this trial's wrapper constructed the sandbox
profile path incorrectly; the retry fixed it. The failed receipt and stderr are
retained. This was a harness error, not a project scorer failure. The stock search's
non-improvement is also retained, rather than reporting only successful attempts.

## What this says about launch readiness

This is encouraging evidence that a randomly selected open row still offers useful
progress after initialization. It supports proceeding with the current collection
for a small cohort. It does not establish that most donors will succeed or that
all tracks are equally accessible. Prior familiarity probably shortened orientation
and implementation time.

The card, frozen alignment, exact checker and small tests made the work concrete.
The supplied search stopped with a useful diagnostic, but obtaining the improvement
required implementing a broader neighborhood. Less experienced contributors may
need more time there. A standard timed-session/receipt command would reduce wrapper
friction. Full-suite checks could be shared at batch-review time while retaining
mandatory candidate checks, subject to the accepting maintainer's policy.

Continue the planned sequence of independent sessions across the task distribution,
recording failures and reviewer effort. Later sessions must treat this score-93
proposal as already known. Do not enlarge the dataset pool solely because this
one session finished early, and do not infer a 100% donor success rate from it.

## Reproduce from the repository root

```sh
python3 phylo.py verify pythonidae-16s-12 results/donor-trial-001/spr-plateau.nwk --claim 93
PYTHONPATH=src python3 experiments/donor_trial_001/test_spr.py
python3 experiments/donor_trial_001/run.py --budget 5000 --seed 1729 --name check-strict
python3 experiments/donor_trial_001/run.py --budget 20000 --seed 1729 --plateau --name check-plateau
python3 scripts/check.py
```

The experimental runner uses the saved `start.nwk`, not the mutable frontier tree,
so replay survives a later frontier update. Algorithm hashes and exact commands
are in the submission; the original and replay receipts preserve timestamps.
No publication, hub action, external message, dependency installation or automatic
frontier promotion was performed.
