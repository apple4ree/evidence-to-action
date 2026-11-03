# Evidence-to-Action

**Agent 행동의 근거 충족성 진단을 위한 데이터·프롬프트·평가 파이프라인**

콕스웨이브 AI 리서치 엔지니어 직무과제의 코드 제출본입니다. 값의 존재뿐 아니라 정책, 출처, 대상·시점·범위가 행동을 뒷받침하는지 평가합니다. 완성된 서비스나 학습 모델이 아니라 **핵심 구현과 재실행 가능한 평가 자료**를 제공합니다.

## 핵심 결과와 현재 선택

- 확대 자연어 **합성** 평가: 24 family·96개 입력 중 평가 18 family·72개. D1·D2·P2 모두 판정 **72/72**, 동결 정답 기준 전체 진단 **71/72**입니다.
- 한 사례의 동등한 필드 귀속을 모든 방법에 허용한 사후 민감도에서는 모두 72/72입니다. 원점수를 대체하지 않습니다.
- 공개 실행의 오류 탐색 2개도 직접 판정으로 진단했습니다. 별도 정상 조회 3개에서는 판정이 모두 맞았으나 P2-L이 중간 전달 위치를 한 번 누락했습니다. 이는 행동 판정 오류와 다릅니다.
- 따라서 **직접 판정을 기본 구현으로 선택**하고 단계 분리는 비교·병목 분석 도구로 유지합니다. 동률은 통계적 동등성이나 모든 환경에서의 충분성 입증이 아닙니다.

## 5분 실행 안내

Python **3.10 이상**, 표준 라이브러리만 필요합니다. API 키나 패키지 설치가 필요하지 않습니다.

```bash
git clone https://github.com/apple4ree/evidence-to-action.git
cd evidence-to-action
python3 -m unittest discover -s action -p 'test_*.py' -v
python3 -m unittest discover -s provenance -p 'test_*.py' -v
python3 scripts/replay.py --output runs/replay
```

`replay.py`는 archive hash와 기존 평가 전 freeze를 검사하고, 저장 예측·동결 정답·저장된 의미 검수 결과로 **재채점**합니다. 재계산한 구성요소·조건별·family별 점수가 보존 결과와 같은지 검사합니다. 새 모델 추론이나 의미 검수는 실행하지 않습니다. 결과는 `runs/replay/test_results.json`에 생성됩니다. 기존 경로가 있으면 덮어쓰지 않으며 다른 `--output`을 사용하면 됩니다.

데이터 생성 뼈대도 별도로 실행할 수 있습니다.

```bash
python3 scripts/generate.py --output runs/authoring-draft
```

이 스크립트는 연구 중 사용한 작성기의 로직을 유지하고 출력 경로와 덮어쓰기 방지만 추가했습니다. **초기 작성 단계의 96개 합성 입력·잠정 정답**을 생성합니다. 이후 긴 기록 수정, event ID 정리, 독립 문맥 LLM 검수·조정을 거친 동결 평가본과는 다릅니다. 생성물을 기존 72개 성능의 입력이라고 사용하지 마세요. 동결 자료와 작성·검수 이력은 archive에 보존했습니다.

## 무엇을 읽으면 되는가

| 파일 | 역할 |
|---|---|
| [`action/workflow.py`](action/workflow.py) | 참조·스키마 검사, P2 관계 상태 → 최종 판정 합성 |
| [`action/prompts/`](action/prompts/) | 공통 출력과 direct / revise / extract / relate 프롬프트 |
| [`action/harness.py`](action/harness.py) | 공개 입력만 전달, 단계 연결, 원시 응답 저장, freeze 및 기술 실패 재시도 제한 |
| [`action/evaluate.py`](action/evaluate.py) | 탐지·진단·유보·대조쌍·조건·family 단위 평가와 bootstrap |
| [`provenance/workflow.py`](provenance/workflow.py) | 최초 출처·주요 변환·재사용 위치의 참조 검사와 합성 |
| [`provenance/prompts/`](provenance/prompts/) | D1-L·D2-L·P2-L 공통 출처 출력 |
| [`scripts/generate.py`](scripts/generate.py) | 24 family의 초기 합성 자료 생성 |
| [`scripts/replay.py`](scripts/replay.py) | 동결 자료 검증 및 저장 결과 재채점 |
| [`data/example_public.json`](data/example_public.json) | 정답·family·조건 태그가 없는 탐지기 입력 예시 |
| [`docs/action_scoring.md`](docs/action_scoring.md) | 핵심 관계 주석과 채점 단위 |
| [`docs/provenance_scoring.md`](docs/provenance_scoring.md) | 출처 경로 평가 규격 |
| [`results/`](results/) | 확대 평가 원점수·사후 민감도·공개 출처 비교 결과 |
| [`source_map.json`](source_map.json) | 기존 연구 코드와 제출 파일의 대응 및 변경 범위 |

