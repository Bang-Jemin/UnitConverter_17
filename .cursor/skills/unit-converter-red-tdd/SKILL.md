---
name: unit-converter-red-tdd
description: >-
  UnitConverter red 브랜치 RED TDD — PRD·TRACEABILITY 기준 실패 테스트 스켈레톤만
  작성. UnitConverter.py·unit_converter/ 구현 수정 금지. spec 완료 후 GREEN 전까지
  사용.
---

# UnitConverter RED TDD Skill

## 목적

- PRD 요구사항을 테스트 ID로 추적한다.
- RED 단계에서 실패하는 테스트만 작성한다.
- 구현 코드는 작성하지 않는다.
- C2C: PRD → TRACEABILITY → RED Test 연결을 유지한다.

## 사용 시점

- spec 브랜치 완료 후 **red 브랜치**에서 사용한다.
- `docs/PRD.md`, `docs/TRACEABILITY.md`, `.cursorrules`가 존재할 때 사용한다.
- **GREEN 구현 전까지만** 사용한다.

## 입력 컨텍스트

- @docs/PRD.md
- @docs/TRACEABILITY.md
- @.cursorrules
- @README.md
- @UnitConverter.py

보조 참고 (필요 시):

- [docs/TEST_LOOP.md](docs/TEST_LOOP.md) — RED 허용·금지·커밋 형식
- [docs/TRACEABILITY.md](docs/TRACEABILITY.md) — Given / When / Then, P1→P4 순서

## 작업 절차

1. PRD 요구사항 ID를 확인한다.
2. TRACEABILITY에서 테스트 ID(`T-*`)를 확인한다.
3. 테스트 유형을 구분한다.
   - **Boundary**: CLI 입력, 오류 메시지, 출력 포맷 → `tests/test_cli.py`
   - **Domain**: 단위 변환, Registry, Converter → `tests/test_converter.py`
   - **Architecture**: OCP/SRP 구조 검증 → `tests/test_converter.py` (또는 전용 모듈, TRACEABILITY 따름)
   - **Extension**: 설정 파일, 동적 단위 등록, 출력 포맷 → Track은 TRACEABILITY 유형·파일 따름
4. **RED 테스트 스켈레톤만** 작성한다.
5. 테스트 본문에는 아직 **구현 세부사항을 가정하지 않는다**.
6. 필요한 경우 `pytest.fail("RED: [Test-ID] ...")`로 의도된 실패를 표시한다.
7. pytest를 실행해서 실패를 확인한다.

   ```bash
   pytest tests/ -v
   pytest tests/ -v -k "<Test-ID 또는 키워드>"
   ```

8. 실패 결과를 테스트 ID별로 요약한다.
9. **구현 파일은 수정하지 않는다.**

### RED 1건 선택 규칙

- TRACEABILITY **P1 → P2 → P3 → P4** 순서를 따른다.
- **1 RED 묶음 = 1 PRD/Test ID** (여러 요구를 한 테스트에 섞지 않음).
- 테스트 docstring·주석에 `# FR-xx / T-xxxx-xx` 형식으로 PRD ID · Test ID를 기록한다.

### pytest.fail vs assert

- 대상 API·모듈이 **아직 없음** → `pytest.fail("RED: T-PARSE-01 ...")` placeholder 허용.
- import·호출 가능해지면 TRACEABILITY **Then**을 검증하는 **assert 실패**로 전환한다.

## 금지 사항

- `UnitConverter.py` 수정 금지
- `unit_converter/` 내부 **구현 코드** 작성 금지 (Harness 역할 주석 외)
- 테스트를 통과시키는 **프로덕션 코드** 작성 금지
- RED 통과용 stub/fake를 `unit_converter/` 또는 conftest에 두는 행위
- `@pytest.mark.skip`, `@pytest.mark.xfail`, `pytest.skip()` 사용 금지
- assert 기대값을 구현에 맞춰 **약화** 금지
- 여러 요구사항을 **한 테스트에 섞기** 금지
- red 단계에서 **리팩토링** 금지

## 출력 형식

작업 후 다음 형식으로 요약한다.

| 테스트 ID | PRD ID | 파일 | 테스트 유형 | 기대 실패 이유 |
|-----------|--------|------|-------------|----------------|
| | | | Boundary / Domain / Architecture / Extension | |

추가로 보고:

- 실행한 pytest 명령
- PASS / FAIL / ERROR / SKIP 개수 (SKIP > 0 이면 TDD 위반 경고)
- 커밋 제안: `test(RED): <Test-ID> — <PRD-ID> <한 줄 요약>`

## 완료 조건

- [ ] **테스트 파일만** 변경되었다.
- [ ] **구현 파일**(`unit_converter/`, `UnitConverter.py`)은 변경되지 않았다.
- [ ] pytest 실행 시 **의도된 실패**가 발생한다.
- [ ] 각 실패는 **PRD ID**와 연결된다.
- [ ] **1 RED 묶음**은 **1 커밋**으로 분리 가능하다.

## 관련 규칙

- SSOT: [.cursorrules](.cursorrules) — RED 단계 금지·`UnitConverter.py` RED-only 미수정
- Cursor Command: `/red-test-plan`, `/pytest-check`
