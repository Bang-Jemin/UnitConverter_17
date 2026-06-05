# /refactor-safe — 선택 스멜 1건 안전 리팩토링

`/refactor-smell` 결과에서 **사용자가 명시적으로 선택한 스멜 1개**만 안전하게 리팩토링한다.

리팩토링의 목적은 기능 추가나 버그 수정이 아니라, **현재 GREEN 상태의 외부 동작을 그대로 유지**하면서 내부 구조만 개선하는 것이다.

| 항목 | 값 |
|------|-----|
| Phase | REFACTOR (Refine) |
| Mode | Agent |
| Scope | `unit_converter/` (수정), `tests/` (검증만) |
| Track | Logic + UI |
| ARRR | **Refine** — 구조 개선, 관측 동작 동일 |

보조 참고:

- [.cursor/commands/refactor-smell.md](./refactor-smell.md) — 선행 스멜 분석·후보 ID
- [docs/TEST_LOOP.md](../../docs/TEST_LOOP.md) — REFACTOR 허용·금지
- [.cursor/rules/unit-converter-tdd.mdc](../rules/unit-converter-tdd.mdc) — SRP·OCP
- [.cursorrules](../../.cursorrules) — 계층·import 방향
- [.cursor/commands/golden-master.md](./golden-master.md) — 출력 계약 보호
- [.cursor/commands/pytest-check.md](./pytest-check.md) — PASS/FAIL 판정

## 사용 시점

- **GREEN** 단계가 완료되어 `pytest` 전체가 PASS인 상태
- **Golden Master**가 생성되어 matched 상태 (존재 시)
- **refactoring** 브랜치에서 작업 중인 상태
- `/refactor-smell` 실행 결과가 있고, 사용자가 리팩토링 후보 **1개를 명시적으로 선택**한 상태

선행 순서: `/refactor-smell` → 후보 선택 → `/refactor-safe RS-01` (또는 스멜·위치 지정)

## 입력 컨텍스트

다음을 **읽은 뒤** 작업한다.

1. [docs/PRD.md](../../docs/PRD.md) — NFR-01(OCP), NFR-02(SRP), NFR-03(비율 SSOT), NFR-06
2. [docs/TRACEABILITY.md](../../docs/TRACEABILITY.md) — `T-ARCH-SRP-01`, `T-ARCH-OCP-01`
3. [docs/TEST_LOOP.md](../../docs/TEST_LOOP.md) — REFACTOR 단계 규칙
4. [.cursorrules](../../.cursorrules)
5. `tests/` — 보호 테스트·아키텍처 테스트 (기대값 변경 금지)
6. `tests/test_golden_master.py`, `tests/golden/` — 출력 계약 (approved 수정 금지)
7. `unit_converter/` — 리팩터 대상
8. **직전 `/refactor-smell` 결과** — 선택한 후보 ID·스멜·위치·Change Budget 내 후보 설명

## 사용자 컨텍스트

명령 뒤에 붙은 텍스트를 **필수**로 해석한다. 비어 있으면 작업을 시작하지 말고 후보 선택을 요청한다.

| 입력 예 | 의미 |
|---------|------|
| `RS-01` | refactor-smell 후보 ID 1건 적용 |
| `SRP cli` | CLI SRP 분리 스멜 1건 (위치 명시 시 해당 위치만) |
| `NFR-03 magic` | 비율 SSOT·Magic Number 스멜 1건 |
| `P0` + 위치 | 해당 우선순위·파일의 스멜 1건만 |

- **한 번에 하나만** — 여러 `RS-XX` 또는 복수 스멜 동시 지정 시 **첫 1건만** 수행하고 나머지는 다음 사이클로 안내
- refactor-smell 결과 없이 임의 대규모 리팩터 **금지**

## 전제 확인

작업 시작 **전에** 반드시 아래 명령을 실행한다.

```bash
python -m pytest tests/ -v
```

- **전부 PASS가 아니면 중단**하고 실패 목록만 보고한다.
- PASS가 아니면 리팩토링을 **시작하지 않는다**.

Golden Master 테스트가 존재하면 아래도 실행한다.

```bash
python -m pytest tests/test_golden_master.py -v
```

- Golden Master가 **FAIL**이면 중단한다. `UPDATE_GOLDEN=1`로 approved를 맞추지 **않는다**.
- 리팩터 목적이 출력 변경이 아니므로, Golden Master FAIL은 **구현 회귀**로 간주하고 원인만 보고한다.

