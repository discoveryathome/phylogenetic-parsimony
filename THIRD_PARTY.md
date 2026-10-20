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
