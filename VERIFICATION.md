# Local verification record

Initialization date: 2026-10-20. Python 3.14.6 on macOS arm64. No external scoring
software or downloaded project code was executed. The scorer, validator, search
and tests were implemented locally. Imported source data were parsed as data only.

The Discovery@Home helper outside this repository was downloaded from the exact
start-playbook URL and matched SHA-256
`d0e9ce87016c42aea0082fa171e29992d9c84a70ca1de0f0713e660fd57e1ea4`.
Its `screen` reported no findings. Its `validate` reported conformant, five cases,
two open, and recognized the weighted catalog, priority log and reproduction
command. The intentionally absent coordination channel, review ledger and package
location were reported as optional conventions, not validation errors.
The helper ran under a local macOS sandbox blocking network and access to other
user folders, with writes confined to this task workspace. Later reproduction and
card checks used that sandbox too. Initial tests of newly written code ran directly
in the task environment. No global packages or settings were changed.

The reproduction suite checks hashes and reconstructs the derived datasets,
rescoring all candidate trees by the reference DP. Its 13 test methods include
all 256 quartet site patterns checked against brute ancestral-state assignments
on all three quartet trees, exhaustive Fitch/DP agreement on both PHYLIP examples,
random multistate differential tests, tree counts, root invariance, graph/Newick
rejection, strict alphabet validation, NNI neighborhoods/connectivity and a CLI
negative control. The empirical six-taxon bound is separately enumerated using
reference DP across all 105 trees during `scripts/check.py`.

`python3 scripts/replay_search.py` checks all 20 stored searches, including scores,
Newick topologies, histories and evaluation counts. Wall times are excluded from
identity. The Python version is recorded; reproducibility on other interpreter
versions should be checked, not assumed from the seed alone.

`python3 scripts/check_cards.py` executes each of the five catalog positive controls
and checks expected outcomes. Its logs are disposable under `.scratch/card-checks`.
The completion handoff records the tested code commit and fresh-clone outcome.
All evidence is author-checked; no human maintainer or independent reviewer has
endorsed it. No global-optimality claim is made for 12 or 24 taxa.
