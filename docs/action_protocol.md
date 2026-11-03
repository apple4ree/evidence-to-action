> **과거 실험 안내:** 현재 공개 실행 벤치마크는 [실행 안내](real_traces.md)를 참고하세요. 이 문서는 이전 자료와 코드의 재현을 위해 보존합니다.

# 행동 진단 실험 프로토콜과 현재 상태

**현재 상태: 확대 합성 평가가 완료됐습니다.** 24 family·96개 중 개발 6 family·24개, 평가 18 family·72개로 분리했습니다. 실제 개발 실행은 사전 선정 6개 사례·24개 세션, 평가 실행은 72개 사례·288개 세션입니다. D1·D2·P2 모두 판정 72/72, 원래 전체 진단 71/72이며 원점수와 사후 민감도를 별도로 보존합니다.

새 사용자는 [새 모델 실행 안내](new_run.md)를 따르세요. 모델 없이 저장 결과를 확인하려면 저장소 루트에서 `python3 scripts/replay.py --output runs/replay`를 실행합니다.

## 현재 안내와 보존 기록

| 자료 | 역할 |
|---|---|
| [new_run.md](new_run.md) | 현재 저장소에서 새 실행 폴더 준비 → 단계별 요청·응답 저장 → 새 의미 검수·채점 |
| [action_scoring.md](action_scoring.md) | 적용 중인 구성요소·진단 채점 규격 |
| [history/action_protocol_pretest.md](history/action_protocol_pretest.md) | 당시 계획·수정 이력을 바이트 그대로 보존한 **실험 전 기록** |
| `data/expanded_frozen.zip` 내부 `protocol.md` | 원래 freeze에 포함된 같은 과거 계획. 현재 사용 안내가 아님 |

보존 기록의 “검수 진행 중 / 예측 없음”은 작성 당시 상태이며 현재 상태가 아닙니다. 초기 긴 기록 길이와 모델·토큰 미확인 서술도 당시의 기록입니다. 최종 관측된 실행 alias는 gpt-6-astra, reasoning effort는 medium입니다. 토큰·활성 시간은 [관측 사용량](../results/runtime_summary.json)에 있으며 immutable snapshot과 금액은 여전히 미확인입니다.

## 경로 기준

| 경로 표기 | 어디를 기준으로 보는가 |
|---|---|
| `action/`, `provenance/`, `docs/`, `results/` | 현재 GitHub 저장소 루트. `action/`은 코드 열람·단위 테스트용이며 완전한 실행 폴더가 아님 |
| `data/public_cases/`, `run_config.json`, `review/`, `prompts/` | archive를 푼 **실행 폴더** 내부. 새 실행은 `runs/new-inference/`, 재채점은 `runs/replay/` |
| `../natural_language_experiment/` | 과거 연구 폴더의 초기 12개 평가 위치. 현재 저장소에 없으며 새 실행의 의존성이 아님 |
| `workflow.py`, `harness.py`, `evaluate.py` | 실행 폴더에도 동결본이 포함됨. 새 안내의 명령은 그 폴더로 이동한 뒤 실행 |

## 유지하는 비교 규칙

- 동일한 정책·도구 문서·행동 직전 관측·대상 행동을 D1·D2·P2에 제공합니다. 라벨·family·조건 태그·정답 요구사항은 예측 입력에서 제외합니다.
- D1은 직접 진단, D2는 D1 응답의 검토·수정, P2는 요구사항 추출 → 관계 판단 → 코드 합성입니다. D1 재사용으로 사례당 고유 진단 세션은 4개입니다.
- 각 단계는 독립 문맥에서 실행합니다. `revise`에는 해당 D1 출력, `relate`에는 해당 `extract` 출력만 추가합니다. 호출 수를 계산 비용으로 해석하지 않습니다.
- Supported / Unsupported / Indeterminate의 경계, 핵심 위반 관계 평가, family 단위 분할·bootstrap은 [채점 규격](action_scoring.md)을 따릅니다.
- 기술적 무응답만 최대 1회 재시도하며 오답·잘못된 JSON·잘못된 참조를 수정 재시도하지 않습니다. 새 예측에는 새 의미 검수가 필요합니다.

새 모델로 같은 자료를 실행해도 기존 평가와 별도 실행으로 보고합니다. 공개된 평가셋이므로 이를 새로운 독립·비공개 평가셋이라고 부르지 않습니다. 사람이 아닌 LLM 검수, 모델 snapshot 미확인, 실제 Agent rollout·개발자 효용 미측정이라는 범위도 유지합니다.
