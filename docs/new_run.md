> **과거 실험 안내:** 현재 공개 실행 벤치마크는 [실행 안내](real_traces.md)를 참고하세요. 이 문서는 이전 자료와 코드의 재현을 위해 보존합니다.

# 새 모델 예측 실행 안내

이 문서는 **동결된 합성 입력에 새 예측을 생성하는 절차**입니다. 저장된 결과를 다시 채점하는 `scripts/replay.py`와 다릅니다. 모델을 호출하는 API 클라이언트는 포함하지 않으므로, 실행자는 모델 API 또는 독립 문맥을 제공하는 Agent 환경을 준비해야 합니다. 기존 코드·프롬프트·데이터를 그대로 사용하며 새 기능이나 새 평가셋을 만들지 않습니다.

## 1. 저장소 루트에서 새 작업 폴더 준비

Python 3.10 이상과 표준 라이브러리를 사용합니다. `action/`은 코드를 열람하는 위치이며 바로 실행하기 위한 데이터·설정이 없습니다. 아래 블록은 저장소 루트에서 실행합니다. **archive의 평가 전 freeze에 포함된 파일만** 추출하므로 과거 예측·모델 응답·test 의미 검수 ratings가 새 폴더에 들어가지 않습니다.

```bash
python3 - <<'PY'
import hashlib, json, zipfile
from pathlib import Path

repo = Path.cwd()
archive = repo / 'data/expanded_frozen.zip'
expected = json.loads((repo / 'data/archive_manifest.json').read_text())['sha256']
assert hashlib.sha256(archive.read_bytes()).hexdigest() == expected, 'Archive hash mismatch'
out = (repo / 'runs/new-inference').resolve()
if out.exists():
    raise SystemExit('Refusing to overwrite: ' + str(out))
with zipfile.ZipFile(archive) as z:
    freeze = json.loads(z.read('freeze_manifest.json'))
    payload = {}
    for name, digest in freeze['sha256'].items():
        dest = (out / name).resolve()
        assert dest.is_relative_to(out), 'Unsafe archive path'
        data = z.read(name)
        assert hashlib.sha256(data).hexdigest() == digest, name
        payload[name] = data
    payload['freeze_manifest.json'] = z.read('freeze_manifest.json')
    out.mkdir(parents=True)
    for name, data in payload.items():
        dest = out / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
(out / 'incoming').mkdir()
(out / 'new_run.json').write_text(json.dumps({
    'source_archive_sha256': expected,
    'scope': 'New predictions on the existing frozen synthetic benchmark',
    'model_requested': None,
    'model_observed': None,
    'settings_requested': {},
    'settings_observed': {},
    'note': 'Fill only verified runner/provider information; do not inherit old observations.'
}, indent=2) + '\n')
assert not (out / 'raw').exists()
assert not (out / 'review/test_semantic_ratings.json').exists()
print(out)
PY
cd runs/new-inference
python3 harness.py verify
```

실행 폴더에는 다음 파일이 함께 있어야 합니다.

```text
runs/new-inference/
  harness.py, workflow.py, evaluate.py, export_tables.py
  run_config.json, freeze_manifest.json, test_schedule.json, dev_selection.json
  data/public_cases/               # 예측 입력 96개
  data/private_split_plan.json     # 평가자가 쓰는 분할·태그
  review/adjudicated_gold.json     # 평가자용 정답
  prompts/                        # common, direct, revise, extract, relate
  incoming/                       # 외부 모델의 수정하지 않은 응답을 저장할 곳
  new_run.json                    # 이번 실행의 모델·설정 관측 기록
```

`freeze_manifest.json`은 **기존 데이터·코드·프롬프트의 동결본**을 검증합니다. 새 실행의 모델 정보를 동결했다는 뜻은 아닙니다. `run_config.json`은 원래 준비 시점의 null 설정을 포함한 역사적 파일이며 모델을 선택하거나 호출하지 않습니다. 해당 파일을 변경하면 원래 freeze 검증이 실패합니다.

