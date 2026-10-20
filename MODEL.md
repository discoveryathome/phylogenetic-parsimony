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
