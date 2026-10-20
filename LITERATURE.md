# Evidence brief and benchmark audit

This is optimization of a fixed alignment under the contract in MODEL.md. Progress
means a smaller **verified integer score on that same instance**. Secondary work
compares heuristic reliability at a fixed score-evaluation budget. There is no
single universal parsimony frontier across datasets. An optimal score on a fixed
topology, an optimal topology over all trees, and a biologically correct history
are three separate claims.

| Claim | Status and source |
|---|---|
| Unordered equal-cost parsimony on a given binary tree is exactly computable | Confirmed: Fitch (1971), [doi:10.1093/sysbio/20.4.406](https://doi.org/10.1093/sysbio/20.4.406). This pilot independently implements a Fitch scorer and a four-state dynamic-programming checker. |
| Searching all topologies is hard even though scoring one is cheap | Confirmed in White & Holland (2011), [XMP](https://doi.org/10.1093/bioinformatics/btr147). Their work motivates exact small controls, branch-and-bound, site-pattern compression and heuristic initial bounds. It is not a claim that our implementation matches XMP performance. |
| PHYLIP RNA example scores 19 | Confirmed by the [Dnapars manual](https://phylipweb.github.io/phylip/doc/dnapars.html), including site scores and a tree diagram. Recomputed locally; all 15 topologies enumerated. |
| PHYLIP eight-taxon DNA example scores 8, with nine optimal trees | Confirmed by the [Dnapenny manual](https://phylipweb.github.io/phylip/doc/dnapenny.html). Recomputed locally over all 10,395 labeled binary unrooted topologies. Duplicate sequences remain distinct taxa. |
| Local NNI minima prove global optimality | False. The shipped seed runs miss even the score-8 tutorial optimum. Exhaustive search settles the small rows; larger rows remain upper bounds. |
| Lower parsimony implies the true evolutionary history | False in general: Felsenstein (1978), [doi:10.1093/sysbio/27.4.401](https://doi.org/10.1093/sysbio/27.4.401), gives conditions in which parsimony is statistically inconsistent. This is a limitation of the inference criterion, not fixed by a better optimizer. |
| Pythonidae derived subset scores are published records | Unverified/not claimed. These newly filtered alignments have no located published MP scores. The baseline is the documented DendroPy MLE fixture pruned to the selected taxa and rescored locally. |

The strongest **established** values for the tutorial rows are the published optima
above; those rows are validation controls, not improvement targets. For the new
empirical rows, `discover/frontier-rows.json` contains local incumbents and safe
lower bounds, never world-record claims. The six-taxon rows are settled by complete
enumeration; larger rows need further search or stronger bounds.

## Public resources considered

- [PHYLIP examples](https://phylipweb.github.io/phylip/doc/dnapenny.html): admitted.
  Small, fully specified synthetic input, explicit published scores, tree diagrams
  and permission to copy documentation without a fee while preserving notices.
  Original HTML and the repository BSD license are retained. These are useful
  correctness benchmarks, not realistic performance benchmarks.
- [DendroPy Pythonidae fixture](https://github.com/jeetsukumaran/DendroPy/blob/b7fc4fd9c70c86a44e10650b3fb9b3be86e9dc77/tests/unittests/data/chars/pythonidae.chars.nexus):
  admitted under its repository BSD-3-Clause license, retained locally. The fixture
  explicitly attributes the data to Rawlings, Rabosky, Donnellan & Hutchinson
  (2008), [Python phylogenetics](https://doi.org/10.1111/j.1095-8312.2007.00904.x).
  Thirty-three snake taxa, 2,716 source characters. We use four CYTB subsets plus 12S and 16S
  subsets, retain exact coordinates, and compare to the source MLE topology.
- [BenchmarkAlignments](https://github.com/roblanf/BenchmarkAlignments): useful
  broader collection; the maintainers identify CC0 or CC BY data and provide
  per-study metadata. The full collection is much larger than this pilot needs;
  individual files must have their own provenance and license checked before
  admission. The linked Figshare page was inaccessible (HTTP 403) during setup.
- [Theriot et al. diatom data, Dryad 610md](https://doi.org/10.5061/dryad.610md):
  potentially useful non-human resource, 208 taxa and 9,349 sites, with explicit
  partitions. Dryad's [terms](https://datadryad.org/terms) specify CC0 for datasets.
  Its alignment download returned HTTP 403; no diatom sequences were admitted.
- [Tree diversity benchmark paper](https://doi.org/10.1186/1471-2105-10-S4-S3):
  useful for comparing replicate search outcomes and tree diversity, not merely
  the single best run. Its reported benchmark values refer to its own alignments
  and conventions. No scores from it are transferred to our rows.
- [Large-scale alignment/phylogeny benchmark survey](https://pmc.ncbi.nlm.nih.gov/articles/PMC2989560/):
  documents empirical and simulated challenges; useful expansion route after
  per-dataset license, nucleotide policy and computational size checks. Aligning
  sequences is outside this pilot's fixed-alignment objective.

The initial collection excludes humans, clinical samples, pathogen surveillance,
private data and locality metadata. Only tutorial sequences and public non-human animal/plant
sequence fixtures are included. This is computational work with existing data.

## Supported research directions and settled scope

NNI with random starts is the baseline. SPR/TBR, plateau traversal and the
[Nixon parsimony ratchet (1999)](https://doi.org/10.1111/j.1096-0031.1999.tb00277.x)
are grounded follow-ups. If a ratchet temporarily reweights sites, every submitted
tree must be rescored under the original unit weights. XMP motivates stronger
exact bounds and incremental scoring; an optimized scorer must be differentially
checked against the deliberately simple verifier.

Changing columns, dropping taxa, collapsing duplicate sequences, scoring only
informative sites without restoring the constant offset, treating gaps as a fifth
state, or constraining a biological root changes the problem. Such changes cannot
improve an existing frontier row. A source MLE tree is a comparator, not an MP
record or proof of truth. Filtering is an engineering choice that may alter
biological signal. The pilot does not infer direction of evolution or ancestral
root location and does not supply bootstrap confidence.

Research audit date: 2026-10-20. The cited literature establishes methods and
specific tutorial scores; it is not an exhaustive survey proving no better
heuristic exists in 2026.

## Expansion audit and biological depth

The expansion adds the BSD-licensed [DendroPy cetacean fixture](https://github.com/jeetsukumaran/DendroPy/blob/b7fc4fd9c70c86a44e10650b3fb9b3be86e9dc77/tests/unittests/data/chars/cetaceans.nex)
and the per-file CC0 [Ferula repository](https://doi.org/10.18150/UZC2YR).
Source snapshots, accession-independent hashes, exact column maps, license evidence
and source-study DOIs are retained. See THIRD_PARTY.md for the adapted cetacean
matrix caveat and Ferula release identity. No published MP record is claimed for
these new derived matrices. Local neighbor joining follows the topology construction
of [Saitou & Nei (1987)](https://doi.org/10.1093/oxfordjournals.molbev.a040454), using
uncorrected Hamming distances, exact rational arithmetic and deterministic ties.

Ferula provides nuclear ETS/ITS and plastid markers on the same selected taxa.
Its [source study](https://doi.org/10.1093/botlinnean/boaf050) specifically examines
conflicting phylogenetic signals. `scripts/progress.py` compares current tree splits
and cross-scores both trees separately on each alignment; `scripts/interpret.py`
identifies changed site costs and original column coordinates. Disagreement is a
research observation, not evidence by itself of introgression, hybridization,
incomplete lineage sorting, or which history is true. Tied optima and filtering
sensitivity should be examined before interpreting mechanisms.

The 17 rows cover three empirical studies and two tutorial controls, not 17
independent biological replicates. Small/large subsets within a study share data;
held-out studies matter when claiming algorithm generality. DendroPy avian
ovomucoid and caenophidia MOS fixtures were inspected but rejected as proteins;
the angiosperm fixture is morphological. The Actinopterygii fixture was not
admitted because it included a human outgroup and would need a separate audited
selection. No clinical, private or sensitive genomic data enter the collection.

Next scientific comparisons should include a vetted established parsimony program
on the identical frozen inputs, stronger search neighborhoods, and independent
verification. The shipped heuristic probes cannot establish superiority over
mature software or novelty relative to the literature.
