# 커밋 메시지 한국어 번역

번역 기준: `112de3a`까지의 기존 커밋 16개. 각 제목과 본문 전체를 번역했다. 원래 커밋의 SHA, 시각과 변경 파일은 유지하며, GitHub 커밋 화면의 영문 메시지는 아래 원문 링크에서 확인할 수 있다. 이후 번역 문서 추가 커밋은 한국어로 작성한다.

과거 메시지는 당시 상태를 설명한다. 특히 단일 검토자로 기록한 판정의 주체는 이후 Gemini로 정정됐다. 최신 구현과 결과는 [README](../../README.md)를 따른다. [변경 이유와 결과 영향 해설](commits.md)

## 6616813 — 저장소 초기화

[원래 커밋과 변경 내역](https://github.com/apple4ree/evidence-to-action/commit/66168133b7adcf5180808ed4ed6f7463a95c0227)

원래 커밋에는 별도 본문이 없다.

<details>
<summary>영문 원문</summary>

Initial commit

</details>

## 543d5bb — 기능: 행동 및 출처 진단 파이프라인 추가

[원래 커밋과 변경 내역](https://github.com/apple4ree/evidence-to-action/commit/543d5bbb6c53705ae665d806ec0ae4fef236155e)

기존 D1/D2/P2 작업 흐름, 프롬프트, 실행 도구와 경계 테스트를 보존한다. 모델의 의미 판단을 참조 검사 및 결정적 라벨 합성과 분리한다.

<details>
<summary>영문 원문</summary>

feat: add action and provenance diagnostic pipelines

Preserve the existing D1/D2/P2 workflow, prompts, harnesses and boundary tests. Separate semantic model judgments from reference checks and deterministic label synthesis.

</details>

## cd31964 — 기능: 고정 평가 자료와 재현 가능한 채점 코드 구성

[원래 커밋과 변경 내역](https://github.com/apple4ree/evidence-to-action/commit/cd319644c9cda0944073cedb2eb80b5b1b1b18e9)

합성 자료 생성기, 96개 사례의 고정 자료 묶음, 저장 진단 출력과 의미 채점을 추가한다. 재채점은 원본 hash를 검사하고 새 모델 호출 없이 72개 사례의 점수를 재현한다. 원점수와 사후 민감도 분석은 별도로 보존한다.

<details>
<summary>영문 원문</summary>

feat: package frozen evaluation and reproducible scoring

Add the synthetic authoring generator, 96-case frozen archive, saved diagnostic outputs and semantic ratings. Replay checks original hashes and reproduces the 72-case scoring without new model calls. Preserve primary scores and post-hoc sensitivity separately.

</details>

## f72aea7 — 문서: 제출 범위, 재현 방법과 검증 결과 정리

[원래 커밋과 변경 내역](https://github.com/apple4ree/evidence-to-action/commit/f72aea76e9b46f082875e1c9dcfd825efba8f098)

한국어 빠른 시작 안내, 원본 대응표, 채점 규격과 완료한 점검을 추가한다. 직접 진단 선택, 행동과 경로의 개별 과제, 모델 접근 제약, 재채점과 새 추론의 차이를 설명한다. 연구 이력의 날짜를 소급하지 않고 제출 커밋을 기록한다.

<details>
<summary>영문 원문</summary>

docs: document submission scope, reproduction and verified results

Add Korean quickstart, source mapping, scoring specifications and completed checks. Explain direct-judge selection, distinct action/path tasks, model-access limitations and the difference between replay and new inference. Record submission commits without backdating research history.

</details>

## 2efabbd — 수정: 제출 CSV의 원본 바이트 보존

[원래 커밋과 변경 내역](https://github.com/apple4ree/evidence-to-action/commit/2efabbdaf561993cbab0abb020774e02c0ffb4ab)

공개 파일이 source_map.json과 일치하도록 내보낸 CSV의 줄바꿈을 원본대로 유지한다. 데이터 값과 점수는 변경하지 않는다.

<details>
<summary>영문 원문</summary>

fix: preserve original CSV bytes in the submission

Keep the exported CSV line endings unchanged so its published blob matches source_map.json. No data values or scores change.

</details>

## b90305e — 문서: 현재 프로토콜과 새 추론 실행 흐름 명확화

[원래 커밋과 변경 내역](https://github.com/apple4ree/evidence-to-action/commit/b90305e1d2cda2fc5c7fc483395339c50f386410)

실험 전 프로토콜을 보존하고, 새 작업 폴더에 고정 자료를 준비하는 방법과 네 단계 실행 명령을 설명한다. 저장된 입출력 예시와 측정 결과 요약을 추가한다.

경계 테스트 20개, 테스트 자료를 이용한 요청 준비와 저장 흐름, 고정 파일 hash, 덮어쓰기 거부, 상대 링크를 검증한다. 새 모델 추론은 수행하지 않는다.

<details>
<summary>영문 원문</summary>

docs: clarify current protocol and fresh inference workflow

Preserve pretest protocol, document clean frozen workspace setup and four-stage commands, and add saved input/output example with measured result summary.

Validate 20 boundary tests, fixture-based prepare/save flow, freeze hashes, overwrite refusal, and relative links. No new model inference.

</details>

## 79e043f — 기능: 실제 Agent 실행에서 추출한 15개 행동 평가

[원래 커밋과 변경 내역](https://github.com/apple4ree/evidence-to-action/commit/79e043fb8e8eaf49917fef7dd0f207970f1bfecb)

고정 원본 기반 입력 복원, 고정 주석과 프롬프트, 완료한 native 단계 60개, 저장 진단 45개, 방법 이름을 가린 의미 채점과 출처 및 그룹별 결과를 추가한다. 이전 합성 및 출처 평가 결과를 보존한다.

관측 판정 점수는 직접 진단 14/15, 재검토 15/15, 단계 분해 14/15다. 전체 진단 원점수를 유지하고 두 공통 입력 및 채점 범위 불일치를 공개한다. 정답을 숨긴 사람 검토 페이지 생성기를 포함하며 사람 검증은 후속 작업으로 남긴다.

입력 15개와 요청 60개의 hash, 경계 및 복원 테스트를 확인하고 저장 예측을 재채점한다. 일반적인 성능 우위나 사람 주석 일치도를 주장하지 않는다.

<details>
<summary>영문 원문</summary>

feat: evaluate 15 actions extracted from real agent traces

Add pinned-source input reconstruction, frozen annotations and prompts, 60 completed native stages, 45 saved diagnoses, blinded semantic ratings and source/group breakdowns. Preserve previous synthetic and provenance results.

Observed decision scores: direct 14/15, revision 15/15, decomposition 14/15. Keep original joint scores and disclose two shared input/rubric scope mismatches. Include a gold-hidden human review page generator; human validation remains pending.

Validate 15 input and 60 request hashes, boundary and reconstruction tests, and replay saved predictions. No claim of general superiority or human annotation agreement.

</details>

## 52bbdea — 문서: 원본 선정 기록 보존과 검증 범위 설명

[원래 커밋과 변경 내역](https://github.com/apple4ree/evidence-to-action/commit/52bbdeacb3ed721a3a4faf62dbd63f0935a419d2)

수집 시점의 포함 및 제외 기록과 최종 엄격성 검토의 조정 내용을 공개한다. 고정 정답이나 실험 점수를 변경하지 않고, 오프라인 복원 점검과 제한된 네트워크 및 브라우저 검증 범위를 명확히 한다.

<details>
<summary>영문 원문</summary>

docs: preserve source screening and document verification limits

Publish collection-time inclusion/exclusion records and final rigor-review resolutions. Clarify offline reconstruction checks and restricted-network/browser verification limits without changing frozen gold or experiment scores.

</details>

## 4e02240 — 문서: 단일 검토자의 주석 반영과 고정 점수 보존

[원래 커밋과 변경 내역](https://github.com/apple4ree/evidence-to-action/commit/4e02240dc8f087514407d1035d2bf823d5674492)

원래 커밋에는 별도 본문이 없다.

<details>
<summary>영문 원문</summary>

docs: incorporate single-reviewer annotations and preserve frozen scores

</details>

## 1617fd2 — 문서: 과거 실험을 현재 벤치마크와 분리

[원래 커밋과 변경 내역](https://github.com/apple4ree/evidence-to-action/commit/1617fd23036db364dbcf6707b8fad9b814c317d5)

원래 커밋에는 별도 본문이 없다.

<details>
<summary>영문 원문</summary>

docs: separate historical experiments from the current benchmark

</details>

## 3a4bac3 — 문서: 제출 README와 실행 안내를 공개 실행 결과에 맞춰 정리

[원래 커밋과 변경 내역](https://github.com/apple4ree/evidence-to-action/commit/3a4bac36207fc36b7c6dca09d7c0d9e0c5daf0c5)

원래 커밋에는 별도 본문이 없다.

<details>
<summary>영문 원문</summary>

docs: align submission README and run guide with public trace results

</details>

## af7b1d5 — 평가 수정: 두 채점 기준을 공개 질문에 맞추고 사후 재채점 결과 보존

[원래 커밋과 변경 내역](https://github.com/apple4ree/evidence-to-action/commit/af7b1d52f129f9ae3740933a6ab0c971c09a2681)

원래 커밋에는 별도 본문이 없다.

<details>
<summary>영문 원문</summary>

fix(eval): align two rubrics with public questions and preserve post-hoc rescores

</details>

## a04e292 — 출처 수정: 제출 검토의 주체를 사람에서 Gemini로 정정

[원래 커밋과 변경 내역](https://github.com/apple4ree/evidence-to-action/commit/a04e292196e1a627ae502753f0f4192c07daf3ca)

원래 커밋에는 별도 본문이 없다.

<details>
<summary>영문 원문</summary>

fix(provenance): correct submitted review attribution from human to Gemini

</details>

## 6fd68b4 — 문서: 검토 한계를 제안서와 통일하고 Gemini 표현 수정

[원래 커밋과 변경 내역](https://github.com/apple4ree/evidence-to-action/commit/6fd68b45bdaf54236ff0f0a6ccdbfafc9e55fe29)

원래 커밋에는 별도 본문이 없다.

<details>
<summary>영문 원문</summary>

docs: align review limitations with proposal and fix Gemini wording

</details>

## 3d9a314 — 문서: 제출 커밋 이력 설명과 평가 보정 자료 연결

[원래 커밋과 변경 내역](https://github.com/apple4ree/evidence-to-action/commit/3d9a31450a78bc1f8f848b4485c5fe57b1d687c8)

이유: 최근 커밋 일부에는 제목만 있어 구현에서 공개 실행 평가와 보정으로 이어지는 과정을 파악하기 어려웠다.

변경: 기존 커밋 14개에 원래 링크, 한국 시간 기준 순서, 변경 이유, 대표 파일과 결과 영향을 정리한 사후 안내를 추가한다. 최초 제출 검토의 주체 표기를 Gemini 정정과 연결하고, 원점수와 채점 범위 사후 재채점을 구분한다. README와 이력 색인에 안내 링크를 추가한다.

검증: 커밋 메시지와 반환된 변경 내역 및 파일 목록을 확인하고, 안내 항목 14개와 상대 링크를 검증했다. 과거 테스트 설명은 당시 기록을 근거로 하며 이번 문서 변경에서 실험이나 테스트 묶음을 재실행하지 않았다.

영향: 문서만 변경한다. 코드, 데이터, 예측과 점수는 그대로이며 원래 커밋 메시지와 시각을 보존한다.

<details>
<summary>영문 원문</summary>

docs: explain submission commit history and link evaluation corrections

Why: several recent commits have subject-only messages, making the progression from implementation to real-trace evaluation and corrections difficult to follow.

Changes: add a retrospective guide for 14 existing commits with original links, Korean-time chronology, rationale, representative files and result impact. Connect the initial submitted-review attribution to its Gemini correction and distinguish original scores from post-hoc scope rescores. Link the guide from README and the history index.

Validation: inspected commit messages and returned diffs/file lists; verified all 14 guide entries and relative links. Historical test statements are attributed to their original records; no experiments or test suites were rerun for this documentation change.

Impact: documentation only. Code, data, predictions and scores are unchanged. Preserve original commit messages and timestamps.

</details>

## 112de3a — 문서: 깨끗한 환경의 오프라인 재채점 검증과 Gemini 실행 정보 기록

[원래 커밋과 변경 내역](https://github.com/apple4ree/evidence-to-action/commit/112de3aaa08656a23d7dc58a8c5944a4034803a9)

이유: 제출물 검토자가 필요한 캐시를 명확히 알고, 생성 입력이나 설치된 의존성 없이 오프라인 복원이 작동함을 확인할 수 있어야 한다.

검증: 공개 파일 목록에 따라 새 임시 작업공간에 파일을 복사하고 pip 없는 가상환경을 만들었다. 외부 패키지를 비활성화하고 Python의 DNS 및 소켓 연결을 차단했다. hash를 확인한 원본 캐시 14개로 입력 15개와 요청 60개를 복원했다. 고정 파일 검사와 테스트 7개를 통과했고 원점수 및 보정 요약 JSON을 정확히 재현했다. 네트워크 clone, 온라인 원본 다운로드와 새 모델 추론은 수행하지 않았다.

변경: 명령 실행 기록, 캐시 준비 및 오프라인 실행 안내를 공개하고 README와 실행 안내를 수정한다. 사용자가 제공한 Gemini 식별자와 유일한 프롬프트를 실행 메타데이터로 기록한다. 판정 변경이나 엄격성 향상 주장은 추가하지 않는다.

영향: 문서와 검토 출처만 변경한다. 고정 정답, 예측과 수치 결과는 그대로다.

<details>
<summary>영문 원문</summary>

docs: verify clean offline replay and record Gemini execution details

Why: submission reviewers need an explicit cache prerequisite and evidence that offline reconstruction works without generated inputs or installed dependencies.

Validation: copied published-file manifest into a fresh temporary workspace, created a venv without pip, disabled site packages and blocked Python DNS/socket connections. Supplied 14 hash-verified source cache files; restored 15 inputs and 60 requests, passed freeze verification and seven tests, and reproduced original and corrected summary JSON exactly. No network clone, online source download or new model inference was run.

Changes: publish command logs and cache preparation/offline instructions; update README and run guide. Record the user-reported Gemini identifier and sole supplied prompt as execution metadata, without changing judgments or claiming increased rigor.

Impact: documentation and review provenance only. Frozen gold, predictions and numerical results remain unchanged.

</details>