## Change Budget

**이번 1회 리팩터**는 아래 예산을 **초과하지 않는다**. 초과가 예상되면 구현 전에 중단하고 범위 축소안을 제안한다.

| 항목 | 한도 |
|------|------|
| 수정 파일 | ≤ 3 |
| 신규 클래스 | ≤ 1 |
| 신규 메서드 | ≤ 3 |
| 외부 동작 | 변경 금지 |
| 테스트 기대값 | 변경 금지 |
| Golden Master approved | 변경 금지 |

## 허용 범위

| 경로 | 허용 |
|------|------|
| `unit_converter/domain/**/*` | SRP/OCP 정렬, Registry·Converter 구조 개선 |
| `unit_converter/app/**/*` | Parser·Formatter 분리, 검증 경계 정리 |
| `unit_converter/infrastructure/**/*` | 설정 로드 책임 정리 (변환·포맷 로직 이전 금지) |
| `unit_converter/cli.py` | 조율만 남기기 — 파싱·변환·포맷 위임 |
| `unit_converter/**/__init__.py` | import 경로 정리 |

**판단 기준:** 선택한 스멜 1건 해소에 필요하고, 계층 책임에 부합하는 최소 diff인가?

## 수정 금지

| 대상 | 이유 |
|------|------|
| `UnitConverter.py` | 레거시 시드 |
| `tests/*` **기대값** | 명세 고정 — assert·입력·기대 결과 변경 금지 |
| `tests/golden/*.approved.txt` | Golden Master 계약 — 리팩터로 갱신 금지 |
| `docs/*`, `README.md` | spec 산출물 |
| `.cursorrules`, `.cursor/commands/*` | SSOT·Command 정의 |
| `pyproject.toml` | REFACTOR 범위 밖 |

- skip / xfail / assert 약화로 통과 우회 **금지**
- `UPDATE_GOLDEN=1` 실행 **금지** (출력이 바뀌었다면 리팩터 실패로 롤백)
- 새 FR 기능 추가 **금지** (→ REPEAT 후 RED)
- **2건 이상** 스멜을 한 세션에 적용 **금지**

## UnitConverter 계층 기준 (리팩터 후 검증)

| 계층 | 책임 | 금지 |
|------|------|------|
| `unit_converter/domain/` | 단위, Registry, 변환 계산 | `app`, `infrastructure`, `cli` import |
| `unit_converter/app/` | 파싱, 포맷, 사용자 경계 | 변환 계산 직접 수행 |
| `unit_converter/infrastructure/` | 설정 로드 | 변환·포맷 직접 수행 |
| `unit_converter/cli.py` | 진입점·흐름 조립 | 비즈니스 로직 직접 보유 |

리팩터 후 import 방향 위반이 없어야 한다. `T-ARCH-SRP-01`, `T-ARCH-OCP-01`이 존재하면 해당 테스트도 PASS를 유지한다.

## 수행 절차

1. **선택 확인** — 사용자가 지정한 `RS-XX` 또는 스멜 1건을 refactor-smell 결과와 대조해 범위를 확정한다.
2. **전제 확인** — `pytest tests/ -v` (+ Golden Master) PASS; 아니면 중단.
3. **보호 테스트 식별** — refactor-smell 후보 표의 「보호 테스트」·관련 `pytest -k` 키워드를 기록한다.
4. **최소 리팩터** — Change Budget 내에서 선택 스멜 1건만 해소하는 구조 변경을 적용한다.
5. **예산 자가 점검** — 수정 파일·신규 클래스·신규 메서드 수가 한도 이내인지 확인한다.
6. **사후 검증** — 아래 명령을 **반드시** 실행한다.

   ```bash
   python -m pytest tests/ -v
   python -m pytest tests/test_golden_master.py -v
   ```

   refactor-smell에 명시된 보호 테스트가 있으면 추가 실행:

   ```bash
   python -m pytest tests/ -v -k "<보호 키워드>"
   ```

7. **diff 검증** — `tests/`·`tests/golden/`·수정 금지 파일이 변경되지 않았는지 확인 (`git diff`).
8. **결과 보고** — 출력 형식에 따라 요약; FAIL 시 변경 롤백 또는 원인 보고 (approved 갱신으로 우회 금지).

### 리팩터 유형별 가이드 (1건당)

