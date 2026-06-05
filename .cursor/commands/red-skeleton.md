# /red-skeleton — RED 테스트 스켈레톤 작성

`/red-test-plan`에서 확정한 테스트 계획을 바탕으로 **RED 단계에서 실패하는 pytest 테스트 스켈레톤만** 작성한다.  
**이 Command는 `tests/` 테스트 파일만 수정한다.** 구현 코드는 작성·수정하지 않는다.

## 목적

확정된 RED 테스트 계획을 실제 pytest 테스트 파일에 반영한다.  
구현 코드는 작성하지 않고, 실패하는 테스트 스켈레톤만 작성한다.

## 사용 시점

- `/red-test-plan`으로 이번 RED 묶음이 확정된 뒤 사용한다.
- **red 브랜치**에서만 사용한다.
- **GREEN 구현 전까지만** 사용한다.

## 입력 컨텍스트

다음 파일·결과를 **읽은 뒤** 작업한다.

1. [docs/PRD.md](../../docs/PRD.md)
2. [docs/TRACEABILITY.md](../../docs/TRACEABILITY.md)
3. [.cursorrules](../../.cursorrules)
4. [.cursor/commands/red-test-plan.md](./red-test-plan.md)
5. **red-test-plan 결과** — 사용자가 붙인 계획 출력 또는 직전 `/red-test-plan` 답변

보조 참고 (필요 시):

- [docs/TEST_LOOP.md](../../docs/TEST_LOOP.md) — RED 단계 허용·금지
- [.cursor/rules/unit-converter-tdd.mdc](../rules/unit-converter-tdd.mdc)
- [.cursor/skills/unit-converter-red-tdd/SKILL.md](../skills/unit-converter-red-tdd/SKILL.md)

## 사용자 컨텍스트

명령 뒤에 붙은 텍스트(있으면)를 우선 반영한다.

- `T-CONV-01`, `FR-02` 등 — 해당 Test ID · PRD ID에 집중
- red-test-plan 출력 붙여넣기 — 해당 계획을 그대로 스켈레톤으로 변환
- 비어 있음 — 직전 대화의 red-test-plan 결과를 사용; 없으면 `/red-test-plan` 선행을 요청

## 실행 지시

1. **red-test-plan 결과에서** 테스트 ID, PRD ID, Track, Given / When / Then을 확인한다.
2. **Track B / Domain** 테스트는 `tests/test_converter.py`에 작성한다.
3. **Track A / Boundary** 테스트는 `tests/test_cli.py`에 작성한다.
4. 각 테스트 함수에는 **테스트 ID**와 **PRD ID**를 주석 또는 docstring으로 남긴다.
   - 형식 예: `# FR-CONV-01 / T-CONV-01` 또는 docstring 첫 줄
5. 아직 구현이 없으므로 **의도된 실패**가 발생하도록 작성한다.
6. 필요한 경우 `pytest.fail("RED: [Test ID] ...")`를 사용한다.
   - 대상 API·모듈이 아직 없음 → `pytest.fail` placeholder 허용
   - import·호출 가능해지면 TRACEABILITY **Then**을 검증하는 **assert 실패**로 작성
7. pytest를 실행해서 **FAIL / ERROR** 상태를 확인한다.

   ```bash
   pytest tests/ -v
   pytest tests/ -v -k "<Test-ID 또는 키워드>"
   ```

8. 실패 결과를 **테스트 ID별**로 요약한다.
9. **구현 파일이 수정되지 않았는지** 확인한다 (`git diff` 또는 변경 파일 목록 점검).

### Track → 파일 매핑

| Track | 테스트 유형 | 파일 |
|-------|-------------|------|
| Track A | Boundary (CLI 입력, 오류 메시지, 출력 포맷) | `tests/test_cli.py` |
| Track B | Domain (단위 변환, Registry, Converter) | `tests/test_converter.py` |

Architecture / Extension 유형은 TRACEABILITY 배치 제안을 따른다. 기본은 위 두 파일 중 하나.

### RED 1건 규칙

- TRACEABILITY **P1 → P2 → P3 → P4** 순서를 따른다.
- **1 RED 묶음 = 1 PRD / Test ID** — 계획에 없는 테스트 추가 금지
- 여러 요구를 한 테스트 함수에 섞지 않는다.

## 허용 파일

- `tests/test_converter.py`
- `tests/test_cli.py`

## 수정 금지 파일

- `UnitConverter.py`
- `unit_converter/domain/*.py`
- `unit_converter/app/*.py`
- `unit_converter/infrastructure/*.py`
- `unit_converter/cli.py`
- `docs/*`
- `.cursorrules`
- `pyproject.toml`

## 금지 사항

- 구현 코드 작성 금지
- GREEN 구현 금지
- REFACTOR 금지
- `@pytest.mark.skip`, `@pytest.mark.xfail`, `pytest.skip()` 사용 금지
- assert 기대값 약화 금지
- 테스트를 통과시키기 위한 프로덕션 코드 작성 금지
- RED 통과용 stub / fake를 `unit_converter/` 또는 conftest에 두는 행위
- **계획에 없는 테스트 추가** 금지

## 출력 형식

작업 후 다음 표로 요약한다.

| 테스트 ID | PRD ID | Track | 파일 | Expected RED Failure | 상태 |
|---|---|---|---|---|---|
| | | | | | |

추가로 보고:

- 실행한 pytest 명령
- PASS / FAIL / ERROR / SKIP 개수 (SKIP > 0 이면 TDD 위반 경고)
- 구현 파일 미변경 확인 결과
- 커밋 제안: `test(RED): <Test-ID> — <PRD-ID> <한 줄 요약>`

## 완료 조건

- [ ] **테스트 파일만** 변경되었다.
- [ ] **구현 파일**은 변경되지 않았다.
- [ ] pytest 실행 결과가 **FAIL** 또는 **ERROR**다.
- [ ] 실패는 **의도된 RED**다.
- [ ] 각 테스트는 **PRD ID**와 연결된다.
- [ ] skip / xfail 0건
- [ ] **1 RED 묶음**은 **1 커밋**으로 분리 가능하다.

## 다음 단계

- 사용자 승인 후 RED 커밋
- GREEN 단계: `/pytest-check`로 실패 목록 확인 → 구현 진행
- 관련 Command: `/red-test-plan` (계획) → `/red-skeleton` (스켈레톤) → `/pytest-check` (결과 검증)
