# Multistate pair-bound proposal: Pythonidae CYTB 12

**Proposed lower bound: 446, up from 392**, on the unchanged
`pythonidae-cytb-12` alignment. The known tree still scores 575; the unresolved
interval becomes **446–575** if this new bound type is accepted. Neither the
accepted historical record nor the working table is changed by this package.
Evidence is **author-checked**, with two algorithmic implementations; it is not
independent human review or maintainer acceptance.

The seeded card's suggested maximum-matching experiment cannot improve its old
certificate. There are 170 biallelic columns, but only 98 have any incompatible
partner (2,568 graph edges). Each admissible pair consumes two active columns,
so every matching has at most 49 pairs. The existing witness already has 49,
giving `343 + 49 = 392`. A blossom implementation would not improve that limit.

The one bounded pivot uses multistate columns and the established two-character
method of [Bruen & Bryant (2008), DOI 10.1007/s00026-008-0335-4](https://doi.org/10.1007/s00026-008-0335-4).
This is an application and certificate contribution, not a new theorem or a
claim of an optimal weighted matching.

## Fixed object and witness

- Base commit: `9f8e6e7649aafb1eed0cd952ce59a7a2d4379810`.
- Task seed: `fa303cb791991297aabd7dc42c2d43e1`; project picker revision 5,
  track `stronger-bounds`, card `bound-pairs`.
- Alignment SHA-256: `b5b57b5a2eec060601144a090d0f68c6ebaee9164089dfe6c518c0a6f43c891e`.
- Profile: `unordered-unit-strict-v1`; all 12 taxa and 647 unit-weight sites retained.
- Witness: [pythonidae-cytb-12.json](pythonidae-cytb-12.json), 80 disjoint pairs.
- Base 343 plus 60 pair bonuses of 1, 17 of 2, and 3 of 3: **446**.
- Generator: greedy descending cycle rank, with shuffled ties for seeds 0–99;
  seed 61 supplies the first best witness. Every trial's bound and pair count
  is retained in the certificate. Unselected witnesses can be regenerated.

All 100 outcomes: 441 (10 runs), 442 (28), 443 (28), 444 (23), 445 (10),
446 (1). Certificate SHA-256:
`098909a54d4390615d2be0da8b006669dd6369d9e762b10a55907618b95a9a17`.

The graph contains 7,307 positive-weight edges on 163 active columns: 6,719
edges of weight 1, 564 of weight 2, and 24 of weight 3. The generator searches
only 100 greedy pairings. It does not find or certify a maximum-weight matching.

## Bound and checking argument

For two sites, construct a bipartite graph with a separate vertex for each
observed state on each site. Distinct observed state pairs are edges. With `m`
edges and `c` components, their exact joint optimum is `m + c - 2`
(Bruen & Bryant, Theorem 4.2). Subtract the two single-site minima to obtain
the nonnegative cycle-rank bonus. Bonuses add only for disjoint column pairs.

A direct lower-bound argument: assign both characters to all vertices of any
tree, split edges changing twice into two unit changes, and contract zero-change
edges. Its score equals its edge count. It contains the `m` observed pair labels.
If `h` additional distinct pair labels occur, connectedness requires `h >= c-1`:
adding one pair can join at most two state-graph components. The tree has at
least `m+h` vertices, hence at least `m+c-2` changes. Sum this inequality over
disjoint pairs and use `d-1` for each remaining site.

[generate.py](generate.py) computes cycle ranks with union/find.
[verify.py](verify.py) independently computes each two-site optimum using Prim's
minimum spanning tree on observed pairs with two-coordinate Hamming costs
(Theorem 5.2). An MST is exact here because there are **exactly two** unordered
unit-cost characters; do not use this checker as a general multi-site MST bound.
The implementations share the repository's strict alignment loader, not a pair
scoring routine. Verification checks dataset/hash/profile, integer arithmetic,
column range and disjointness, independently of generator metadata.

## Replay

From the repository root, using only Python 3.10+ and its standard library:

```sh
python3 phylo.py verify-bound pythonidae-cytb-12 results/pythonidae-cytb-12-bound.json
python3 research/multistate_pairs_20261023/verify.py research/multistate_pairs_20261023/pythonidae-cytb-12.json
python3 research/multistate_pairs_20261023/generate.py pythonidae-cytb-12 --seeds 100 --out .scratch/multistate-pairs-replay.json
cmp research/multistate_pairs_20261023/pythonidae-cytb-12.json .scratch/multistate-pairs-replay.json
python3 -m unittest discover -s tests -p test_multistate_pairs.py -v
python3 scripts/check.py
```

Expected original control: `{"valid": true, "bound": 392}`. The research checker
must report `valid=true`, `bound=446`, `bonus=103`, `pairs=80`, and the binary-pair
ceiling 392. The production `phylo.py verify-bound` intentionally does not accept
the new research schema; integrating a new verifier requires separate review.

The new tests enumerate every unrooted binary tree on 3–6 taxa and every
unordered pair of canonical characters with at most four states: **19,039
character-pair cases**, modulo state relabeling and exchange of the two sites.
Both pair implementations must equal the minimum summed Sankoff score in each
case. Additional controls cover disconnected cycles, repeated taxa, taxon
permutations, the original ceiling, and malformed or inflated certificates.
These are finite implementation checks, not a proof by enumeration for 12 taxa.

[verification.json](verification.json) retains the exact verifier output,
commands, environment and source/artifact hashes. The full repository gate
passed, including all 22 unit tests and the new controls; regeneration was
byte-identical. The existing upper witness was separately checked at 575.
Shared-machine durations are descriptive, with no speed comparison claimed.

## Scope and limits

The mathematical lower-bound argument applies to the full fixed alignment;
finite enumeration checks the implementations on small instances. No better
tree was sought, no 12-taxon exhaustive topology search was run, and the bound
does not settle this row. Search metadata is reproduced by replay, not trusted
by the mathematical checker. The two implementations and tests were written
by the same AI agent and share input loading and repository tree enumeration.
Independent scientific review remains open. No performance superiority or
biological-history claim is made, and other frontier rows are outside this result.

## Open next questions

1. Independently review the two-site theorem's use under MODEL.md, the certificate
   checker, and the explicit 80-pair witness. Success: reproduce 446 and reject
   the corruption controls without relying on this generator.
2. Can maximum-weight matching beat the greedy bonus 103 on this weighted graph?
   First reproduce the saved certificate; then retain a heavier disjoint pairing
   and check it with `verify.py`. An optimum claim needs a checkable upper bound.
3. After reviewing the new bound type, apply it to other existing fixed rows;
   compare each proposed bound separately with its immutable identity and known
   upper bound. Do not update accepted records without maintainer authorization.

## Credit

Bruen & Bryant supply the two-character results; earlier partition-and-matching
lower bounds include [Foulds, Penny & Hendy (1979)](https://doi.org/10.1007/BF01732869).
This package builds on the project's original `bounds.py` generator, independent
pair checker, exact Sankoff scorer, exhaustive tree enumerator, fixed alignment
curation and existing 49-pair certificate at the base above. Pythonidae source
data are credited to Rawlings, Rabosky, Donnellan & Hutchinson (2008), with the
fixture and comparator from DendroPy contributors; see THIRD_PARTY.md.
OpenAI Codex implemented this research package for @thakrarsagar on 2026-10-23.
Project maintenance by @Mister-Meeseeks does not imply acceptance of this result.
