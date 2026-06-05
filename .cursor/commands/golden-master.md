# /golden-master — Golden Master 출력 계약 고정

UnitConverter 프로젝트의 **외부 관찰 가능 출력 계약**을 Golden Master로 고정한다.  
**이 Command는 GREEN PASS 직후, REFACTOR 전에 실행한다.** 리팩토링 중 CLI 출력·오류 메시지·숫자 포맷 회귀를 잡는 안전망이다.

**중요:** Golden Master 대상 시나리오는 Command 안에 고정하지 않는다. PRD / TRACEABILITY / 현재 테스트 상태를 기준으로 후보를 **동적으로 제안**하고, **사용자가 승인한 후보만** Golden Master로 생성 또는 갱신한다.

## 목적

UnitConverter 프로젝트의 외부 관찰 가능 출력 계약을 Golden Master로 고정한다.  
GREEN 구현이 pytest PASS 상태가 된 뒤, REFACTOR 전에 실행한다.  
리팩토링 중 CLI 출력, 오류 메시지, 출력 포맷이 의도치 않게 바뀌는 것을 방지한다.

## 사용 시점

- green 브랜치에서 현재 RED 묶음이 PASS된 직후
- refactoring 브랜치로 넘어가기 전
- 또는 refactoring 브랜치 시작 직후
- **pytest 전체가 PASS 상태일 때만** 실행한다.

보조 참고 (필요 시):

- [.cursor/commands/pytest-check.md](./pytest-check.md)
- [.cursor/commands/green-minimal.md](./green-minimal.md)

## 전제 조건

1. pytest 전체가 PASS여야 한다.
2. 현재 테스트 기대값을 변경하지 않아야 한다.
3. `UnitConverter.py`는 레거시 시드 코드로 유지한다.
4. Golden Master 기준 파일은 수동 편집으로 통과시키지 않는다.
5. 기준 파일 생성 또는 갱신이 필요하면 `UPDATE_GOLDEN=1`을 사용한다.
6. **사용자 승인 없이** Golden Master 파일을 생성/갱신/삭제하지 않는다.

## 입력 컨텍스트

다음 파일·디렉터리를 **읽은 뒤** 작업한다.

1. [docs/PRD.md](../../docs/PRD.md)
2. [docs/TRACEABILITY.md](../../docs/TRACEABILITY.md)
3. [docs/TEST_LOOP.md](../../docs/TEST_LOOP.md)
4. [.cursorrules](../../.cursorrules)
5. [README.md](../../README.md)
6. [.cursor/rules/unit-converter-tdd.mdc](../rules/unit-converter-tdd.mdc)
7. `tests/` — 현재 테스트 목록·출력 관련 테스트
8. `unit_converter/` — CLI 진입점·출력 캡처 경로 파악 (읽기만)

## 사용자 컨텍스트

명령 뒤에 붙은 텍스트(있으면)를 우선 반영한다.

- `GM-01`, `T-CLI-01`, `FR-FMT-01` 등 — 해당 Golden Master 후보·Test ID · PRD ID에 집중
- `갱신`, `UPDATE` — 기존 approved 파일 갱신 의도 (승인·`UPDATE_GOLDEN=1` 필요)
- pytest 출력 붙여넣기 — PASS 여부 확인에 활용
- 비어 있음 — PRD/TRACEABILITY·현재 PASS 테스트 기준으로 후보 전체 제안

## 생성 또는 수정할 수 있는 파일

- `tests/_approval.py`
- `tests/golden/*.approved.txt`
- `tests/test_golden_master.py`

## 수정 금지 파일

- `UnitConverter.py`
- `docs/*`
- `.cursorrules`
- `.cursor/commands/*`
- `unit_converter/*` 의 구현 코드
- 기존 테스트의 기대값

## Golden Master 대상 선정 기준

- PRD/TRACEABILITY에 연결된 Boundary 또는 CLI 출력 계약을 우선한다.
- **현재 pytest가 PASS하는 시나리오만** Golden Master 후보로 삼는다.
- 숫자 변환 결과, 오류 메시지, 출력 포맷처럼 리팩토링 중 깨지기 쉬운 **외부 관찰 결과**를 우선한다.
- Domain 내부 계산만 검증하는 테스트는 Golden Master 대상이 아니라 일반 pytest 대상으로 둔다.
- 후보 시나리오는 먼저 표로 제안하고, **사용자가 승인한 항목만** approved 파일로 생성한다.
- 기존 golden 파일 중 PRD/TRACEABILITY나 테스트에서 더 이상 참조되지 않는 파일은 **stale**로 표시하고 **자동 삭제하지 않는다**.
- 새 테스트가 추가되었지만 Golden Master가 필요한지 불명확하면 **후보로만** 제안한다.
- 의도적인 출력 변경이 있는 경우 `UPDATE_GOLDEN=1` 갱신 전 **변경 이유와 영향 범위**를 먼저 보고한다.

