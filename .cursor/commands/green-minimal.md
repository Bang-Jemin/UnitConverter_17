# /green-minimal — GREEN 최소 구현

RED 단계에서 작성된 **현재 실패 테스트**를 통과시키는 **최소 구현만** 작성한다.  
**이 Command는 `unit_converter/` 구현 코드만 수정·생성한다.** 테스트 기대값·문서·레거시 진입점은 변경하지 않는다.

## 목적

의도된 RED 실패를 **PASS**로 만드는 최소 코드만 추가한다.  
설계 완성·리팩터·범위 밖 FR 선행 구현은 하지 않는다.

## 사용 시점

- RED 테스트 스켈레톤 커밋 후, **GREEN 단계**에서 사용한다.
- **red 브랜치**(또는 GREEN 작업 브랜치)에서만 사용한다.
- `/pytest-check`로 현재 실패 목록을 확인한 **직후** 사용한다.

## 입력 컨텍스트

다음 파일·결과를 **읽은 뒤** 작업한다.

1. [docs/PRD.md](../../docs/PRD.md)
2. [docs/TRACEABILITY.md](../../docs/TRACEABILITY.md)
3. [.cursorrules](../../.cursorrules)
4. [docs/TEST_LOOP.md](../../docs/TEST_LOOP.md) — GREEN 단계 허용·금지
5. [.cursor/rules/unit-converter-tdd.mdc](../rules/unit-converter-tdd.mdc)
6. **현재 RED 묶음** — 실패 중인 Test ID · PRD ID (직전 `/red-skeleton` 또는 `/pytest-check` 결과)

보조 참고 (필요 시):

- [.cursor/commands/pytest-check.md](./pytest-check.md)
- [.cursor/commands/red-skeleton.md](./red-skeleton.md)

## 사용자 컨텍스트

명령 뒤에 붙은 텍스트(있으면)를 우선 반영한다.

- `T-CONV-01`, `FR-02` 등 — 해당 Test ID · PRD ID에 집중
- pytest-check 출력 붙여넣기 — 해당 실패만 최소 구현
- 비어 있음 — 직전 대화의 RED 묶음·실패 목록을 사용; 없으면 `/pytest-check` 선행을 요청

## 실행 지시

1. **현재 RED 묶음**의 Test ID · PRD ID · Given / When / Then을 확인한다.
2. 실패 테스트가 요구하는 **공개 API·동작**만 구현한다.
3. **허용 범위** 내에서만 파일을 수정·생성한다.
4. 새 파일이 필요하면 **새 파일 생성 규칙**을 따른다.
5. 단위·비율 추가 시 **OCP 제한**을 위반하지 않는다.
6. pytest를 실행해서 **대상 RED + 기존 테스트 전체 PASS**를 확인한다.

   ```bash
   pytest tests/ -v
   pytest tests/ -v -k "<Test-ID 또는 키워드>"
   ```

7. **테스트 파일·기대값**이 변경되지 않았는지 확인한다 (`git diff tests/`).
8. **수정 금지 파일**이 변경되지 않았는지 확인한다.

### GREEN 1건 규칙

- **1 GREEN 묶음 = 1 RED 묶음**(1 PRD / Test ID) — 현재 실패만 통과시킨다.
- REFACTOR 성격의 구조 변경·이름 정리·중복 제거는 **하지 않는다** (REFACTOR 단계로 미룸).
- Mom Test 상수(`3.28084`, `1.09361` 등)는 **단일 정의**를 유지한다 — 새 위치에 중복 정의 금지.

## 허용 범위

고정 파일명이 아니라 **계층·책임** 기준으로 판단한다. 아래 경로 및 그 하위 파일·폴더를 수정·생성할 수 있다.

| 경로 | 책임 |
|------|------|
| `unit_converter/domain/**/*` | 단위 개념, 단위 등록/조회, 변환 계산, 도메인 예외 |
| `unit_converter/app/**/*` | 입력 파싱, 출력 포맷, CLI 경계 처리 보조 |
| `unit_converter/infrastructure/**/*` | 설정 파일 로드, 외부 설정 파싱 |
| `unit_converter/cli.py` | CLI 진입점 연결 |
| `unit_converter/**/__init__.py` | 패키지 import 연결 |

예시 (허용 — 책임에 부합하면 파일명·하위 폴더는 자유):

- `unit_converter/domain/exceptions.py` — 도메인 예외
- `unit_converter/domain/default_units.py` — 기본 단위 등록
- `unit_converter/app/formatter/json_formatter.py` — JSON 출력
- `unit_converter/infrastructure/yaml_config_loader.py` — 설정 로더

**판단 기준:** 현재 RED 테스트 통과에 필요하고, 위 책임 중 하나에 명확히 속하는가?

