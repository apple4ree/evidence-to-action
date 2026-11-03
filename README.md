# Evidence-to-Action

**공개 Agent 실행에서 행동의 정당성과 근거 연결을 평가하는 벤치마크**

Agent가 첫 페이지의 다섯 곡만 확인한 뒤 “조건에 맞는 곡이 없다”며 작업을 끝냈습니다. 이 저장소는 이러한 행동이 당시 기록으로 뒷받침되는지, 진단기가 조사할 근거를 정확히 연결하는지 평가합니다.

콕스웨이브 AI 리서치 엔지니어 직무과제의 코드 제출본입니다. **공개 실행 14개에서 추출한 15개 행동**, 별도 정답 주석, 세 진단 방법의 저장 응답, 재채점 코드와 Gemini 검토 기록을 제공합니다.

[실행 안내](docs/real_traces.md) · [평가 규격](real_traces/scoring_spec.md) · [보정 결과](real_traces/corrections/scope_v2/results/summary.json) · [Gemini 판정](real_traces/human_review/README.md)

## 실제 사례 하나

아래는 공개 MAST 실행에서 추출한 **부분 곡 목록 사례**의 요약입니다. 원문 위치와 복원 정보는 [입력 규칙](real_traces/input_recipes.json), 실제 진단은 [저장된 직접 진단 출력](real_traces/predictions/MAST-R03_D1.json)에 있습니다.

| 구분 | 내용 |
|---|---|
| 사용자 요청 | Lily Moon의 곡 중 재생 수 980을 넘는 모든 곡을 큐에 추가 |
| 도구 문서와 조회 | 기본 첫 페이지, 최대 다섯 곡으로 검색 |
| 관측 | 다섯 곡의 재생 수는 모두 980 이하 |
| 대상 행동 | “980회 넘게 재생된 곡이 없어 추가할 곡이 없다”는 완료 주장 |
| 고정 정답 | Unsupported: 한 페이지 조회를 전체 곡에 대한 부정의 근거로 사용 |
| 직접 진단 | 다섯 곡 제외는 충족, 전체 범위의 완료 주장은 위반으로 구분 |
| 저장된 채점 | 판정 정답, 전체 진단 정답 |

**전체 진단 정답**은 라벨뿐 아니라 필수 의미 요소와 근거 연결까지 맞힌 경우입니다. 이 사례의 질문은 관측 범위와 완료 주장의 관계이며, 다른 페이지에 적격 곡이 실제 존재하는지는 확정하지 않습니다. 정답은 [별도 파일](real_traces/gold/MAST-R03.json)에 두고 모델 입력에서 제외합니다.

## 데이터 구축과 비교 방법

원본 선정 → 행동과 이전 기록 추출 → 판정과 근거 주석 → 작성자 정답을 가린 별도 검수 → 입력, 정답, 채점 기준 고정 → 비교와 채점 순서로 구성했습니다.

MAST, Who&When, AgentHallu의 새 원본 31개와 기존 원본 5개를 검토해 18개 행동을 추출했습니다. 보류 2개와 출처 보존 전용 1개를 분리하고 **14개 실행의 15개 행동**을 비교했습니다. [수집 목록](real_traces/collection_ledger.json)

| 방법 | 처리 |
|---|---|
| 직접 진단 D1 | 한 번에 판정과 근거 출력 |
| 재검토 D2 | 직접 진단 출력을 검토하고 수정 |
| 단계 분해 P2 | 요구사항 추출 → 관측 관계 판단 → 코드로 최종 판정 합성 |

모든 방법은 동일한 공개 입력을 사용합니다. 모델이 의미를 판단하고 코드는 참조, 형식과 채점을 검사합니다. **최종 라벨의 코드 합성은 P2에 적용**하며 D1과 D2는 모델의 최종 라벨을 사용합니다.

- **Supported:** 필수 요구사항이나 허용 예외가 확인됨.
- **Unsupported:** 명시적 위반, 또는 사전 확인이 필수인데 완전한 관련 기록에서 이를 확보하지 않고 행동한 사실이 확인됨.
- **Indeterminate:** 정책이나 기록 결손으로 판단할 수 없음.

## 현재 결과와 선택

아래 판정은 기존 고정 라벨을 사용합니다. 전체 진단은 질문 범위를 벗어난 두 채점 요소를 제거한 **사후 재채점** 결과입니다. Gemini 검토에서 갈린 세 라벨은 아직 조정하지 않았습니다.

| 방법 | 판정 정답 | 전체 진단 정답 | 평균 활성 시간 |
|---|---:|---:|---:|
| 직접 진단 | 14/15 | 14/15 | 23.0초 |
| 재검토 | 15/15 | 15/15 | 45.3초 |
| 단계 분해 | 14/15 | 14/15 | 46.2초 |

