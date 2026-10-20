"""Local weighted task draw; seed is emitted so the selection can be replayed."""
import argparse,json,secrets
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--seed');a=p.parse_args()
seed=a.seed or secrets.token_hex(16)
if len(seed)!=32 or any(c not in '0123456789abcdefABCDEF' for c in seed):p.error('seed must be 32 hexadecimal digits')
root=Path(__file__).resolve().parents[1]
c=json.loads((root/'discover/catalog.json').read_text())
x=int(seed[:8],16)%100
for track in c['tracks']:
    if x<track['weight']:break
    x-=track['weight']
group=None
tasks=track['tasks']
if track['id']=='improved-trees':
    cases={r['id']:r for r in json.loads((root/'data/manifest.json').read_text())['datasets']}
    grouped={}
    for task in tasks:
        family=cases[task['id'].removeprefix('improve-')]['source_group']
        grouped.setdefault(family,[]).append(task)
    group=sorted(grouped)[int(seed[8:16],16)%len(grouped)]
    tasks=grouped[group]
card=tasks[int(seed[16:24],16)%len(tasks)]
print(json.dumps(dict(seed=seed,priority_revision=c['priority_revision'],track=track['id'],study_group=group,task=card['id'],first_step=card['first_step'],status='local suggestion only; review paused'),indent=2))
