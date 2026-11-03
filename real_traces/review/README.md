# 사람 검토 페이지

저장소 루트에서 원본 입력을 복원한 뒤 페이지를 생성합니다.

```sh
python3 real_traces/restore_inputs.py
python3 real_traces/review/build_page.py
node real_traces/review/test_core.cjs
```

생성된 `real_traces/review/review.html`을 브라우저에서 엽니다. 서버는 필요 없습니다.
페이지에는 공개 입력과 `focal_relation`만 포함되며 정답과 모델 예측은 포함하지 않습니다.

기존 실제 실행 15건 페이지와 같은 packet ID, 답변 JSON 규격을 유지합니다. 다른 파일 경로에서 브라우저 자동 저장이 공유되지 않을 수 있으므로 기존 페이지에서 답변을 내보낸 뒤 새 페이지에서 가져오세요. 최초 제출과 수정 이력을 보존합니다.

생성물 `cases.js`, `review.html`, `build_check.json`은 원문을 포함하므로 GitHub 코드 패키지에는 넣지 않습니다. 원본 입력 복원 후 로컬에서 만듭니다.
