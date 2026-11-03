from pathlib import Path
import json,hashlib
OUT=Path(__file__).resolve().parent
SRC=OUT.parent
ids=json.loads((SRC/'case_ids.json').read_text());assert len(ids)==15 and len(set(ids))==15
cases=[json.loads((SRC/'public'/f'{i}.json').read_text()) for i in ids]
for c in cases:
 assert set(c)=={'case_id','source','dataset','task_scope','input','focal_relation'}
 assert c['case_id'] in ids
payload={'packet':'eta-real-trace-human-15-v2','cases':cases,'public_input_hashes':{i:hashlib.sha256((SRC/'public'/f'{i}.json').read_bytes()).hexdigest() for i in ids}}
(OUT/'cases.js').write_text('const PACKET_DATA = '+json.dumps(payload,ensure_ascii=False)+';\n')
s=(OUT/'index.html').read_text()
for name in ['cases.js','core.js','app.js']:
 s=s.replace(f'<script src="{name}"></script>','<script>'+ (OUT/name).read_text().replace('</script','<\\/script')+'</script>')
(OUT/'review.html').write_text(s)
roundtrip=json.loads((OUT/'cases.js').read_text().split(' = ',1)[1].rstrip(';\n'))
assert roundtrip['cases']==cases
(OUT/'build_check.json').write_text(json.dumps({'case_count':len(cases),'public_only':True,'exact_public_objects_preserved':True,'source_files':payload['public_input_hashes'],'hidden_answer_keys_injected':False},ensure_ascii=False,indent=2))
print('15 public objects preserved exactly, standalone page built')
