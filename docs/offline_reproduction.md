# 원본 캐시를 이용한 오프라인 재현

오프라인 재현은 **제출 코드와 저장 응답, 원본 캐시 14개**가 필요하다. 캐시는 저장소에 포함되지 않는다. 캐시 없이 `--offline`을 실행하면 누락된 파일을 명시하며 중단한다.

## 1. 캐시 준비

네트워크가 연결된 컴퓨터에서 저장소를 받은 뒤 다음을 실행한다.

```sh
python3 real_traces/restore_inputs.py --cache ./eta-source-cache
```

원본은 `input_recipes.json`의 고정 revision에서 가져오며 SHA-256과, 명시된 경우 Git blob hash를 검사한다. 같은 원본을 쓰는 두 행동이 있어 15개 행동에 필요한 원본은 14개다. 캐시 파일명은 확장자 없는 SHA-256이다. 임의로 파일 이름이나 줄바꿈을 변경하지 않는다.

완료된 `eta-source-cache/`와 저장소를 오프라인 컴퓨터로 복사한다. 원본별 이용 조건은 upstream 저장소를 따른다. 원본 다운로드가 막힌 환경에서는 먼저 네트워크 가능한 환경에서 이 준비를 완료해야 한다.

## 2. 오프라인 실행

Python 3.10 이상과 표준 라이브러리를 사용한다. 저장소 루트에서 실행하며, 캐시 경로는 실제 복사한 위치로 바꾼다.

```sh
python3 real_traces/restore_inputs.py --cache ./eta-source-cache --offline
python3 real_traces/harness.py verify
python3 real_traces/evaluate.py
python3 real_traces/rescore_scope.py
python3 real_traces/test_harness.py
python3 real_traces/test_restore.py
python3 real_traces/test_scope_correction.py
```

입력 15개와 보존 요청 60개를 복원한다. 재검토와 관계 판단의 요청은 저장된 이전 단계 응답을 사용한다. 이 과정은 새 모델 호출이 아니라 **저장 실행의 재구성과 재채점**이다. 원점수는 `real_traces/results/`, 보정 결과는 `real_traces/corrections/scope_v2/results/`에 기록된다.

## 3. 깨끗한 환경 검증 결과

- 새 임시 폴더에 공개 파일 목록에 포함된 제출 파일만 복사했다. `public/`과 `requests/`는 시작 시 없었다.
- pip 없는 새 가상환경과 `-S` 옵션으로 외부 패키지와 기존 Python 설정을 제외했다.
- 별도 폴더에 hash를 확인한 원본 캐시 14개만 제공했다.
- Python audit hook으로 DNS 조회와 소켓 연결을 차단했다.
- 입력 15개, 요청 60개 복원과 고정 파일 검증을 통과했다.
- 원점수와 보정 결과 모두 기존 JSON과 일치했고 테스트 7개가 통과했다.

[명령별 출력과 환경 기록](offline_validation.json)을 보존했다. 이 검증은 로컬 공개 파일 사본과 원본 캐시를 사용했다. 네트워크를 통한 새 clone, 최초 원본 다운로드와 새 모델 추론은 이번 검증 범위 밖이다.