## 두 하위 과제

**A. 행동 정당성 진단:** 값·선택이 당시 정책과 관측으로 정당화되는가? 판정, 문제 필드, 요구사항, 근거와 예외를 출력합니다.

- `supported`: 필수 요구사항 또는 허용 예외가 확인됨.
- `unsupported`: 명시적 위반, 또는 사전 확인이 필수인 완전한 관련 기록에서 필수 근거 없이 실행함.
- `indeterminate`: 정책·기록 부족으로 결정할 수 없음.

**B. 근거 전달 과정 복원:** 최초 출처 → 주요 저장·요약·전달 → 재사용 위치와 범위 변화를 출력합니다. B의 중간 위치 누락만으로 A 판정까지 틀렸다고 처리하지 않습니다. P2와 출력 범위가 확장된 P2-L 점수를 직접 비교하지 않습니다.

## 비교 파이프라인

```text
공통 정책·도구 문서·행동 전 관측·대상 행동
  ├─ D1: 직접 구조화 진단
  ├─ D2: D1 출력 → 비판적 검토·수정
  └─ P2: 요구사항·예외 추출 → 관측 관계 판단 → 코드 합성
```

모든 방법은 같은 공개 입력과 최종 출력 규격을 사용합니다. 사람이 작성한 정답 요구사항·라벨을 탐지기에 주지 않습니다. D1을 D2 첫 단계에 재사용하므로 사례당 고유 진단 세션은 4개입니다. 내부 파일 읽기·도구 왕복이 있어 세션 수와 모델 응답 수·계산 비용은 다릅니다.

모델은 자연어 정책 적용과 의미 관계를 판단합니다. 코드는 ID 존재·출력 형식·상태 합성·채점을 수행합니다. **ID나 hash의 적합성이 의미적 정당성을 보증하지 않습니다.** 일반적인 자연어 시점·권한 판정이나 숨은 actor context 복원은 구현 범위가 아닙니다.

## 재실행 범위

| 작업 | 이 저장소에서 가능한 범위 |
|---|---|
| 코드 경계 검사 | 모델 없이 unit test 실행 |
| 확대 합성 평가 재채점 | 저장 예측 + 동결 정답 + 저장된 의미 검수 ratings 사용 |
| 새 작성 초안 생성 | 초기 작성기 실행; 동결 평가 정답을 새로 생성하는 명령이 아님 |
| 새 모델 예측 생성 | harness와 프롬프트 제공. 별도 모델 실행 환경 필요 |
| 공개 출처 비교 | 핵심 코드·프롬프트·보존 결과 제공. 원본 실행 전체와 내부 로그는 재배포하지 않음 |

`harness.py`는 **모델 API 클라이언트가 아닙니다**. 원래 예측은 독립 문맥의 runtime-managed subagent에서 실행하고 최종 응답을 저장했습니다. 관측 alias는 `gpt-6-astra`, reasoning effort는 `medium`이며 immutable snapshot과 금액은 미확인입니다. 새 모델 실행은 별도 새 실행 폴더에서 수행해야 하며 동결 archive의 예측을 덮어쓰면 안 됩니다. 단계별 사용법과 재시도 규칙은 [실험 프로토콜](docs/action_protocol.md)에 있습니다.

의미 검수 ratings는 독립 문맥 LLM 검수 결과이며 독립 사람 주석이 아닙니다. 재채점은 이 ratings를 입력으로 사용하므로 자연어 진단의 의미적 정확성을 새로 검증하지 않습니다. 실제 Agent 오류 발생률, 사람 주석 재현성, 개발자 조사 효용은 측정하지 않았습니다.

## 자료와 공개 범위

`data/expanded_frozen.zip`에는 합성 입력, 작성·검수 이력, 동결 코드·프롬프트, 저장된 진단 출력이 포함됩니다. `private_`는 **탐지기에서 가려야 하는 평가용 정답·메타데이터**라는 뜻이며 사용자 개인정보라는 뜻은 아닙니다. 새 평가 시 모델 입력과 분리해야 합니다.

실제 공개 기록은 [MAST](https://github.com/multi-agent-systems-failure-taxonomy/MAST), [Who&When](https://github.com/mingyin1/Agents_Failure_Attribution), [AgentHallu](https://github.com/liuxuannan/AgentHallu)에서 확인할 수 있습니다. 원본 revision과 사례 식별자는 제출 제안서에 있습니다. 이 저장소는 타 저장소 원본 로그를 복제하지 않습니다.

## 커밋 이력

기존 연구 폴더에는 Git 이력이 없었습니다. **이번 제출 정리부터 실제 변경 단위로 커밋**하며 과거 실험 당시의 커밋처럼 소급 작성하지 않습니다. 기존 코드의 출처와 그대로 유지한 파일 hash는 `source_map.json`에 남겼습니다.
