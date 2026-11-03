# Real execution trace comparison

원본 실행 14개에서 추출한 국소 행동 15개를 같은 입력으로 직접 진단, 재검토, 단계 분해에 제공한 별도 비교 묶음입니다. 이전 합성 평가와 합산하지 않습니다.

[실행 안내](../docs/real_traces.md)에서 입력 복원, 저장 결과 재채점, 새 추론 작업 폴더 구성과 현재 제약을 확인할 수 있습니다. [집계 결과](results/summary.json), [사례별 결과](results/per_case.csv), [고정 채점 규격](scoring_spec.md)을 함께 제공합니다.

```sh
python3 real_traces/restore_inputs.py
python3 real_traces/harness.py verify
python3 real_traces/evaluate.py
```

전체 원본 로그는 포함하지 않습니다. `input_recipes.json`의 revision 고정 URL에서 원본을 받아 hash를 검사하고, 원래 사용한 입력을 정확히 복원합니다. 원문에 등장하는 계정, 비밀번호와 토큰 문자열은 공개 벤치마크의 실행 기록에서 온 값입니다.