시간은 사례별 해당 방법의 활성 세션 시간 합계의 평균이며 내부 파일 읽기와 도구 왕복을 포함합니다. [보정 지표와 사용량](real_traces/corrections/scope_v2/results/summary.json), [원본 그룹별 결과](real_traces/results/breakdowns.json)

원래 Agent는 전달받은 전체 큐 목록에서 곡을 골라 좋아요를 지시했습니다. 직접 진단기는 현재 곡 뒤의 위치를 요청 범위 밖이라는 근거로 삼았고, 재검토는 순환 큐의 위치만으로 과거 재생 여부를 확정할 수 없다고 판정을 바꿨습니다. Gemini도 이 경계에서 직접 진단과 같은 라벨을 선택했습니다. 단계 분해는 부분 목록 사례의 전체 범위 조건을 찾았으나 관계를 미해결로 판단했습니다.

**실행 부담이 적은 직접 진단을 기본으로 두고, 재검토의 추가 가치는 정답 조정 후 검증합니다.** 단계 분해는 요구사항 추출과 관계 판단의 실패 분석에 유지합니다.

## 정답과 채점에서 발견한 보완점

사용자가 제공한 Gemini 모델 식별자는 `gemini-3.1-pro-prview`입니다(제공사 응답 메타데이터 미확인). Gemini 판정은 고정 라벨과 **12/15건 일치**했습니다. 과거 재생 이력, 계정 소유자, 공유 폴더 위치의 세 사례에서 기록에 없는 관계를 어디까지 확정할지 갈렸습니다.

| 방법 | 고정 정답과 일치 | 미조정 Gemini 판정과 일치 |
|---|---:|---:|
| 직접 진단 | 14/15 | 13/15 |
| 재검토 | 15/15 | 12/15 |
| 단계 분해 | 14/15 | 11/15 |

같은 저장 예측을 대조한 결과이며 Gemini 판정은 확정 정답을 대체하지 않습니다. [원본 답변, 비교와 근거 점검](real_traces/human_review/README.md)

별도로 두 채점 항목이 공개 질문보다 넓은 설명을 요구했습니다. 저장 위치 질문에는 단어 수의 출처까지, 파일 내용 질문에는 검색 파일과 읽은 파일의 연결까지 요구해 세 방법 모두 공통 감점됐습니다. 공개 질문은 유지한 채 이 두 요소만 제거하고 남은 필수 요소와 근거를 세 방법의 저장 응답에서 다시 확인했습니다. 전체 진단은 12/15, 13/15, 12/15에서 14/15, 15/15, 14/15로 각각 두 건 증가했습니다. 판정과 사용량은 그대로이며 원점수를 보존했습니다. [변경 기준과 검토 기록](real_traces/corrections/scope_v2/README.md)

## 저장 결과 재채점

Python **3.10 이상**, 표준 라이브러리를 사용합니다. 저장 예측 재채점에는 모델 API 키가 필요하지 않습니다. 캐시가 없는 최초 원본 복원에는 네트워크가 필요합니다. 오프라인 실행에는 원본 캐시 14개를 별도로 준비해야 하며, 캐시는 저장소에 포함되지 않습니다. [캐시 준비와 오프라인 검증](docs/offline_reproduction.md)

```sh
git clone https://github.com/apple4ree/evidence-to-action.git
cd evidence-to-action
python3 real_traces/restore_inputs.py
python3 real_traces/harness.py verify
python3 real_traces/test_harness.py
python3 real_traces/test_restore.py
python3 real_traces/evaluate.py
python3 real_traces/rescore_scope.py
```

`restore_inputs.py`는 고정 원본을 받아 입력 15개와 요청 60개를 복원합니다. `evaluate.py`는 저장 예측과 저장 의미 채점을 읽어 `real_traces/results/summary.json`, `per_case.json`, `per_case.csv`를 다시 계산합니다. **새 모델 추론이나 새로운 의미 검수를 수행하는 명령은 아닙니다.** `rescore_scope.py`는 저장된 사후 검토를 사용해 `corrections/scope_v2/results/`에 보정 결과를 따로 생성합니다.

