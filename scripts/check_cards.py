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
            expected=int(argv[argv.index('--claim')+1])
            if not parsed['valid'] or parsed['score']!=expected:raise SystemExit('Wrong positive control score')
        elif card['id']=='bound-pairs':
            parsed=json.loads(result.stdout)
            cert=json.loads((ROOT/argv[-1]).read_text())
            if not parsed['valid'] or parsed['bound']!=cert['bound']:raise SystemExit('Wrong bound control')
        elif card['id'] in ('paired-heuristics','interpret-ferula'):
            report=json.loads(result.stdout)
            if len(report['paired_panels'])!=4 or len(report['ferula_comparison'])!=3:raise SystemExit('Incomplete progress controls')
        print('PASS',card['id'],flush=True)
print('PASS: every catalog first_step and expected positive control')