이번 실행에서 실제 사용할 모델·설정은 외부 실행기에서 선택하고, 요청값과 확인된 반환값을 `new_run.json`에 기록하세요. 원래 관측 alias `gpt-6-astra`·`medium`을 새 실행 관측으로 복사하지 않습니다. 확인하지 못한 snapshot·토큰·비용은 null로 남기고, 공급자가 제공하면 호출별 메타데이터를 별도 보존합니다. 입력·프롬프트·채점기를 변경할 연구는 이 동일 조건 재실행과 분리된 새 버전으로 관리해야 합니다.

## 2. 개발 사례 하나로 D1 실행

이후 명령의 작업 디렉터리는 **`runs/new-inference/`**입니다. `77e12e82`는 동결된 개발용 선정 사례입니다.

```bash
python3 harness.py prepare 77e12e82 direct --phase dev
```

`calls/dev_77e12e82_direct.txt`와 같은 이름의 요청 메타데이터 JSON이 만들어집니다. 출력된 지시대로 **그 txt 내용만** 외부 모델의 새 문맥에 전달하세요. 모델에 작업 폴더 전체, `review/`, `private_*`, 다른 사례·다른 방법의 출력을 제공하지 않습니다. 파일을 읽는 Agent 방식에서는 파일 전체가 실제로 전달되었는지도 확인합니다. API 방식에서는 txt 전체를 요청 본문에 넣습니다.

모델이 반환한 원문을 `incoming/dev_77e12e82_direct.txt`에 수정 없이 저장한 뒤 다음 명령을 실행합니다. 이 파일은 **실행자가 외부 모델 응답으로 만들어야 하며 harness가 자동 생성하지 않습니다.**

```bash
python3 harness.py save dev_77e12e82_direct \
  --response incoming/dev_77e12e82_direct.txt --status success
```

확인 가능한 실제 실행 ID가 있으면 `--task-id`를 추가합니다. 응답의 markdown fence를 제거하거나 JSON을 손으로 고쳐 저장하지 않습니다. 파싱 실패도 결과에 남깁니다. 저장 위치는 `responses/`의 원문, `raw/`의 원문·파싱 결과, `execution_log.jsonl`의 상태입니다.

## 3. D2와 P2 실행

아래 **prepare → 외부 모델 실행 → 원문 파일 저장 → save**를 각 단계마다 수행합니다. 단계 사이의 주석은 실제로 완료해야 하는 작업입니다.

```bash
# D2: 저장한 D1 응답을 같은 사례의 새 문맥에서 검토
python3 harness.py prepare 77e12e82 revise --phase dev
# calls/dev_77e12e82_revise.txt를 외부 모델에 전달하고
# 원문 응답을 incoming/dev_77e12e82_revise.txt에 저장
python3 harness.py save dev_77e12e82_revise \
  --response incoming/dev_77e12e82_revise.txt --status success

# P2 첫 단계: 요구사항·예외 추출
python3 harness.py prepare 77e12e82 extract --phase dev
# calls/dev_77e12e82_extract.txt → 외부 모델 실행 → incoming/..._extract.txt
python3 harness.py save dev_77e12e82_extract \
  --response incoming/dev_77e12e82_extract.txt --status success

# P2 둘째 단계: 앞서 저장한 extract 출력을 이용해 관계 판단
python3 harness.py prepare 77e12e82 relate --phase dev
# calls/dev_77e12e82_relate.txt → 외부 모델 실행 → incoming/..._relate.txt
python3 harness.py save dev_77e12e82_relate \
  --response incoming/dev_77e12e82_relate.txt --status success
```