새 추론은 [실행 안내](docs/real_traces.md#3-새-모델-추론)의 별도 작업 폴더에서 시작합니다. 요청 준비와 출력 검사는 구현되어 있으며 모델 호출에는 별도 실행 환경이 필요합니다. API provider adapter는 포함하지 않습니다.

## 제출 코드 바로가기

| 제출 항목 | 핵심 파일 | 확인할 내용 |
|---|---|---|
| **방법론 코드** | [진단 실행 도구](real_traces/harness.py), [평가 코드](real_traces/evaluate.py) | 요청 준비, 출력 검사, 단계 분해의 판정 합성, 저장 예측 채점 |
| **평가 데이터 수집 및 구축 스크립트** | [원본 수집 및 입력 복원](real_traces/restore_inputs.py), [추출 규칙](real_traces/input_recipes.json) | 고정 원본 다운로드, hash 확인, 행동 이전 기록과 대상 행동 추출 |
| **프롬프트 파이프라인 구조** | [공통 규격](real_traces/prompts/common.txt), [단계별 프롬프트](real_traces/prompts/) | 직접 진단, 재검토, 단계 분해의 입력과 출력 연결 |

### 1. 방법론 코드

[real_traces/harness.py](real_traces/harness.py)가 진단 실행의 핵심이다.

- `verify()`: 평가 전에 고정한 파일의 hash를 확인한다.
- `prepare()`: 공통 규격, 단계별 프롬프트, 해당 사례의 공개 입력을 결합한다. 재검토와 관계 판단 단계에는 각각 이전 직접 진단 또는 요구사항 추출 응답을 덧붙인다. 정답 파일은 요청에 넣지 않는다.
- `validate()`: 출력 항목과 관계 라벨을 검사하고, 근거 인용이 지정한 원문 위치에 실제로 존재하는지 확인한다. 요구사항 추출 단계에서는 요구사항 목록의 존재를 검사한다.
- `aggregate()`: 단계 분해의 관계 판단에서 `violated`가 있으면 근거 불충족, 그렇지 않고 `unresolved`가 있으면 판단 불가, 나머지는 근거 충족으로 합성한다.
- `collect()`: 저장 응답을 읽어 검사 기록과 최종 진단 파일을 만든다. 직접 진단과 재검토는 모델이 출력한 판정을 사용한다.

요구사항의 적용 여부와 근거의 의미 관계는 모델이 판단한다. 코드의 인용 검사는 원문 대응을 확인하며, 의미적 정답 여부는 [채점 규격](real_traces/scoring_spec.md)에 따른 [저장 의미 채점](real_traces/semantic_ratings.json)과 함께 평가한다. [evaluate.py](real_traces/evaluate.py)는 판정, 전체 진단, 그룹별 결과와 실행 부담을 집계하고, [rescore_scope.py](real_traces/rescore_scope.py)는 두 채점 범위 보정의 사후 결과를 별도로 계산한다.

### 2. 평가 데이터 수집 및 구축

현재 제출 데이터는 **공개 실행 기록에서 추출한 행동 사례**다. [restore_inputs.py](real_traces/restore_inputs.py)는 선정된 고정 원본을 수집하고 평가 입력을 재구성한다.

1. [input_recipes.json](real_traces/input_recipes.json)의 원본 URL, revision, hash와 추출 위치를 읽는다.
2. 원본을 다운로드하거나 로컬 캐시에서 읽고 SHA-256 및 명시된 Git blob hash를 확인한다.
3. 텍스트 기록은 줄번호, JSON 기록은 기록 개수와 JSON pointer를 사용해 행동 이전 기록과 대상 행동을 분리한다.
4. 사례 템플릿과 결합해 `real_traces/public/`에 입력 15개를 생성하고, 고정 입력의 hash와 비교한다.
5. 저장된 이전 단계 응답을 이용해 기존 요청 60개를 `real_traces/requests/`에 복원한다. 새 실행은 자체 이전 단계 응답으로 요청을 구성한다.

선정과 주석 자료는 별도로 제공한다.

| 자료 | 역할 |
|---|---|
| [수집 목록](real_traces/collection_ledger.json), [원본 선정 기록](real_traces/source_screening.json) | 후보 원본, 포함 및 보류 판단을 추적 |
| [고정 정답](real_traces/gold/), [주석 조정 기록](real_traces/gold_adjudication.json) | 판정, 필수 근거 관계와 주석 검토 결과 |
| [고정 파일 목록](real_traces/freeze_manifest.json) | 평가 입력, 정답, 프롬프트와 설정의 버전 확인 |
| [검토 페이지 생성기](real_traces/review/build_page.py) | 정답과 예측을 숨긴 별도 검토 화면 생성 |

원본 선정과 의미 주석은 검토 과정에서 수행했고, 복원 스크립트가 새로운 사례를 자동 선정하거나 정답을 자동 생성하지는 않는다. 현재 수집 범위는 MAST, Who&When, AgentHallu이며, 14개 원본 실행에서 15개 행동을 구성했다.

```sh
# 저장소 루트에서 원본 수집과 기존 평가 입력 복원
python3 real_traces/restore_inputs.py
python3 real_traces/harness.py verify

# 원본 캐시가 준비된 환경에서 오프라인 복원
python3 real_traces/restore_inputs.py --cache ./eta-source-cache --offline
```

캐시 준비와 검증 결과는 [오프라인 실행 안내](docs/offline_reproduction.md)에 있다.

### 3. 프롬프트 파이프라인 구조

모든 단계는 [common.txt](real_traces/prompts/common.txt)의 판정 기준, 평가 범위, 인용 방식과 공통 출력 규격을 사용한다. 공통 출력은 판정, 문제 필드, 요구사항, 근거 위치와 인용, 관계, 예외, 판단 이유를 포함한다.

| 방법 | 프롬프트와 처리 순서 | 최종 출력 |
|---|---|---|
| 직접 진단 D1 | 공개 입력 → [direct.txt](real_traces/prompts/direct.txt) | 모델이 한 번에 판정과 근거를 출력 |
| 재검토 D2 | 동일 공개 입력 + D1 응답 → [revise.txt](real_traces/prompts/revise.txt) | 이전 판정, 근거와 범위를 검토한 완전한 진단 출력 |
| 단계 분해 P2 | 공개 입력 → [extract.txt](real_traces/prompts/extract.txt) → 동일 공개 입력 + 추출 결과 → [relate.txt](real_traces/prompts/relate.txt) → 코드 합성 | 요구사항과 예외 추출, 관측 관계 판단, 최종 판정 합성 |

재검토의 이전 진단과 단계 분해의 추출 결과는 수정 가능한 중간 출력으로 전달한다. D2는 D1 응답을 재사용하므로 세 방법을 함께 실행할 때 사례당 단계는 `direct`, `revise`, `extract`, `relate`의 네 개다.

새 추론에는 [create_run.py](real_traces/create_run.py)로 별도 작업 폴더를 만들고, `harness.py prepare`로 요청을 구성한 뒤 모델 응답을 저장하고 `collect`로 검사한다. 모델 API 호출 adapter는 포함하지 않으며, 실행 환경에서 요청 전체를 모델에 전달해야 한다. 단계별 명령과 응답 저장 위치는 [새 모델 추론 안내](docs/real_traces.md#3-새-모델-추론)에 정리했다.

## 구현을 읽는 순서

| 파일 | 역할 |
|---|---|
| [input_recipes.json](real_traces/input_recipes.json), [restore_inputs.py](real_traces/restore_inputs.py) | 원본 URL, 버전과 hash, 행동 경계, 입력 복원 |
| [harness.py](real_traces/harness.py), [prompts](real_traces/prompts/) | 공통 입력, 단계별 요청, 출력 참조 검사, P2 합성 |
| [gold](real_traces/gold/), [scoring_spec.md](real_traces/scoring_spec.md) | 고정 정답과 핵심 의미 요소 |
| [evaluate.py](real_traces/evaluate.py) | 판정, 전체 진단, 유보, 원본 그룹 집계 |
| [predictions](real_traces/predictions/), [semantic_ratings.json](real_traces/semantic_ratings.json) | 저장 진단과 방법 이름을 가린 의미 채점 |
| [human_review](real_traces/human_review/) | Gemini 답변, 미조정 불일치, 인용 위치 점검 |
| [review](real_traces/review/) | 정답을 숨긴 사람 검토 페이지 생성 |

## 실행 범위와 다음 검증

관측 모델은 `gpt-6-astra` alias, reasoning effort `medium`입니다. 고정 snapshot과 과금액은 확인되지 않았습니다. 새 임시 폴더와 패키지 없는 가상환경에서 네트워크를 차단한 채 캐시 복원, 고정 파일 검증, 원점수·보정 점수 재채점과 테스트 7개를 통과했습니다. 온라인 다운로드 전체 경로는 DNS 제한으로 재검증하지 못했습니다. [환경과 재현 범위](docs/real_traces.md#4-실행-환경과-재현-범위)

현재 자료는 공개 원문을 읽어 선정한 탐색 비교입니다. 현재 정답은 LLM 검수와 Gemini 판정 비교를 거쳤으며, 사람 검토를 통한 판정 기준의 타당성과 주석 재현성은 후속 검증 항목입니다. 개발자 조사 효용도 후속 평가합니다. 다음 검증은 **남은 정답 경계 조정과 보정 규격 검수 → 별도 실제 실행 평가 → 개발자 조사 정확성과 시간** 순서입니다.

## 연구 이력

[전체 커밋 메시지 한국어 번역](docs/history/commits_ko.md)과 [커밋별 변경 이유와 결과 영향](docs/history/commits.md)에서 구현, 공개 실행 평가, 채점 보정, Gemini 출처 정정의 흐름을 확인할 수 있습니다.

이전 합성 벤치마크와 전체 전달 경로 복원 실험은 [과거 실험 안내](docs/history/README.md)에 분리했습니다. 기존 코드, 원점수와 실행 기록의 경로는 유지하며 현재 결과와 합산하지 않습니다. [커밋 이력](https://github.com/apple4ree/evidence-to-action/commits/main/)은 실제 저장소 변경을 기록합니다.