## 새 파일 생성 규칙

- **현재 RED 테스트를 통과하는 데 필요한 경우에만** 새 파일을 생성한다.
- 새 파일을 만들 경우, **어떤 Test ID · PRD ID 때문에 필요한지** 작업 요약에 남긴다.
- 미래 확장을 예상한 **빈 추상화·미사용 인터페이스·placeholder 모듈**은 만들지 않는다.
- 현재 RED 묶음과 **무관한** 설정 파일, formatter, 동적 등록 기능은 **미리 구현하지 않는다**.

## OCP 제한

GREEN 단계에서도 OCP 위반 패턴을 **도입하지 않는다**. (REFACTOR에서 고칠 코드를 GREEN에서 넣지 않는다.)

- 새 단위 추가를 위해 **Converter 내부에 `if/elif` 단위 분기**를 늘리지 않는다.
- 새 단위는 **Registry 등록** 또는 **설정 파일 로드** 방식으로 확장 가능해야 한다.
- **Converter 핵심 로직**은 단위 목록을 몰라도 동작하도록 유지한다 (Registry·설정에서 비율을 조회).
- 단위별 변환 비율은 **meter 기준 값**으로 표현한다.
- 출력 포맷 추가는 **Formatter** 책임으로 분리한다 — Converter·Registry 변경 없이 동일 수치 유지.

## 수정 금지

| 대상 | 이유 |
|------|------|
| `UnitConverter.py` | 레거시 시드 — GREEN에서도 수정하지 않음 |
| `docs/*` | spec 산출물 |
| `.cursorrules` | SSOT 규칙 |
| `.cursor/commands/*` | Command 정의 |
| `tests/*` **기대값** | 테스트가 명세; assert·입력·기대 결과 변경 금지 |
| `pyproject.toml` | 프로젝트 메타 — GREEN 범위 밖 |

- `tests/` **fixture·conftest**를 통과 우회용으로 수정하는 행위 금지.
- skip / xfail 추가로 통과시키기 **금지**.

## GREEN 원칙

- **현재 RED 테스트 통과**가 유일한 목적이다.
- **리팩토링 금지** — 동작은 맞지만 구조가 지저분해도 REFACTOR까지 유지한다.
- **추가 요구사항 선구현 금지** — RED·TRACEABILITY에 없는 FR은 넣지 않는다.
- **테스트 기대값 변경 금지** — 구현을 테스트에 맞춘다.
- **`@pytest.mark.skip`**, **`@pytest.mark.xfail`**, **`pytest.skip()`** 사용 금지.
- **assert 약화·삭제·`pytest.approx` 허용 오차 임의 확대** 금지.

## 금지 사항 (요약)

- RED 범위 밖 FR 구현
- REFACTOR (SRP 분리, 중복 제거, rename-only 정리)
- 과도한 추상화, 사용하지 않는 확장 포인트
- Converter `if/elif` 단위 분기 확장
- Mom Test 상수의 새 위치 중복 정의
- 테스트·문서·Command·레거시 진입점 수정

## 출력 형식

작업 후 다음으로 요약한다.

| Test ID | PRD ID | 수정·생성 파일 | 변경 요약 |
|---------|--------|----------------|-----------|
| | | | |

추가로 보고:

- 실행한 pytest 명령
- PASS / FAIL / ERROR / SKIP 개수 (SKIP > 0 이면 TDD 위반 경고)
- **새로 생성한 파일**과 생성 사유(Test ID 연결)
- OCP·SRP 위반 여부 자가 점검 (위반 시 REFACTOR 예약 명시)
- `tests/` · 수정 금지 파일 미변경 확인 결과
- 커밋 제안: `feat(GREEN): <Test-ID> — <PRD-ID> <한 줄 요약>`

## 완료 조건

- [ ] **허용 범위** 내 구현만 변경·생성되었다.
- [ ] **수정 금지** 대상은 변경되지 않았다.
- [ ] **현재 RED 묶음** 테스트가 **PASS**다.
- [ ] `pytest tests/ -v` **전체 PASS** (기존 회귀 없음).
- [ ] skip / xfail 0건.
- [ ] assert 약화 없음.
- [ ] OCP 제한 위반 없음 (또는 위반 시 REFACTOR TODO 명시).
- [ ] **1 GREEN 묶음**은 **1 커밋**으로 분리 가능하다.

## 다음 단계

- 사용자 승인 후 GREEN 커밋
- SRP/OCP 위반·임시 코드 존재 시 → **REFACTOR** 단계
- 구조가 단순하면 → **REPEAT** (다음 `/red-test-plan`)
- 관련 Command: `/pytest-check` (실패 확인) → `/green-minimal` (구현) → `/pytest-check` (전체 PASS 확인)
