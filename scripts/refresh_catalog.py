"""Maintainer initialization: derive current, runnable challenge controls from rows."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]

def main():
    rows=json.loads((ROOT/'discover/frontier-rows.json').read_text())
    tracks=[]
    def card(ident,question,command,expected,gate,experiment,points):
        return dict(id=ident,question=question,starting_points=points,
            methods=[experiment],acceptance_gate=gate,
            first_step=dict(command=command,expected=expected),
            bottleneck_link='DISCOVERY.md#bottleneck-and-research-tracks',
            first_experiment=experiment,claim_kind=['exact'],
            scope_change_triggers=['Changed taxa, columns, costs or symbol semantics require a new fixed row/profile.'])
    tasks=[]
    for r in rows:
        if r['status']!='open':continue
        tasks.append(card('improve-'+r['dataset'],f"Can a tree beat {r['score']} on {r['dataset']}?",
            ['python3','phylo.py','verify',r['dataset'],r['tree'],'--claim',str(r['score'])],
            f"valid=true; score={r['score']}",
            f"Identical hash/profile; independent reference score below {r['score']}; keep seed, budget and witness.",
            'Start from the incumbent; try plateau traversal or SPR with a declared budget.',
            ['discover/frontier-rows.json','MODEL.md','results/expansion-benchmark.json']))
    tracks.append(dict(id='improved-trees',weight=30,useful_outcome='Smaller independently verified scores on open fixed rows',tasks=tasks))
    r16=next(r for r in rows if r['dataset']=='pythonidae-16s-12')
    tracks.append(dict(id='better-heuristics',weight=25,useful_outcome='Better all-seed quality or success rate at equal evaluation caps',tasks=[
        card('paired-heuristics','Can an algorithm improve the declared 20-seed panels?',
             ['python3','scripts/progress.py'],'Complete panels; all wins, ties and losses shown',
             'Predeclare at least 20 paired seeds and budgets; independent scoring; retain failures. Use held-out seeds/studies before generalizing.',
             'Add plateau handling or SPR, compare against both shipped methods, then evaluate held-out seeds.',
             ['results/expansion-benchmark.json','src/phylo/advanced.py','RESULTS.md']),
        card('mature-baselines',"What do mature parsimony programs (TNT, PAUP*, MPBoot) score on each identical fixed row?",
             ['python3','phylo.py','verify',r16['dataset'],r16['tree'],'--claim',str(r16['score'])],
             f"valid=true; score={r16['score']}",
             'Every reported score is phylo.py verify on the exported Newick, on the identical alignment hash and profile; program, version, settings, budget and runtime recorded. A lower score is a frontier proposal for review, not an acceptance.',
             'Run a mature program on every open row with stated settings, export its best tree, verify it, and record the scores as row baselines.',
             ['discover/frontier-rows.json','data/manifest.json','MODEL.md','LITERATURE.md'])]))
    r=next(r for r in rows if r['dataset']=='pythonidae-cytb-12')
    tracks.append(dict(id='stronger-bounds',weight=20,useful_outcome='Higher independently checked lower bounds, or a closed optimum gap',tasks=[
        card('bound-pairs',f"Can a certificate raise the lower bound above {r['lower_bound']} on pythonidae-cytb-12?",
             ['python3','phylo.py','verify-bound',r['dataset'],r['bound_evidence']],
             f"valid=true; bound={r['lower_bound']}",
             'Same hash/profile; stronger certificate accepted by the checker. New bound types need a proof and independent tests before acceptance.',
             'Improve disjoint incompatible-site pairing using maximum matching; retain an explicit pair witness.',
             ['src/phylo/bounds.py','MODEL.md',r['bound_evidence']])]))
    tracks.append(dict(id='verifier-audits',weight=15,useful_outcome='Minimized counterexamples and independent assurance',tasks=[
        card('audit-verifier','Can invalid topology, score or bound evidence pass?',
             ['python3','-m','unittest','discover','-s','tests','-v'],'All tests pass',
             'Minimized reproducer and a regression test; preserve scoring semantics.',
             'Audit malformed Newick and bound certificates; compare independent ancestral-state enumeration.',
             ['tests/test_phylo.py','tests/test_expansion.py','MODEL.md'])]))
    tracks.append(dict(id='biological-interpretation',weight=10,useful_outcome='Mapped site changes and careful cross-marker interpretation',tasks=[
        card('interpret-ferula','Where do the same-taxon nuclear and plastid solutions disagree?',
             ['python3','scripts/progress.py'],'Three same-taxon comparisons with separately scored alignments',
             'Use frozen columns and same taxa; cite the source; no species-history, support or causal claim from score or RF alone.',
             'Map differences to ETS/ITS and plastid partitions; characterize tied alternatives and filtering effects.',
             ['results/progress.json','data/ferula-nrdna-12-selection.json','sources/ferula-plastid.partition','LITERATURE.md'])]))
    catalog=dict(schema='discover-catalog/v0',priority_revision=3,assessed_on='2026-10-21',
        priority_log='discover/priority-log.md',status='Public pilot; donor intake open from 2026-10-21 (review capacity: surge). Evidence remains author-checked pending independent verification.',tracks=tracks)
    (ROOT/'discover/catalog.json').write_text(json.dumps(catalog,indent=2)+'\n')
if __name__=='__main__':main()
