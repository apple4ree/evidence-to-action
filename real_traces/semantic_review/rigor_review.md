# 실제 기록 비교: 제출 원고의 근거·범위 검토

검토일: 2026-11-03. 요청된 protocol, scoring_spec, summary, per_case, semantic_ratings, 두 blinded review, 제출 manuscript와 보조 environment_audit를 읽었다. 외부 검색, 새 추론, 재채점은 하지 않았다. ara-rigor-reviewer의 D1–D6를 체크리스트로만 사용했다. ARA 구조 검증이나 공식 Level 2 심사가 아니며 Seal·등급을 부여하지 않는다. 아래 행 번호는 검토 당시 manuscript.md 기준이다.

## 우선 수정

### F01 — Major · D1/D3/D6: 전체 진단 점수의 공통 감점 두 건에 범위 불일치가 누락됨

- 위치: `submission_real_trace_final/manuscript.md:207–215`, Table 9 및 4.4.
- 원고 인용: “전체 진단은 판정, 필수 의미 요소, 유효한 근거 연결을 함께 맞힌 경우다.”
- 근거: `experiment/blinded_review/review_batch2.md`, Boundary concerns: “AHN08's public focal relation is file location, while normal_value additionally requires value provenance. AHN09's public focal relation asks about quoted content support, while file_link additionally requires the located-file/directory relationship.”
- 관찰: semantic_ratings의 AHN08 세 출력은 location_gap/uncertainty 통과, normal_value 실패다. AHN09 세 출력은 content_preservation 통과, file_link 실패다. 모두 핵심 근거의 의미 정확성은 true, contradiction은 false이며 decision도 맞았다. 이 공통 두 사례가 모든 방법의 전체 진단 점수를 각각 2건 낮춘다. 원고는 실제로 다른 판정 오류 두 건만 설명하고, 이 평가 설계의 한계를 설명하지 않는다.
- 영향: 독자는 12/15, 13/15, 12/15를 공개 focal relation의 실패 수로 읽을 수 있다. 기준이 사전 동결됐다는 사실은 입력과 기준의 범위 일치까지 보증하지 않는다.
- 수정: **원점수·정답·기준을 그대로 유지**하고 Table 9 아래에 다음 취지를 추가한다. “AHN08의 값 출처와 AHN09의 파일·디렉터리 연결은 공개 focal relation보다 넓은 필수 기준이었다. 세 방법 모두 이 요소를 누락해 각각 두 건씩 전체 진단에서 감점됐다. 원점수는 유지하되 이 공통 감점은 입력–채점 범위 정합성의 한계로 별도 해석한다.” 사후 점수로 본표를 대체하지 않는다.

### F02 — Minor · D3/D4: 일반 정의와 실제 국소 Supported의 범위 구분을 더 가까이 표시

- 위치: manuscript.md §3.1, §4.3 첫 문단.
- 원고 인용: “**Supported**는 적용 필수 요구사항이 근거로 충족되거나 허용 예외가 확인된 경우다.” / “7개 오류, 5개 정상, 3개 판단 불가를 같은 입력으로 비교했다.”
- 근거: `experiment/scoring_spec.md:7`: “이는 모든 적용 요구사항의 완전한 정당성을 판정하는 과제가 아니라 지정한 핵심 관계의 진단이다.”
- 관찰: §3.2에는 제한이 제대로 있다. 그러나 일반 정의와 Table 9에서 독자가 모든 정책·도구 계약 충족 판정으로 읽을 여지가 남는다. 특히 정상 5건은 전체 행동·실행 성공 검증이 아니다.
- 수정: 실제 비교의 첫 문단에 “여기서 정상·오류는 공개 기록에서 지정한 핵심 관계에 한정한다”를 붙인다. 일반 정의에는 실제 기록 비교가 이 정의를 국소 관계에 제한해 적용함을 연결한다.

### F03 — Minor · D4: “직접 진단만”이라는 표현의 비교 집합이 불명확

