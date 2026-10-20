"""Execute every catalog positive control, with logs kept under .scratch/."""
import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'.scratch/card-checks';out.mkdir(parents=True,exist_ok=True)
c=json.loads((ROOT/'discover/catalog.json').read_text())
for track in c['tracks']:
    for card in track['tasks']:
        argv=card['first_step']['command'][:]
        if argv[0]=='python3':argv[0]=sys.executable
        result=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True)
        (out/(card['id']+'.log')).write_text(result.stdout+result.stderr)
        if result.returncode:raise SystemExit('FAIL '+card['id'])
        if card['id'].startswith('improve-'):
            parsed=json.loads(result.stdout)
            expected=579 if card['id']=='improve-12' else 990
            if not parsed['valid'] or parsed['score']!=expected:raise SystemExit('Wrong positive control score')
        elif card['id']=='escape-plateaus':
            if json.loads(result.stdout)['score']!=9:raise SystemExit('Failure case changed')
        elif card['id']=='interpret-12':
            report=json.loads(result.stdout)
            if (report['baseline_score'],report['best_score'])!=(591,579):raise SystemExit('Interpretation control changed')
        print('PASS',card['id'],flush=True)
print('PASS: every catalog first_step and expected positive control')
