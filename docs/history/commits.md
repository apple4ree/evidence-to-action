# 커밋 이력과 변경 해설

현재 제출물의 핵심은 **공개 실행 14개에서 추출한 15개 행동의 진단 벤치마크**다. 이 문서는 기존 14개 커밋의 메시지와 변경 파일을 확인해 작성한 사후 해설이다. 원래 커밋 메시지를 수정하거나 과거에 작성된 댓글로 표시한 기록이 아니다.

## 먼저 볼 변경

1. [공개 실행 벤치마크 추가](https://github.com/apple4ree/evidence-to-action/commit/79e043fb8e8eaf49917fef7dd0f207970f1bfecb): 입력 복원, 진단과 평가 구현.
2. [채점 범위 보정](https://github.com/apple4ree/evidence-to-action/commit/af7b1d52f129f9ae3740933a6ab0c971c09a2681): 원점수 보존, 변경 기준과 결과 영향.
3. [Gemini 출처 정정](https://github.com/apple4ree/evidence-to-action/commit/a04e292196e1a627ae502753f0f4192c07daf3ca): 제출 검토 답변의 주체 정정.
4. [현재 실행 안내](../real_traces.md): 저장 결과 재채점과 새 추론의 구분.

## 변경 흐름

기존 구현·실험 공개 → 재현 안내 보완 → 공개 실행 벤치마크 추가 → 원본 선정과 검토 기록 → 과거 자료 분리 → 채점 범위 보정 → Gemini 출처 정정 → 문서 표현 통일.

아래 시각은 **2026년 11월 3일, 한국 시간(UTC+9)**이다. 저장소 반영 시점이며 각 연구 작업의 시작·종료 시각은 아니다. 원래 커밋과 날짜는 보존했다.

| 시각 | 커밋 | 변경 | 결과 영향 |
|---|---|---|---|
| 16:09:42 | [6616813](https://github.com/apple4ree/evidence-to-action/commit/66168133b7adcf5180808ed4ed6f7463a95c0227) | 저장소 시작 | 자료·구현·설명 정리 |
| 16:17:46 | [543d5bb](https://github.com/apple4ree/evidence-to-action/commit/543d5bbb6c53705ae665d806ec0ae4fef236155e) | 진단 파이프라인 공개 | 자료·구현·설명 정리 |
| 16:18:01 | [cd31964](https://github.com/apple4ree/evidence-to-action/commit/cd319644c9cda0944073cedb2eb80b5b1b1b18e9) | 기존 평가 자료와 재채점 공개 | 자료·구현·설명 정리 |
| 16:18:13 | [f72aea7](https://github.com/apple4ree/evidence-to-action/commit/f72aea76e9b46f082875e1c9dcfd825efba8f098) | 초기 재현 안내 | 자료·구현·설명 정리 |
| 16:22:22 | [2efabbd](https://github.com/apple4ree/evidence-to-action/commit/2efabbdaf561993cbab0abb020774e02c0ffb4ab) | CSV 바이트 보존 | 자료·구현·설명 정리 |
| 16:41:55 | [b90305e](https://github.com/apple4ree/evidence-to-action/commit/b90305e1d2cda2fc5c7fc483395339c50f386410) | 새 추론 사용 안내 보완 | 자료·구현·설명 정리 |
| 19:47:13 | [79e043f](https://github.com/apple4ree/evidence-to-action/commit/79e043fb8e8eaf49917fef7dd0f207970f1bfecb) | 현재 공개 실행 벤치마크 추가 | 평가 결과 추가 또는 사후 보정 |
| 19:49:58 | [52bbdea](https://github.com/apple4ree/evidence-to-action/commit/52bbdeacb3ed721a3a4faf62dbd63f0935a419d2) | 원본 선정 근거 보존 | 자료·구현·설명 정리 |
| 20:10:31 | [4e02240](https://github.com/apple4ree/evidence-to-action/commit/4e02240dc8f087514407d1035d2bf823d5674492) | 제출 검토 답변 비교 | 자료·구현·설명 정리 |
| 21:15:14 | [1617fd2](https://github.com/apple4ree/evidence-to-action/commit/1617fd23036db364dbcf6707b8fad9b814c317d5) | 현재 연구와 과거 실험 분리 | 자료·구현·설명 정리 |
| 21:15:25 | [3a4bac3](https://github.com/apple4ree/evidence-to-action/commit/3a4bac36207fc36b7c6dca09d7c0d9e0c5daf0c5) | 사례 중심 README 정리 | 자료·구현·설명 정리 |
| 21:27:30 | [af7b1d5](https://github.com/apple4ree/evidence-to-action/commit/af7b1d52f129f9ae3740933a6ab0c971c09a2681) | 질문과 채점 범위 보정 | 평가 결과 추가 또는 사후 보정 |
| 22:17:18 | [a04e292](https://github.com/apple4ree/evidence-to-action/commit/a04e292196e1a627ae502753f0f4192c07daf3ca) | 검토 주체를 Gemini로 정정 | 자료·구현·설명 정리 |
| 22:59:39 | [6fd68b4](https://github.com/apple4ree/evidence-to-action/commit/6fd68b45bdaf54236ff0f0a6ccdbfafc9e55fe29) | 보고서와 검토 설명 통일 | 자료·구현·설명 정리 |

## 커밋별 설명

### 6616813 — 저장소 시작

[원래 커밋과 diff](https://github.com/apple4ree/evidence-to-action/commit/66168133b7adcf5180808ed4ed6f7463a95c0227) · `Initial commit`

- **이유:** 제출 코드를 공개할 저장소를 생성했다.
- **변경:** README의 저장소 이름을 추가했다.
- **영향·해석:** 코드와 실험 자료는 후속 커밋에서 추가된다.
- **대표 변경 파일:** [README.md](https://github.com/apple4ree/evidence-to-action/blob/66168133b7adcf5180808ed4ed6f7463a95c0227/README.md).

### 543d5bb — 진단 파이프라인 공개

[원래 커밋과 diff](https://github.com/apple4ree/evidence-to-action/commit/543d5bbb6c53705ae665d806ec0ae4fef236155e) · `feat: add action and provenance diagnostic pipelines`

- **이유:** 연구 작업공간의 핵심 진단 절차를 제출 가능한 코드로 묶었다.
- **변경:** action/과 provenance/에 프롬프트, 입력 준비, 출력 검사, 합성, 경계 테스트를 추가했다.
- **영향·해석:** 현재 공개 실행 평가 이전의 구현이다. 현재 실행 진입점은 real_traces/다.
- **대표 변경 파일:** [.gitignore](https://github.com/apple4ree/evidence-to-action/blob/543d5bbb6c53705ae665d806ec0ae4fef236155e/.gitignore), [README.md](https://github.com/apple4ree/evidence-to-action/blob/543d5bbb6c53705ae665d806ec0ae4fef236155e/README.md), [action/evaluate.py](https://github.com/apple4ree/evidence-to-action/blob/543d5bbb6c53705ae665d806ec0ae4fef236155e/action/evaluate.py), [action/export_tables.py](https://github.com/apple4ree/evidence-to-action/blob/543d5bbb6c53705ae665d806ec0ae4fef236155e/action/export_tables.py).

<details>
<summary>당시 커밋 본문</summary>

Preserve the existing D1/D2/P2 workflow, prompts, harnesses and boundary tests. Separate semantic model judgments from reference checks and deterministic label synthesis.

</details>

### cd31964 — 기존 평가 자료와 재채점 공개

[원래 커밋과 diff](https://github.com/apple4ree/evidence-to-action/commit/cd319644c9cda0944073cedb2eb80b5b1b1b18e9) · `feat: package frozen evaluation and reproducible scoring`

- **이유:** 입력, 저장 예측, 의미 채점으로 과거 평가를 다시 계산할 수 있게 했다.
- **변경:** 고정 합성 자료, 생성 스크립트, replay.py, 원점수와 민감도 결과를 추가했다.
- **영향·해석:** 현재 15개 행동 비교와 별개인 과거 실험 자료다. 저장 예측 재채점과 새 모델 호출을 구분한다.
- **대표 변경 파일:** [data/archive_manifest.json](https://github.com/apple4ree/evidence-to-action/blob/cd319644c9cda0944073cedb2eb80b5b1b1b18e9/data/archive_manifest.json), [data/example_public.json](https://github.com/apple4ree/evidence-to-action/blob/cd319644c9cda0944073cedb2eb80b5b1b1b18e9/data/example_public.json), [data/expanded_frozen.zip](https://github.com/apple4ree/evidence-to-action/blob/cd319644c9cda0944073cedb2eb80b5b1b1b18e9/data/expanded_frozen.zip), [results/expanded_original.json](https://github.com/apple4ree/evidence-to-action/blob/cd319644c9cda0944073cedb2eb80b5b1b1b18e9/results/expanded_original.json).

<details>
<summary>당시 커밋 본문</summary>

Add the synthetic authoring generator, 96-case frozen archive, saved diagnostic outputs and semantic ratings. Replay checks original hashes and reproduces the 72-case scoring without new model calls. Preserve primary scores and post-hoc sensitivity separately.

</details>

### f72aea7 — 초기 재현 안내

[원래 커밋과 diff](https://github.com/apple4ree/evidence-to-action/commit/f72aea76e9b46f082875e1c9dcfd825efba8f098) · `docs: document submission scope, reproduction and verified results`

- **이유:** 코드만으로 파악하기 어려운 실행 범위와 자료 대응을 설명했다.
- **변경:** 한국어 README, 채점 규격, 검증 기록과 source_map.json을 추가했다.
- **영향·해석:** 당시 합성 및 출처 복원 중심 안내다. 현재 안내는 docs/real_traces.md를 따른다.
- **대표 변경 파일:** [README.md](https://github.com/apple4ree/evidence-to-action/blob/f72aea76e9b46f082875e1c9dcfd825efba8f098/README.md), [docs/action_protocol.md](https://github.com/apple4ree/evidence-to-action/blob/f72aea76e9b46f082875e1c9dcfd825efba8f098/docs/action_protocol.md), [docs/action_scoring.md](https://github.com/apple4ree/evidence-to-action/blob/f72aea76e9b46f082875e1c9dcfd825efba8f098/docs/action_scoring.md), [docs/provenance_scoring.md](https://github.com/apple4ree/evidence-to-action/blob/f72aea76e9b46f082875e1c9dcfd825efba8f098/docs/provenance_scoring.md).

<details>
<summary>당시 커밋 본문</summary>

Add Korean quickstart, source mapping, scoring specifications and completed checks. Explain direct-judge selection, distinct action/path tasks, model-access limitations and the difference between replay and new inference. Record submission commits without backdating research history.

</details>

### 2efabbd — CSV 바이트 보존

[원래 커밋과 diff](https://github.com/apple4ree/evidence-to-action/commit/2efabbdaf561993cbab0abb020774e02c0ffb4ab) · `fix: preserve original CSV bytes in the submission`

- **이유:** 내보내기 중 바뀐 줄바꿈으로 파일 hash가 달라지는 문제를 수정했다.
- **변경:** results/provenance_components.csv의 원본 줄바꿈을 복원했다.
- **영향·해석:** 데이터 값과 점수 변경 없이 원본 파일 대응을 유지했다.
- **대표 변경 파일:** [results/provenance_components.csv](https://github.com/apple4ree/evidence-to-action/blob/2efabbdaf561993cbab0abb020774e02c0ffb4ab/results/provenance_components.csv).

<details>
<summary>당시 커밋 본문</summary>

Keep the exported CSV line endings unchanged so its published blob matches source_map.json. No data values or scores change.

</details>

### b90305e — 새 추론 사용 안내 보완

[원래 커밋과 diff](https://github.com/apple4ree/evidence-to-action/commit/b90305e1d2cda2fc5c7fc483395339c50f386410) · `docs: clarify current protocol and fresh inference workflow`

- **이유:** 과거 계획과 현재 사용 안내, 재채점과 새 추론을 구분했다.
- **변경:** 개발 전 프로토콜을 보존하고 작업 폴더 준비, 단계별 명령, 입출력 예시와 실행 요약을 추가했다.
- **영향·해석:** 커밋 본문에 경계 테스트 20개와 fixture 흐름 점검이 기록돼 있다. 과거 실험 경로에 대한 점검이며 새 추론 결과를 추가한 커밋은 아니다.
- **대표 변경 파일:** [README.md](https://github.com/apple4ree/evidence-to-action/blob/b90305e1d2cda2fc5c7fc483395339c50f386410/README.md), [data/example_d1_output.json](https://github.com/apple4ree/evidence-to-action/blob/b90305e1d2cda2fc5c7fc483395339c50f386410/data/example_d1_output.json), [docs/action_protocol.md](https://github.com/apple4ree/evidence-to-action/blob/b90305e1d2cda2fc5c7fc483395339c50f386410/docs/action_protocol.md), [docs/history/action_protocol_pretest.md](https://github.com/apple4ree/evidence-to-action/blob/b90305e1d2cda2fc5c7fc483395339c50f386410/docs/history/action_protocol_pretest.md).

<details>
<summary>당시 커밋 본문</summary>

Preserve pretest protocol, document clean frozen workspace setup and four-stage commands, and add saved input/output example with measured result summary.

Validate 20 boundary tests, fixture-based prepare/save flow, freeze hashes, overwrite refusal, and relative links. No new model inference.

</details>

### 79e043f — 현재 공개 실행 벤치마크 추가

[원래 커밋과 diff](https://github.com/apple4ree/evidence-to-action/commit/79e043fb8e8eaf49917fef7dd0f207970f1bfecb) · `feat: evaluate 15 actions extracted from real agent traces`

- **이유:** 합성 사례 중심 자료에서 실제 공개 실행의 지정 행동 평가로 연구의 중심을 옮겼다.
- **변경:** 고정 원본 복원, 15개 행동 주석, 세 진단 방법, 저장 응답, 의미 채점, 그룹별 결과와 검토 페이지를 추가했다.
- **영향·해석:** 판정은 D1 14/15, D2 15/15, P2 14/15. 당시 전체 진단 원점수는 12/15, 13/15, 12/15다. 채점 범위 보정은 af7b1d5에서 별도 수행했다.
- **대표 변경 파일:** [README.md](https://github.com/apple4ree/evidence-to-action/blob/79e043fb8e8eaf49917fef7dd0f207970f1bfecb/README.md), [docs/real_traces.md](https://github.com/apple4ree/evidence-to-action/blob/79e043fb8e8eaf49917fef7dd0f207970f1bfecb/docs/real_traces.md), [real_traces/README.md](https://github.com/apple4ree/evidence-to-action/blob/79e043fb8e8eaf49917fef7dd0f207970f1bfecb/real_traces/README.md), [real_traces/calls/AHN01_direct.json](https://github.com/apple4ree/evidence-to-action/blob/79e043fb8e8eaf49917fef7dd0f207970f1bfecb/real_traces/calls/AHN01_direct.json).

<details>
<summary>당시 커밋 본문</summary>

Add pinned-source input reconstruction, frozen annotations and prompts, 60 completed native stages, 45 saved diagnoses, blinded semantic ratings and source/group breakdowns. Preserve previous synthetic and provenance results.

Observed decision scores: direct 14/15, revision 15/15, decomposition 14/15. Keep original joint scores and disclose two shared input/rubric scope mismatches. Include a gold-hidden human review page generator; human validation remains pending.

Validate 15 input and 60 request hashes, boundary and reconstruction tests, and replay saved predictions. No claim of general superiority or human annotation agreement.

</details>

### 52bbdea — 원본 선정 근거 보존

[원래 커밋과 diff](https://github.com/apple4ree/evidence-to-action/commit/52bbdeacb3ed721a3a4faf62dbd63f0935a419d2) · `docs: preserve source screening and document verification limits`

- **이유:** 포함·보류 판단과 재현 확인 범위를 추적할 수 있게 했다.
- **변경:** source_screening.json, 검토 해소 기록, 실행 안내와 배포 목록을 보완했다.
- **영향·해석:** 고정 정답과 실험 점수를 바꾸지 않았다. 로컬 캐시 복원과 온라인 다운로드 검증 범위를 구분했다.
- **대표 변경 파일:** [docs/real_traces.md](https://github.com/apple4ree/evidence-to-action/blob/52bbdeacb3ed721a3a4faf62dbd63f0935a419d2/docs/real_traces.md), [real_traces/export_manifest.json](https://github.com/apple4ree/evidence-to-action/blob/52bbdeacb3ed721a3a4faf62dbd63f0935a419d2/real_traces/export_manifest.json), [real_traces/package_from_workspace.py](https://github.com/apple4ree/evidence-to-action/blob/52bbdeacb3ed721a3a4faf62dbd63f0935a419d2/real_traces/package_from_workspace.py), [real_traces/publish_files.json](https://github.com/apple4ree/evidence-to-action/blob/52bbdeacb3ed721a3a4faf62dbd63f0935a419d2/real_traces/publish_files.json).

<details>
<summary>당시 커밋 본문</summary>

Publish collection-time inclusion/exclusion records and final rigor-review resolutions. Clarify offline reconstruction checks and restricted-network/browser verification limits without changing frozen gold or experiment scores.

</details>

### 4e02240 — 제출 검토 답변 비교

[원래 커밋과 diff](https://github.com/apple4ree/evidence-to-action/commit/4e02240dc8f087514407d1035d2bf823d5674492) · `docs: incorporate single-reviewer annotations and preserve frozen scores`

- **이유:** 제출된 15개 판정과 고정 주석의 일치 및 불일치를 확인했다.
- **변경:** 제출 원본, 비교 스크립트, 인용 위치 점검과 검토 방식 기록을 추가했다.
- **영향·해석:** 당시 사람 검토로 기록한 출처 설명은 a04e292에서 Gemini 판정으로 정정됐다. 이 커밋을 사람 검증의 근거로 사용하지 않는다. 원본 답변과 점수는 보존됐다.
- **대표 변경 파일:** [README.md](https://github.com/apple4ree/evidence-to-action/blob/4e02240dc8f087514407d1035d2bf823d5674492/README.md), [docs/real_traces.md](https://github.com/apple4ree/evidence-to-action/blob/4e02240dc8f087514407d1035d2bf823d5674492/docs/real_traces.md), [real_traces/export_manifest.json](https://github.com/apple4ree/evidence-to-action/blob/4e02240dc8f087514407d1035d2bf823d5674492/real_traces/export_manifest.json), [real_traces/human_review/README.md](https://github.com/apple4ree/evidence-to-action/blob/4e02240dc8f087514407d1035d2bf823d5674492/real_traces/human_review/README.md).

### 1617fd2 — 현재 연구와 과거 실험 분리

[원래 커밋과 diff](https://github.com/apple4ree/evidence-to-action/commit/1617fd23036db364dbcf6707b8fad9b814c317d5) · `docs: separate historical experiments from the current benchmark`

- **이유:** 서로 다른 평가 단위와 결과가 섞이지 않도록 자료의 역할을 구분했다.
- **변경:** docs/history/와 과거 안내문에 현재 연구와의 관계를 명시했다.
- **영향·해석:** 과거 코드와 결과 경로는 보존하고 현재 공개 실행 점수에 합산하지 않는다.
- **대표 변경 파일:** [docs/action_protocol.md](https://github.com/apple4ree/evidence-to-action/blob/1617fd23036db364dbcf6707b8fad9b814c317d5/docs/action_protocol.md), [docs/action_scoring.md](https://github.com/apple4ree/evidence-to-action/blob/1617fd23036db364dbcf6707b8fad9b814c317d5/docs/action_scoring.md), [docs/history/README.md](https://github.com/apple4ree/evidence-to-action/blob/1617fd23036db364dbcf6707b8fad9b814c317d5/docs/history/README.md), [docs/history/README_before_current_focus.md](https://github.com/apple4ree/evidence-to-action/blob/1617fd23036db364dbcf6707b8fad9b814c317d5/docs/history/README_before_current_focus.md).

### 3a4bac3 — 사례 중심 README 정리

[원래 커밋과 diff](https://github.com/apple4ree/evidence-to-action/commit/3a4bac36207fc36b7c6dca09d7c0d9e0c5daf0c5) · `docs: align submission README and run guide with public trace results`

- **이유:** 처음 읽는 평가자가 문제, 입력, 진단, 결과와 재현 경로를 따라가게 했다.
- **변경:** README와 docs/real_traces.md를 공개 실행 사례와 현재 결과 중심으로 재작성했다.
- **영향·해석:** 실험이나 채점 변경 없이 문서 구조와 설명을 정리했다.
- **대표 변경 파일:** [README.md](https://github.com/apple4ree/evidence-to-action/blob/3a4bac36207fc36b7c6dca09d7c0d9e0c5daf0c5/README.md), [docs/real_traces.md](https://github.com/apple4ree/evidence-to-action/blob/3a4bac36207fc36b7c6dca09d7c0d9e0c5daf0c5/docs/real_traces.md).

### af7b1d5 — 질문과 채점 범위 보정

[원래 커밋과 diff](https://github.com/apple4ree/evidence-to-action/commit/af7b1d52f129f9ae3740933a6ab0c971c09a2681) · `fix(eval): align two rubrics with public questions and preserve post-hoc rescores`

- **이유:** 두 사례에서 공개 질문보다 넓은 설명을 요구한 채점 요소를 제거했다.
- **변경:** AHN08의 단어 수 출처, AHN09의 검색·읽기 파일 연결 요구를 보정하고 남은 필수 요소를 저장 응답에서 재검토했다. scope_v2에 기준, 원본 hash, 검토 기록과 결과를 분리했다.
- **영향·해석:** 새 추론 없이 세 방법을 동일 기준으로 재채점했다. 전체 진단은 12→14, 13→15, 12→14건. 판정 점수와 사용량은 유지됐다. 평가 후 수행한 보정이다.
- **대표 변경 파일:** [README.md](https://github.com/apple4ree/evidence-to-action/blob/af7b1d52f129f9ae3740933a6ab0c971c09a2681/README.md), [docs/real_traces.md](https://github.com/apple4ree/evidence-to-action/blob/af7b1d52f129f9ae3740933a6ab0c971c09a2681/docs/real_traces.md), [docs/scope_revision.md](https://github.com/apple4ree/evidence-to-action/blob/af7b1d52f129f9ae3740933a6ab0c971c09a2681/docs/scope_revision.md), [real_traces/README.md](https://github.com/apple4ree/evidence-to-action/blob/af7b1d52f129f9ae3740933a6ab0c971c09a2681/real_traces/README.md).

### a04e292 — 검토 주체를 Gemini로 정정

[원래 커밋과 diff](https://github.com/apple4ree/evidence-to-action/commit/a04e292196e1a627ae502753f0f4192c07daf3ca) · `fix(provenance): correct submitted review attribution from human to Gemini`

- **이유:** 사용자가 제출 판정의 주체를 사람에서 Gemini로 정정했다.
- **변경:** README, 실행 안내, 검토 분석·스크립트·출처 기록의 주체를 수정했다. 원래 출처 설명은 superseded_provenance로 보존했다.
- **영향·해석:** 고정 정답과 12/15 일치, D1/D2/P2와 13/15, 12/15, 11/15 일치는 그대로다. 사람 주석 재현성을 측정한 결과가 아니다. Gemini의 정확한 버전과 실행 설정은 미확인이다.
- **대표 변경 파일:** [README.md](https://github.com/apple4ree/evidence-to-action/blob/a04e292196e1a627ae502753f0f4192c07daf3ca/README.md), [docs/real_traces.md](https://github.com/apple4ree/evidence-to-action/blob/a04e292196e1a627ae502753f0f4192c07daf3ca/docs/real_traces.md), [real_traces/corrections/scope_v2/README.md](https://github.com/apple4ree/evidence-to-action/blob/a04e292196e1a627ae502753f0f4192c07daf3ca/real_traces/corrections/scope_v2/README.md), [real_traces/human_review/README.md](https://github.com/apple4ree/evidence-to-action/blob/a04e292196e1a627ae502753f0f4192c07daf3ca/real_traces/human_review/README.md).

### 6fd68b4 — 보고서와 검토 설명 통일

[원래 커밋과 diff](https://github.com/apple4ree/evidence-to-action/commit/6fd68b45bdaf54236ff0f0a6ccdbfafc9e55fe29) · `docs: align review limitations with proposal and fix Gemini wording`

- **이유:** 완료한 LLM 검수와 후속 사람 검증을 일관되게 설명했다.
- **변경:** README의 Gemini 관련 조사 오타를 고치고 후속 검증 문장을 보고서와 맞췄다.
- **영향·해석:** 코드, 입력, 정답, 예측과 점수 변경이 없는 문서 편집이다.
- **대표 변경 파일:** [README.md](https://github.com/apple4ree/evidence-to-action/blob/6fd68b45bdaf54236ff0f0a6ccdbfafc9e55fe29/README.md).

## 결과와 검증 기록을 읽는 방법

| 구분 | 확인할 자료 | 해석 |
|---|---|---|
| 최초 비교 | [원점수](../../real_traces/results/summary.json) | 실행 전 고정된 주석·채점 기준의 저장 결과 |
| 채점 보정 | [보정 설명](../../real_traces/corrections/scope_v2/README.md), [영향](../../real_traces/corrections/scope_v2/impact.json) | 두 범위 오류를 수정한 사후 재채점 |
| 제출 판정 비교 | [Gemini 출처 기록](../../real_traces/human_review/review_provenance.json), [비교](../../real_traces/human_review/comparison.json) | 고정 정답을 대체하지 않은 미조정 보조 비교 |
| 이전 연구 | [과거 실험 안내](README.md) | 현재 15개 행동 결과와 분리된 연구 이력 |

이번 이력 정리에서는 커밋 메시지와 제공된 diff, 변경 파일, 문서 링크를 점검했다. 큰 커밋의 API 파일 목록은 일부만 반환될 수 있어 전체 변경 파일 수를 단정하지 않는다. 과거 테스트 설명은 당시 커밋·검증 기록의 내용이며 이번에 실험이나 테스트를 다시 실행했다는 뜻은 아니다. 새 모델 추론과 점수 변경은 없다.

## 이후 커밋 작성 기준

제목은 `feat`, `fix`, `docs`, `test` 등의 유형과 실제 변경을 적는다. 본문에는 **문제와 이유 → 변경 내용 → 수행한 검증 → 점수·데이터 영향**을 쓴다. 문서만 수정했으면 그 범위를 밝히고, 평가 기준을 수정했으면 변경 전후와 원점수 위치를 연결한다. 정정은 새 커밋으로 남긴다.
