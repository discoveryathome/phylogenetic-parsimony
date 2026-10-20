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
card=track['tasks'][int(seed[8:16],16)%len(track['tasks'])]
print(json.dumps(dict(seed=seed,priority_revision=c['priority_revision'],track=track['id'],task=card['id'],first_step=card['first_step'],status='local suggestion only; review paused'),indent=2))