| 스멜 | 허용 방향 | 금지 |
|------|-----------|------|
| SRP 위반 | Extract Method/Class, CLI→app/domain 위임 | 동작·메시지·출력 문자열 변경 |
| OCP 위반 | Registry SSOT, Converter 분기 축소 | 새 단위 FR 선행 추가 |
| Magic Number | 리터럴을 Registry(또는 SSOT)로 이동 | 비율 값 자체 변경 |
| Duplicated Code | 공통 함수·모듈로 추출 | 검증 규칙·오류 조건 변경 |
| Feature Envy | 로직을 domain으로 이동 | app/cli에 변환식 잔류 |
| Long Method | 책임별 분리 | public API 시그니처 무분별 변경 |
| Mysterious Name | rename-only (동작 동일) | 의미 바뀌는 rename |
| 계층 위반 | import·호출 방향 수정 | domain이 상위 계층 참조 |

## 출력 형식

작업 후 **한국어**로 다음을 보고한다.

### 1. 적용 요약

| 항목 | 값 |
|------|-----|
| 선택 후보 | RS-XX 또는 스멜명 |
| 대상 스멜 | Long Method / SRP / … |
| PRD·NFR 연결 | NFR-02, T-ARCH-SRP-01 등 |
| 수정 파일 | (≤3) |
| 신규 클래스 / 메서드 | N / N |

### 2. Change Budget 준수

| 항목 | 한도 | 실제 | 준수 |
|------|------|------|------|
| 수정 파일 | ≤3 | | ✅/❌ |
| 신규 클래스 | ≤1 | | ✅/❌ |
| 신규 메서드 | ≤3 | | ✅/❌ |

### 3. 검증 결과

| 명령 | 결과 |
|------|------|
| `pytest tests/ -v` | PASS (N passed) / FAIL |
| `pytest tests/test_golden_master.py -v` | PASS / N/A |
| 보호 테스트 `-k` | PASS / N/A |

### 4. diff·금지 파일 확인

- `tests/` 기대값: 미변경 ✅/❌
- `tests/golden/*.approved.txt`: 미변경 ✅/❌
- 수정 금지 파일: 미변경 ✅/❌

### 5. 구조 개선 요약

- 무엇을 어디로 옮겼는지 2~4문장
- 남은 스멜(다음 `/refactor-smell` 대상) 한 줄

### 6. 커밋 제안

```
refactor: <영역> — <NFR/PRD> <한 줄>
```

예: `refactor: cli — NFR-02 Parser 조율 위임`

- 사용자가 요청할 때만 커밋한다.

### 7. 다음 단계

- **PASS** → `/refactor-smell` 재실행해 잔여 스멜 확인, 또는 REPEAT(다음 FR)
- **FAIL** → 변경 롤백 후 원인 분석; Golden Master diff는 **버그**로 처리 (approved 수정 금지)

## 완료 조건

- [ ] 사용자가 선택한 스멜 **1건**만 적용했다.
- [ ] Change Budget **전 항목** 준수.
- [ ] `pytest tests/ -v` **전체 PASS** (사전·사후 동일).
- [ ] Golden Master **PASS** (존재 시).
- [ ] `tests/` 기대값·`tests/golden/` **미변경**.
- [ ] skip / xfail 0건, assert 약화 없음.
- [ ] 새 FR·관측 동작 변경 없음.
- [ ] **1 리팩터 = 1 커밋** 분리 가능 (`refactor:` 접두사).

## 중단 조건

- pytest 전체 또는 Golden Master **사전** FAIL
- refactor-smell 후보 선택이 **없거나** 모호함 (여러 스멜 동시 요청)
- Change Budget 초과가 불가피함
- 리팩터 후 Golden Master FAIL — `UPDATE_GOLDEN` 없이 **중단·롤백**
- 테스트 기대값 변경이 필요해 보임 — 명세 오류가 아니면 **중단** (리팩터 범위 아님)
- 출력 문자열·오류 메시지·변환 수치가 의도치 않게 변경됨

## 금지 사항 (요약)

- 한 세션에 스멜 2건 이상 적용
- 테스트·approved·docs 수정으로 「통과」
- `UPDATE_GOLDEN=1`로 Golden Master 맞추기
- RED/GREEN 단계 작업 (새 FR 구현)
- refactor-smell 없이 대규모 구조 변경
- 사용자 요청 없이 commit

## ARRR 단계

- **REFACTOR** — `/refactor-smell` 직후, 선택 후보 1건씩 반복
- **REPEAT** — 구조 부채가 허용 수준이면 다음 FR RED
- **RED / GREEN** — 이 Command 사용 대상 아님