## 작업 절차

1. **pytest 전체를 실행**해 PASS 상태인지 확인한다.
   - PASS가 아니면 **중단**하고 실패 목록만 보고한다.
   - 명령: `pytest tests/ -v`

2. [docs/PRD.md](../../docs/PRD.md)와 [docs/TRACEABILITY.md](../../docs/TRACEABILITY.md)를 읽고 Boundary/CLI 출력 계약 요구사항을 찾는다.

3. `tests/` 하위 테스트 목록을 읽고 현재 출력 관련 테스트를 찾는다.

4. 기존 `tests/golden/*.approved.txt` 파일이 있다면 목록화한다.

5. 다음 표로 **Golden Master 후보를 제안**한다. (시나리오는 PRD/TRACEABILITY/테스트 상태에서 동적으로 도출)

| 후보 ID | 연결 PRD ID | 연결 테스트 ID | 대상 출력 | 추천 이유 | 상태(new/existing/stale) |
|---|---|---|---|---|---|

6. **사용자가 승인한 후보만** Golden Master 테스트와 approved 파일로 생성 또는 갱신한다.

7. `tests/_approval.py`가 없으면 생성한다.
   - `assert_matches_golden(actual: str, relative_path: str)` 함수를 제공한다.
   - `UPDATE_GOLDEN=1` 환경변수가 있을 때 기준 파일을 생성/갱신한다.
   - `UPDATE_GOLDEN`이 없을 때는 `actual`과 approved 파일 내용을 비교한다.
   - 차이가 있으면 unified diff를 보여준다.

8. `tests/test_golden_master.py`를 생성 또는 보완한다.
   - 실제 CLI 또는 CLI 진입 함수의 출력을 캡처한다.
   - 승인된 시나리오의 출력 문자열을 `tests/golden/*.approved.txt`와 비교한다.

9. 기준 파일 생성은 **`UPDATE_GOLDEN=1`일 때만** 수행한다.
   - Windows (PowerShell): `$env:UPDATE_GOLDEN=1; pytest tests/test_golden_master.py -v`
   - Unix: `UPDATE_GOLDEN=1 pytest tests/test_golden_master.py -v`

10. `UPDATE_GOLDEN` 없이 다시 pytest를 실행해 Golden Master가 일치하는지 확인한다.
    - 명령: `pytest tests/ -v`

11. **stale** golden 파일은 삭제하지 말고 보고만 한다.

## 자동 생성 금지

- 후보 제안 없이 approved 파일을 **자동 생성하지 않는다**.
- stale golden 파일을 **자동 삭제하지 않는다**.
- 사용자 승인 없이 `UPDATE_GOLDEN=1`로 기준 파일을 **갱신하지 않는다**.
- 테스트가 변경되었다고 해서 golden 파일을 **자동으로 맞춰 바꾸지 않는다**.
- Golden Master 생성을 위해 **프로덕션 코드를 수정하지 않는다**.

## Golden Master 포맷 규칙

- 출력 문자열의 줄바꿈을 고정한다.
- 숫자 포맷은 PRD 또는 기존 테스트가 정한 기준을 따른다.
- 오류 메시지는 테스트 가능한 고정 문자열로 관리한다.
- 기준 파일을 **수동 편집**해서 테스트를 통과시키지 않는다.
- 의도적으로 출력 계약을 변경해야 할 경우, 변경 이유를 먼저 보고하고 사용자 승인 후 `UPDATE_GOLDEN=1`로 갱신한다.

## 출력 형식

작업 후 다음 표로 요약한다.

| GM ID | 대상 시나리오 | Golden 파일 | 생성/검증 명령 | matched 여부 |
|---|---|---|---|---|

## 중단 조건

- pytest 전체가 PASS가 아니면 **중단**한다.
- CLI 출력 캡처 방법이 불명확하면 **구현 코드를 수정하지 말고 중단**한다.
- Golden Master 생성을 위해 **프로덕션 코드를 수정**해야 하면 **중단**한다.
- **기존 테스트 기대값 변경**이 필요하면 **중단**한다.
- **사용자 승인 없이** approved 파일을 생성/갱신해야 하는 상황이면 **중단**한다.

## ARRR 단계

- **GREEN 직후 · REFACTOR 전** — Golden Master 후보 제안 및 승인된 항목만 생성/검증
- **REFACTOR 중** — `pytest tests/ -v` + Golden Master 일치 확인으로 회귀 감지
- **RED** — 이 Command 사용 대상 아님 (구현·테스트 기대값 변경 금지 원칙과 충돌)
