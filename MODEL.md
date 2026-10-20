# Scoring contract: unordered-unit-strict-v1

For each fixed alignment, minimize the sum over sites and tree edges of 1 when
endpoint states differ and 0 otherwise, minimizing over all internal states in
{A,C,G,T}. Every site has weight one, including constant and uninformative sites.
No transition/transversion distinction, branch length cost, threshold, codon model,
site exclusions, or biological root constraint applies. The integer score is exact
for a given topology; it is not a certificate of global optimality.

FASTA IDs must be unique nonempty ASCII letters/digits/underscore/dot/hyphen with no
description. Sequences must have equal positive length, at least three taxa, and
uppercase fully specified nucleotides. DNA accepts ACGT; RNA accepts ACGU and maps
U bijectively to T for scoring. Mixed T/U input is rejected. Identical sequences
remain separate labeled taxa.

Gaps (`-`, `.`), missing values (`?`, `N`, `X`), and ambiguous IUPAC symbols
(`R Y S W K M B D H V`) are REJECTED, never silently assigned a state or deleted.
No fifth-state, polymorphism, or set-valued ambiguity semantics are implemented.
Real source files containing these symbols are archival inputs only. Curated
instances explicitly select taxa, then keep only columns fully specified for all
selected taxa. Original 1-based coordinates and label mappings are saved; this
creates a NEW fixed instance. It cannot inherit a score published for the source.
An eventual ambiguity or gap profile requires a new version and independent tests.

Candidates contain exactly one semicolon-terminated Newick tree. Accept binary
rooted syntax (top degree two, suppressed on import) and unrooted syntax (top
degree three). All remaining internal vertices must have degree three. Leaves
must equal alignment taxa exactly, once each. No sampled ancestors, internal
labels/support, comments, forests, unary nodes or polytomies. Quoted leaf names
with doubled apostrophes are supported, but must still match accepted FASTA IDs.
Underscores are literal. Optional finite nonnegative decimal branch lengths are
parsed and ignored; omitted lengths are fine. Root position has no effect under
this symmetric cost model. Newick is normalized at an edge incident to the
lexicographically first leaf. A tree is connected, acyclic, with n leaves, n-2
internal vertices and 2n-3 edges. Input size/nesting limits are documented errors.

The reference checker uses four-state Sankoff dynamic programming, with integer
costs and no search imports. The search uses a separate Fitch set recurrence and
weighted identical-site compression. Every saved search tree is rescored by the
reference checker. Both share the parser, so parser tests and graph validation are
also required; these are independent algorithms, not independent human review.

A site with d observed states has at least d-1 changes. The sum is a safe lower
bound, usually loose. Exhaustive labeled unrooted binary enumeration inserts the
next sorted taxon into every edge. Removing that last leaf and suppressing its
neighbor gives a unique predecessor, proving completeness and no duplication.
The count is (2n-5)!!: 1, 3, 15, 105, 945, 10395 for n=3..8. Only completed runs
with matching counts can establish optima. Exhaustive CLI refuses n>8.

A lower parsimony score does not prove that a tree reflects the true evolutionary
history. Homoplasy, long-branch attraction, alignment uncertainty and model
misspecification can matter; mitochondrial gene trees need not be species trees.

## Independently checked pair bounds

Two biallelic columns exhibiting all four combinations of their states cannot
both have score one on a tree: score one induces an edge split, and two edge splits
cannot cross in all four intersections. Each column costs at least one, so their
joint score is at least three. Disjoint such pairs raise the sum-of-distinct-states
lower bound by one per pair. Columns must not be reused. This argument is
independent of how the pairs were found.

`bounds.py` generates pairs using bit masks and greedy seeded matching. Its checker
uses direct character sets and checks all four combinations, biallelic states,
disjointness, indices and arithmetic. The CLI also checks dataset/hash/profile.
The initial certificate is the best of seeds 0..19; no maximum-matching claim is
made. Improving matching or proving stronger site-set bounds is useful progress.
A bound meeting a witnessed score settles that row. A wide gap does not imply
that a better tree exists.

## Expansion curation

The original five alignments remain byte-for-byte fixed. New alignments first
exclude taxa with fewer than 80% fully specified nucleotides in the chosen source
window (both source matrices for paired Ferula rows), select evenly spaced sorted
eligible taxa, then retain complete-case
columns. This is an engineering choice, not biological representativeness. The
additional full eligible CYTB row has 29 taxa; four source taxa fail coverage.
It is a different alignment from the old 24-taxon row, not an extension on which
raw scores can be compared.

Source lowercase is explicitly uppercased. NEXUS match characters are expanded
relative to the first sequence only in the archival importer. Numeric support
labels are stripped from source ML trees before pruning; candidate syntax remains
unchanged. Every selected source column and excluded taxon is recorded. Source
formats are narrowly parsed, not a general-purpose alignment importer.
