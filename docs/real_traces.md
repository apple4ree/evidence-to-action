# 실제 공개 실행 기록: 입력 복원, 재채점, 새 추론

이번 묶음은 기존 합성 72건과 분리된 **15개 국소 행동, 14개 원본 실행**이다. MAST 6개, Who&When 4개, AgentHallu 5개를 사용한다. 같은 원본의 두 행동은 통계 집계에서 같은 그룹으로 묶는다. 원문에서 평가할 행동과 그 이전 기록을 추출했고, 가상 정책이나 이벤트를 추가하지 않았다.

## 1. 기록과 데이터 위치

| 위치 | 내용 |
|---|---|
| `real_traces/input_recipes.json` | 원본 URL, 고정 revision, SHA-256/Git blob hash, 줄번호 또는 JSON pointer, 입력 재구축 규칙 |
| `real_traces/public/` | 복원 후 생성되는 모델 공통 입력. upstream 정답과 후속 기록 제외 |
| `real_traces/gold/`, `gold_adjudication.json` | 비교 전에 고정한 LLM 주석과 별도 문맥 LLM 검수, 판정 범위 조정 기록 |
| `real_traces/prompts/`, `config.json`, `freeze_manifest.json` | 단계별 프롬프트, 실행 순서, 평가 전 파일 hash |
| `real_traces/responses/`, `predictions/`, `validation/` | 모델의 원시 최종 응답, 파싱/합성 결과, 출력 참조 검사 |
| `real_traces/runtime/` | 실제 관측한 모델 alias, reasoning effort, 토큰, 세션 시간, 입력 전달 확인 결과 |
| `real_traces/semantic_ratings.json`, `results/` | 방법 이름을 가린 의미 채점과 집계 결과. 의미 채점 파일은 재추론이 아니라 저장된 채점 자료 |

원본 저장소의 파일은 통째로 재게시하지 않고, 고정 URL에서 가져와 동일한 입력으로 복원한다. 원본별 이용 조건은 해당 upstream 저장소를 따른다. 표준 Python 3 외의 패키지는 필요 없다.

## 2. 저장 결과 재채점

저장소 루트에서 실행한다.

```sh
python3 real_traces/restore_inputs.py
python3 real_traces/harness.py verify
python3 real_traces/test_harness.py
python3 real_traces/evaluate.py
```

첫 명령은 14개 고정 원본을 다운로드하고 hash를 검증한 뒤, 15개 입력과 저장된 비교의 60개 요청을 byte-for-byte 복원한다. 캐시는 `real_traces/source_cache/`에 보관한다. 재접속 없이 확인하려면 `python3 real_traces/restore_inputs.py --offline`을 실행한다. 원본이 삭제되거나 변경되면 오류를 내며, 다른 revision으로 자동 대체하지 않는다.

`evaluate.py`는 저장 예측과 저장된 의미 채점을 읽고 `results/summary.json`, `per_case.json`, `per_case.csv`를 다시 계산한다. 의미 채점이 없으면 해당 항목은 미채점으로 남는다. 모델을 새로 호출하는 명령은 아니다.

## 3. 새 모델 추론

기존 결과를 덮어쓰지 않도록 별도 작업 폴더를 만든다.

```sh
python3 real_traces/create_run.py runs/real_trace_new
python3 runs/real_trace_new/harness.py prepare AHN01 direct
python3 runs/real_trace_new/harness.py prepare AHN01 extract
```

각 `requests/*.txt`의 전체 내용을 모델에 입력하고, 응답 원문을 `runs/real_trace_new/responses/AHN01_direct.json`과 `AHN01_extract.json`에 저장한다. **정답 폴더나 원본 URL은 모델에 전달하지 않는다.** 모든 방법에 같은 공개 입력을 제공한다.

```sh
python3 runs/real_trace_new/harness.py collect AHN01_direct
python3 runs/real_trace_new/harness.py collect AHN01_extract
python3 runs/real_trace_new/harness.py prepare AHN01 revise
python3 runs/real_trace_new/harness.py prepare AHN01 relate
```

뒤의 두 요청을 모델에 전달해 응답을 각각 `responses/AHN01_revise.json`, `AHN01_relate.json`으로 저장하고 `collect AHN01_revise`, `collect AHN01_relate`를 실행한다. `case_ids.json`의 나머지 사례도 같은 방식으로 수행한다.

- 직접 진단(D1): `direct` 1개 세션.
- 재검토(D2): 동일한 `direct` 응답을 재사용하고 `revise`를 실행.
- 단계 분해(P2): `extract`로 요구사항을 추출하고 `relate`에서 관계를 판단. 코드가 최종 판정을 합성.