- 위치: manuscript.md:217.
- 원고 인용: “직접 진단만 맞힌 것은 부분 목록 사례, 단계 분해만 맞힌 것은 재생 이력 사례로 각각 1개다.”
- 관찰: 이는 D1–P2 쌍 비교에서는 정확하지만 재검토 D2는 두 사례 모두 맞혔다. 앞 표가 세 방법 비교이므로 ‘세 방법 중 유일’로 읽힐 수 있다.
- 수정: 문두를 “직접 진단과 단계 분해를 서로 비교하면”으로 한정한다.

## 확인한 강점과 수치 일치

- **분모와 점수:** 15개 행동, 14개 원본 그룹, 7 Unsupported/5 Supported/3 Indeterminate가 protocol·scoring·결과와 일치한다. MAST-R01/R05의 group_id가 같으며 15개 독립 실행으로 취급하지 않는다. Table 9 판정 14/15·15/15·14/15와 전체 진단 12/15·13/15·12/15는 summary/per_case/semantic_ratings와 일치한다.
- **실패 위치:** D1의 MAST-R06 Unsupported, P2의 MAST-R03 Indeterminate가 결과와 일치한다. MAST-R03은 실제 미발견 곡의 존재가 아니라 제한된 검색으로 전체 부정 결론을 정당화하는 관계를 평가한다. MAST-R06은 순환 큐 위치만으로 과거 재생 이력을 결정할 수 없다는 다른 관계다. 이 차이를 원고가 설명한다.
- **비용:** 평균 활성 시간 23.0·45.3·46.2초는 summary의 23.0082·45.2645·46.1692와 일치한다. 관측 토큰은 D1 입력 1,070,797/출력 10,845, D2 2,042,649/22,036, P2 2,012,209/21,623이다. D2는 재사용 D1을 포함하므로 세 방법 합산은 고유 실행 비용이 아니다. 원고는 API 호출 수나 순수 추론 latency, 금전 비용을 주장하지 않는다. 이 구분을 유지한다.
- **60의 의미:** protocol의 direct/revise/extract/relate 네 고유 세션 × 15 = 완료 세션 60이라는 설계와 원고가 일치한다. 완료 60과 중단 시도 1을 구별한다. 다만 이번 검토는 60개 runtime 원본을 전수 대조하지 않았으므로 전체 입력 exact 전달, 실제 alias/effort 일치와 재시도 경위를 독립 재검증했다고 주장하지 않는다. environment_audit도 prepared 본문 전달과 최초 spawn invocation 본문 일치를 별개로 취급한다.
- **실행과 actor context:** §1.1·3.2·4.7 및 scoring_spec는 공개 다중 actor 기록이 원래 단일 actor의 전체 입력이라는 가정을 피한다. 평가 predictor의 전체 입력 전달 확인을 원래 업무 actor의 관측 범위 확인으로 바꾸어 쓰지 않는다.
- **검수 provenance:** 원고는 정답과 의미 채점을 별도 문맥 LLM 검수로 밝히고 사람 검증 미완료, 검토자 간 일치도 미측정을 명시한다. 익명화가 모델 간/사람 간 독립 검증을 의미한다는 주장은 없다.
- **원점수 보존:** 합성 account/mode와 초기 경로 완전성의 사후 민감도를 본점수와 분리한 서술이 있다. 이번 실제 비교도 frozen primary 결과를 유지한다.

## 체크리스트 결론

D1 근거 관련성과 D3 범위 조정에서 F01이 가장 중요하다. D2는 후속 사람 검토·효용 검증 및 실패 시 규격 축소 조건이 제시되어 있으나 현재 일반화 성능을 검증한 것은 아니다. D4는 본문 흐름이 일관되며 위 두 문구 수정으로 더 명확해진다. D5는 초기 전달 실패, 정답 설명 보정, 부정 결과와 사후 민감도를 보존한 점이 강점이다. D6는 같은 입력과 D2 비교, 14개 원본 그룹 및 실제 세션 시간 보고가 적절하다. 작은 탐색 표본·단일 실행·LLM gold의 한계를 원고가 명시하므로 추가 실험 없이도 제한된 탐색 결과로 제출할 수 있다. 우선 F01을 반영하고 원점수는 변경하지 않는 것이 권고다.
