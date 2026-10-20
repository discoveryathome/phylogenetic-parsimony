# Source permissions and attribution

Original pilot code and prose: MIT, see LICENSE. Imported materials retain their
own terms. No software implementation from these projects is used by the scorer.

- `sources/dnapars.html`, `sources/dnapenny.html`, their FASTA transcriptions and
  transcribed baseline topologies: Joseph Felsenstein / University of Washington,
  PHYLIP 3.69 documentation, copyright 1986–2008. The HTML contains the express
  permission to copy the document provided no fee is charged and the copyright
  notice is retained. We retain the complete original notices and charge no fee.
  The PHYLIP web repository also provides BSD-2-Clause (`sources/PHYLIP-LICENSE`).
  Do not strip the embedded notices or represent the documentation as MIT-only.
- `sources/pythonidae.fasta`, `sources/pythonidae.nex`,
  `sources/pythonidae-mle.nwk`, derived Pythonidae alignments and pruned baseline
  trees: DendroPy, BSD-3-Clause, full terms in `sources/DENDROPY-LICENSE.rst`.
  Copyright Jeet Sukumaran, Mark T. Holder and Matthew Andres Moreno. Pinned commit
  `b7fc4fd9c70c86a44e10650b3fb9b3be86e9dc77`. The NEXUS header credits Rawlings,
  Rabosky, Donnellan & Hutchinson (2008), *Python phylogenetics: inference from
  morphology and mitochondrial DNA*, Biological Journal of the Linnean Society
  93:603–619, DOI 10.1111/j.1095-8312.2007.00904.x. Cite both the original study
  and DendroPy when using these derived fixtures. Admission relies on the explicit
  repository license covering its distributed test files; it does not license
  arbitrary other data from the study.
- Discovery@Home protocol and schemas in `sources/`: MIT, full notice retained in
  `sources/DISCOVER-LICENSE`. Source URLs and hashes are in `sources/index.json`.

All sources were retrieved 2026-10-20. `data/manifest.json` binds each alignment to
its source and hash. Selection JSON files identify all original columns and labels.
No claims of endorsement by source authors are made.

## Expansion sources

- `sources/cetaceans.nex` and derivatives: same pinned DendroPy BSD-3-Clause
  distribution and retained license. Its header attributes the adapted fixture to
  Milinkovitch, Meyer & Powell (1994), *Phylogeny of all major groups of cetaceans
  based on DNA sequences from three mitochondrial genes*,
  [DOI 10.1093/oxfordjournals.molbev.a040164](https://doi.org/10.1093/oxfordjournals.molbev.a040164).
  The distributed 1,365-character fixture is not asserted to be the paper's exact
  1,352-base analysis matrix. Our comparator is a deterministic Hamming-distance
  neighbor-joining tree, not a published parsimony tree.
- `sources/ferula-*`: Piwczyński et al., *Conflicting phylogenetic signals obscure
  taxonomic position of Ferula heuffelii*, [RePoD dataset
  10.18150/UZC2YR](https://doi.org/10.18150/UZC2YR), version 1.0, released
  2025-06-26. Every downloaded file is unrestricted and explicitly CC0-1.0 in
  `sources/ferula-metadata.json`. Download MD5s were checked against metadata;
  SHA-256s are in the source index. Included: nuclear ETS/ITS and plastid matrices,
  ML trees, partitions and README. Cite the original study,
  [DOI 10.1093/botlinnean/boaf050](https://doi.org/10.1093/botlinnean/boaf050),
  alongside the dataset. Each source matrix has 46 terminals. Curated subsets
  and pruned comparators are newly derived instances.
