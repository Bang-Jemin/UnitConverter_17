# /pytest-check — pytest 결과 요약 및 실패 분류

UnitConverter 프로젝트의 pytest를 실행하고, 결과를 **PASS / FAIL / ERROR**로 요약하며 실패 원인을 분류한다.

## 사용자 컨텍스트

명령 뒤 텍스트(있으면)를 pytest 옵션으로 사용한다.

- 예: `-k CONV`, `tests/test_parser.py`, `-x`
- 비어 있음 → `pytest tests/ -v --tb=short` 실행

## 사전 참고 (읽기)

- [docs/TEST_LOOP.md](../../docs/TEST_LOOP.md) — ARRR 단계별 pytest 기대
- [.cursor/rules/unit-converter-tdd.mdc](../rules/unit-converter-tdd.mdc)

## 수행 절차

1. **환경 확인**
   - 프로젝트 루트에서 실행
   - `tests/` 존재 여부 확인; 없으면 ERROR로 보고하고 종료

2. **pytest 실행**
   ```bash
   pytest tests/ -v --tb=short <사용자_추가_옵션>
   ```
   - 실패 시 exit code를 기록한다.

3. **결과 파싱**
   - passed / failed / error / skipped 개수 추출
   - skipped > 0 이면 **TDD 위반 경고** (skip/xfail 금지)

4. **실패·에러 분류**
   각 실패 테스트에 대해 아래 **원인 카테고리** 중 하나(또는 복합)를 부여:

   | 카테고리 | 설명 | ARRR 해석 |
   |----------|------|-----------|
   | `NOT_IMPLEMENTED` | ImportError, ModuleNotFoundError, AttributeError — 대상 API 미구현 | RED에서 **정상** (의도된 실패) |
   | `ASSERTION` | AssertionError — 기대값과 불일치 | RED: 정상 / GREEN·REFACTOR: **수정 필요** |
   | `RUNTIME` | ValueError, TypeError 등 구현 버그 | GREEN·REFACTOR에서 수정 |
   | `TEST_ERROR` | 테스트 코드 오류, fixture 실패 | 테스트 자체 수정 |
   | `ENVIRONMENT` | pytest 미설치, 경로, venv 문제 | 환경 설정 |
   | `TDD_VIOLATION` | skip, xfail, assert 약화 의심 | 규칙 위반 — 즉시 보고 |

5. **ARRR 단계 추론** (컨텍스트 기반)
   - 대부분 `NOT_IMPLEMENTED` / `ASSERTION` + 구현 없음 → **RED 확인 중**
   - 전부 passed → **GREEN 또는 REFACTOR 완료 후**
   - passed + failed 혼재 → **GREEN 진행 중** 또는 부분 구현

6. **권장 다음 액션** (수정은 사용자 요청 시에만)
   - RED: 실패가 의도된 것인지 TRACEABILITY Test ID와 대조
   - GREEN: 실패 목록만 — 자동 수정하지 않음
   - REFACTOR: 전체 passed 여부 강조

## 출력 형식

```markdown
## pytest-check 결과

### 실행 명령
`<실행한 명령>`

### 요약
| 상태 | 개수 |
|------|------|
| PASS | |
| FAIL | |
| ERROR | |
| SKIP | |

**전체 판정:** PASS / FAIL / ERROR / MIXED

### 상세 (FAIL · ERROR만)
| 테스트 | 상태 | 원인 카테고리 | 핵심 메시지 |
|--------|------|---------------|-------------|
| | FAIL/ERROR | | |

### ARRR 해석
- 추정 단계: RED / GREEN / REFACTOR / 불명
- 근거: (1~2문장)

### TDD 규칙 점검
- [ ] skip/xfail 0건
- [ ] assert 약화 징후 없음

### 권장 다음 단계
1. ...
```

## 금지 (기본 동작)

- 사용자가 명시적으로 요청하지 않는 한 **구현 코드·테스트 코드 자동 수정 금지**
- skip/xfail 추가로 통과시키기 **금지**
- `UnitConverter.py` 무단 수정 **금지**

## 사용자가 "고쳐줘" 요청한 경우

- 현재 ARRR 단계를 먼저 확인
- **RED** 단계면 구현 수정 대신 테스트·계획 검토만 제안
- **GREEN/REFACTOR**만 코드 수정 허용 ([TEST_LOOP.md](../../docs/TEST_LOOP.md) 준수)