현재 저장소는 파일 기반 요청 준비, 출력 검사, 합성, 채점을 제공한다. API provider 호출 adapter는 포함하지 않는다. 실행 당시에는 fresh Codex native child 세션을 사용했다. 새 호출은 사용자의 실행 환경에서 수행하고 모델 ID, 설정, 원시 응답, 오류와 측정 가능한 비용을 별도로 기록해야 한다. 잘못된 답이나 JSON 오류를 맞을 때까지 재시도하지 않는다.

새 예측에는 기존 의미 채점 파일을 복사하지 않는다. 고정된 `scoring_spec.md`에 따라 방법 이름을 가린 새 출력을 검토한 다음 의미 채점을 작성한다. 사람 검수와 LLM 검수는 구분한다.

## 4. 실행 환경과 재현 범위

실행 기록에서 확인한 설정은 모델 alias `gpt-6-astra`, reasoning effort `medium`이다. immutable 모델 snapshot과 과금액은 확인되지 않았다. 토큰은 native 세션의 시스템 문맥과 도구 왕복을 포함한다. 시간은 실제 native task duration이며 준비부터 파일 수집까지의 시간과 구분한다. D2와 P2의 세션 수가 같아도 계산 비용이 같다는 뜻은 아니다.

각 원본의 전체 actor payload가 공개된 것은 아니다. 이번 과제는 제공된 공개 기록 안의 지정한 행동/주장 관계를 평가한다. 입력 파일의 전체 텍스트 전달 여부와 의미적 주의/이해 여부도 다르다. 공개 runtime은 개인정보성 로컬 경로와 세션 식별자를 뺀 계측 부분집합이며, 원래 감사 기록은 연구 작업공간에 보존했다.

단일 사람 검토 15건을 수집했으며 고정 라벨과 12/15건 일치했다. 세 불일치는 미조정 상태다. 고정 정답과 의미 채점은 유지하며, 복수 사람 간 재현성은 후속 검증이다. [검토 원본과 분석](../real_traces/human_review/README.md). 원본 수집의 선택 과정과 기존 합성 자료의 결과는 별개다.

## 5. 사람 주석 참여

```sh
python3 real_traces/review/build_page.py
```

앞의 입력 복원을 마친 후 생성된 `real_traces/review/review.html`을 브라우저에서 연다. 서버 설치나 로그인은 필요 없다. 기존 실제 실행 15건 페이지와 답변 JSON 형식을 유지한다.

1. 사례의 **평가할 관계(focal relation)**, 대상 행동과 요청을 읽는다.
2. 행동 이전 기록에서 적용 조건과 관련 관측을 찾고 줄번호나 `history[index]`를 적는다.
3. **Supported**(근거 충족), **Unsupported**(명시적 위반 또는 완전한 기록에서 필수 확인 부재), **Indeterminate**(정책/기록 부족으로 판정 불가) 중 하나를 고른다. 판단 작업 자체가 어려우면 별도의 **검토 보류**를 고른다.
4. 요구사항과 원문 출처, 문제 필드, 근거 위치, 판단 이유를 적고 ‘검토 완료, 다음’을 누른다. 사례나 기존 정답을 본 적이 있으면 체크한다.
5. 완료 후 ‘답변 파일 내보내기’로 JSON을 저장해 전달한다. 수정 시 최초 제출과 수정 이력이 함께 보존된다.

실패한 실행 안의 정상 조회나 확인 질문은 그 자체로 오류가 아니다. 공개 전체 로그를 모든 Agent가 보았다고 가정하지 않는다. 정답과 모델 예측은 페이지에 포함하지 않는다. 한 사람이 검토한 결과는 단일 사람 확인으로 기록하고, 사람 간 일치도 측정과 구분한다.

자동 저장은 브라우저와 파일 위치에 따라 달라질 수 있다. 기존 페이지의 작업을 이어갈 때는 먼저 답변 파일을 내보낸 뒤 새 페이지에서 ‘이전 답변 불러오기’를 사용한다. 답변은 외부 서버로 전송되지 않는다.

## 5. 수행한 재현 점검

고정 원본의 로컬 캐시로 입력 15개와 요청 60개를 정확히 복원하고 freeze 검사를 통과했다. 경계/복원 테스트 5개, 주석 UI의 저장, 최초 제출 보존, 가져오기 검증도 수행했다. 별도 새 폴더에서 direct/extract 요청 생성을 확인했다.

이 작업 환경의 Python 외부 접속은 DNS 제한으로 실패해 온라인 다운로드 경로 전체는 재실행하지 못했다. 원본은 연결된 GitHub 도구로 수집했으며 URL, revision과 바이트 hash를 보존했다. 네트워크가 없는 환경에서는 고정 원본을 hash 이름의 캐시에 준비하고 `--cache 경로 --offline`을 사용한다. 브라우저의 실제 클릭, 내보내기 점검은 미완료다.