`revise`는 자기 사례의 `direct`, `relate`는 자기 사례의 `extract` 원문을 harness가 자동으로 연결합니다. 이전 응답이 없으면 준비가 실패합니다. `relate` 저장 시 `raw/dev_77e12e82_aggregate.json`에 코드 합성 결과가 생성됩니다. D1·D2는 각각 `raw/..._direct.json`, `raw/..._revise.json`을 최종 출력으로 사용합니다.

각 단계는 독립 문맥입니다. D1 출력을 D2에 재사용하므로 고유 진단 세션은 네 개입니다. 모델 의미 판단과 코드 합성을 구분하며, 단계를 나눴다는 이유로 더 정확하다고 전제하지 않습니다.

## 4. 전체 평가와 새 의미 검수

- 개발 자료를 더 실행하려면 `dev_selection.json`의 여섯 ID만 사용합니다.
- 평가에는 `test_schedule.json`의 `record_ids`와 사례별 `stage_orders`를 따르고 `--phase test`를 사용합니다. 결과를 본 뒤 ID·정답·프롬프트를 선택적으로 수정하지 않습니다.
- 새 실행은 기존 archive와 다른 폴더에 저장하며 **과거 `raw/`나 `review/test_semantic_ratings.json`을 가져오지 않습니다.** 새 예측에 대한 의미 검수를 새로 해야 합니다.

72개 평가 사례의 예측을 수집한 뒤, 같은 작업 디렉터리에서:

```bash
python3 evaluate.py blind-pack
# 검수자가 review/test_packets의 공개 입력·정답·익명 예측을 검토하여
# review/test_semantic_ratings.json을 새로 작성
python3 evaluate.py score
python3 export_tables.py
python3 harness.py verify
```

채점기는 의미 관계를 자동으로 판단하지 않습니다. [ratings 형식](action_scoring.md#semantic-rating-format)에 맞춰 모든 후보를 검수해야 합니다. 검수자는 private method map을 보지 않으며 LLM 검수와 사람 검수를 구분합니다. 개발의 의미 점수까지 산출하려면 같은 명령에 `--phase dev`를 사용하고 개발용 ratings를 별도로 작성합니다 (`export_tables.py`는 평가용 출력 기준).

`test_results.json`에 전체·조건·family·대조쌍·bootstrap 결과, `tables/`에 내보낸 표가 생성됩니다. 일부 응답이 누락·잘못되면 해당 실패가 분모에 남습니다. **개발 사례 하나의 실행만으로 기존 72개 결과를 재현했다고 보고하지 않습니다.**

## 5. 기술 실패와 재개

실제 무응답인 경우 `--response`를 주지 않고 기록합니다. 아래는 `direct`에서 기술 실패가 발생했을 때만 실행하는 예입니다.

```bash
python3 harness.py save dev_77e12e82_direct --status technical_failure
python3 harness.py prepare 77e12e82 direct --phase dev --attempt 1
# 재시도 응답이 있다면 incoming/dev_77e12e82_direct_retry1.txt에 저장
python3 harness.py save dev_77e12e82_direct_retry1 \
  --response incoming/dev_77e12e82_direct_retry1.txt --status success
```

오답·JSON 오류·잘못된 근거 참조는 기술 실패가 아니므로 재시도하지 않습니다. 기존 출력 파일을 덮어쓰거나 성공한 호출을 다시 저장하지 않습니다. 중단 후에는 `calls/`, `responses/`, `execution_log.jsonl`을 확인해 아직 완료되지 않은 단계부터 진행합니다. 첫 단계에 쓸 수 있는 응답이 없으면 종속 단계는 생성하지 않습니다.

## 6. 실행 범위

이 안내의 폴더 준비·요청 생성·저장·합성은 보존 응답을 이용한 **명령 동작 점검**으로 검증했습니다. 새 모델 추론이나 새 성능 실험을 실행했다는 뜻이 아닙니다. 새 실행에는 외부 모델 접근과 새 의미 검수가 필요하며, 원래 immutable model snapshot의 재현은 보장되지 않습니다.
