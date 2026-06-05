# /refactor-smell — REFACTOR 전 코드 스멜 분석

REFACTOR 단계에서 코드를 수정하기 **전에**, 현재 구현의 코드 스멜을 분석하고 `/refactor-safe`에 넘길 후보를 제안한다.

**이 Command는 분석 전용이다.** 코드 수정·테스트 수정·커밋·`/refactor-safe` 실행은 하지 않는다.

| 항목 | 값 |
|------|-----|
| Phase | REFACTOR (Refine) |
| Scope | `unit_converter/`, `tests/` (읽기·분석만) |
| Track | Logic + UI |
| ARRR | **Refine** — 구조 분석만, 구현 변경 없음 |

보조 참고:

- [docs/TEST_LOOP.md](../../docs/TEST_LOOP.md) — REFACTOR 허용·금지
- [.cursor/rules/unit-converter-tdd.mdc](../rules/unit-converter-tdd.mdc) — SRP·OCP·책임 분리
- [.cursorrules](../../.cursorrules) — 계층·import 방향·Change Budget
- [.cursor/commands/golden-master.md](./golden-master.md) — Golden Master 보호 계약
- [.cursor/commands/pytest-check.md](./pytest-check.md) — PASS/FAIL 판정

## 사용자 컨텍스트

명령 뒤에 붙은 텍스트(있으면)를 우선 반영한다.

- `SRP`, `NFR-02`, `cli` — 해당 계층·책임 스멜에 집중
- `OCP`, `NFR-01`, `registry` — 단위 확장·비율 SSOT 스멜에 집중
- `magic`, `3.28084`, `NFR-03` — Magic Number·비율 중복에 집중
- pytest 출력 붙여넣기 — 전제 확인에 활용
- 비어 있음 — 아래 스멜 표 전 항목을 `unit_converter/`·`tests/` 전체 스캔

## 전제 확인

분석을 시작하기 **전에** 아래 명령을 실행한다.

```bash
python -m pytest tests/ -v
```

- **전부 PASS가 아니면 중단**하고 실패 목록만 알려준다.
- PASS 상태가 아니면 코드 스멜 분석을 **진행하지 않는다**.

Golden Master 테스트가 존재하면 아래도 실행한다.

```bash
python -m pytest tests/test_golden_master.py -v
```

- Golden Master가 **FAIL**이면 중단하고 diff 또는 실패 원인만 보고한다.
- `tests/golden/*.approved.txt`는 **읽기만** — 수정·갱신 금지.

## 사전 읽기 (분석 시)

다음을 읽고 스멜 판정 근거로 삼는다.

1. [docs/PRD.md](../../docs/PRD.md) — NFR-01(OCP), NFR-02(SRP), NFR-03(비율 SSOT), NFR-06(Formatter 분리)
2. [docs/TRACEABILITY.md](../../docs/TRACEABILITY.md) — `T-ARCH-SRP-01`, `T-ARCH-OCP-01` (P3)
3. `unit_converter/` — `domain/`, `app/`, `infrastructure/`, `cli.py` (읽기만)
4. `tests/` — 아키텍처·경계·Golden Master 테스트 (읽기만)

`UnitConverter.py`는 레거시 시드 — 스멜 스캔 대상에서 제외한다. (REFACTOR 구현 대상은 `unit_converter/`)

## 분석 원칙

다음 스멜 표 기준으로 `unit_converter/`와 `tests/`를 스캔한다.

**코드 수정, 테스트 수정, approved 파일 수정, commit은 금지한다.**

| 우선순위 | 스멜 | 위치(파일:함수/클래스) | 근거 | Change Budget 내 리팩터 후보 |
|---|---|---|---|---|
| P0/P1/P2 | Long Method (>25줄·책임 2개 이상) | | | |
| P0/P1/P2 | Duplicated Code (입력 검증/단위 변환/출력 포맷 반복) | | | |
| P0/P1/P2 | Mysterious Name (의도가 불명확한 이름) | | | |
| P0/P1/P2 | Magic Number (`3.28084` / `1.09361` 등 상수 위치 부적절) | | | |
| P0/P1/P2 | 계층 위반 (domain/app/infrastructure/cli import 방향 위반) | | | |
| P0/P1/P2 | Feature Envy (cli/app이 domain 변환 로직을 직접 수행) | | | |
| P0/P1/P2 | OCP 위반 (새 단위 추가 시 converter 핵심 로직 수정 필요) | | | |
| P0/P1/P2 | SRP 위반 (Parser/Registry/Converter/Formatter 책임 혼재) | | | |

### 우선순위 가이드

| 등급 | 기준 | 예시 |
|------|------|------|
| **P0** | 외부 동작·Golden Master 회귀 위험, 또는 계층 위반으로 테스트 통과 후 구조 부채가 누적 | `cli.py`에 변환·비율 하드코딩, 비율 리터럴 다중 정의 |
| **P1** | SRP/OCP 위반이지만 Change Budget 1회로 분리 가능 | CLI에 파싱+검증+조율 혼재, Formatter 미분리 |
| **P2** | 이름·소규모 중복·dead code — 동작 영향 낮음 | rename-only, 미사용 import |

### 스멜별 UnitConverter 체크 포인트

- **Long Method** — `unit_converter/cli.py` 흐름 조립, `app/input_parser.py` 파싱+검증 혼재 여부
- **Duplicated Code** — 형식/숫자/음수/미지원 단위 검증이 Parser·CLI에 중복되는지; 변환식이 Converter 밖에 있는지
- **Magic Number** — `3.28084`, `1.09361`이 `domain/unit_registry.py`(또는 SSOT) 외부에 있는지 (NFR-03)
- **계층 위반** — `domain/`이 `app`·`infrastructure`·`cli`를 import하는지; `infrastructure/`가 변환·포맷을 수행하는지
- **Feature Envy** — `cli.py`·`app/`이 meter 기준 변환·단위 분기를 직접 수행하는지
- **OCP** — 새 단위 추가 시 `domain/converter.py` 핵심 분기 확장이 필요한지 (`if/elif` 단위 나열)
- **SRP** — Parser / Registry / Converter / Formatter / CLI 조율이 한 모듈에 묶였는지 (NFR-02)

## UnitConverter 계층 기준

| 계층 | 책임 | 금지 |
|------|------|------|
| `unit_converter/domain/` | 단위 개념, Registry, 변환 계산 | `app`, `infrastructure`, `cli` import |
| `unit_converter/app/` | 입력 파싱, 출력 포맷, 사용자 경계 처리 | 변환 계산 직접 수행 |
| `unit_converter/infrastructure/` | 설정 파일 로드 | 변환 계산·출력 포맷 직접 수행 |
| `unit_converter/cli.py` | CLI 진입점과 흐름 조립 | 비즈니스 로직 직접 보유 |

### SRP 컴포넌트 매핑 (TEST_LOOP · Rule)

| 컴포넌트 | 모듈(목표) | PRD 연결 |
|----------|------------|----------|
| **Parser** | `app/input_parser.py` | IN-01, FR-VAL-01~02 |
| **Registry** | `domain/unit_registry.py` | R-02~R-05, FR-CFG-01, FR-REG-01 |
| **Converter** | `domain/converter.py` | FR-CONV-01~03, R-04 |
| **Formatter** | `app/output_formatter.py` | FR-FMT-01, NFR-06 |
| **CLI** | `unit_converter/cli.py` | NFR-02 — 조율만 |

한 클래스·함수가 파싱+변환+출력을 동시에 하면 **P0~P1 SRP 위반** 후보로 표기한다.

## Change Budget

이번 리팩토링 후보는 **아래 예산 안에서만** 제안한다. 예산을 초과하는 후보는 표에 적되 `/refactor-safe` 후보에서 제외하고 「예산 초과」로 표기한다.

| 항목 | 한도 |
|------|------|
| 수정 파일 | ≤ 3 |
| 신규 클래스 | ≤ 1 |
| 신규 메서드 | ≤ 3 |
| 외부 동작 | 변경 금지 |
| 테스트 기대값 | 변경 금지 |
| Golden Master approved | 변경 금지 |

## 수행 절차

1. **전제 확인** — `pytest tests/ -v` (+ Golden Master) 실행, PASS 아니면 중단
2. **스캔** — `unit_converter/`·`tests/` 읽기만; import 그래프·함수 길이·리터럴·책임 혼재 확인
3. **스멜 표 작성** — 위 8종 스멜별 P0/P1/P2 판정, 위치·근거·Budget 내 후보 기입
4. **후보 선정** — Change Budget 준수하는 `/refactor-safe` 넘김 후보 1~3개 제안
5. **자가 점검** — 코드·테스트·docs·approved·commit 미수정 확인

## 출력 형식

아래 구조로 **한국어**로 답변한다.

### 1. 스멜 표

| 우선순위 | 스멜 | 위치 | 근거 | Change Budget 내 리팩터 후보 |
|---|---|---|---|---|

- 스멜이 없으면 해당 행에 「없음」과 근거(예: 이미 Registry SSOT 준수)를 명시한다.
- 여러 위치면 대표 1곳 + 「외 N곳」 요약.

### 2. `/refactor-safe` 후보 (1~3개)

| 후보 ID | 목표 | 수정 예상 파일 | 보호 테스트 | 위험도 | 추천 커밋 메시지 |
|---|---|---|---|---|---|
| RS-01 | | | | 낮음/중간/높음 | `refactor: ...` |

- **보호 테스트**: 회귀 확인용 `pytest -k` 키워드 또는 `tests/test_*.py` 파일명
- Architecture 검증: `T-ARCH-SRP-01`, `T-ARCH-OCP-01` 연결 시 명시
- **추천 커밋 메시지**: [TEST_LOOP.md](../../docs/TEST_LOOP.md) `refactor:` 접두사 준수

### 3. 전제·스캔 요약

```markdown
### 전제 확인
- pytest 전체: PASS / FAIL (N건)
- Golden Master: PASS / FAIL / 해당 없음

### 스캔 범위
- unit_converter/: <파일 수>개
- tests/: <관련 테스트> 요약
```

### 4. 마무리 안내

다음 문장을 **반드시** 출력한다.

> 가장 우선순위가 높은 P0 후보 1개만 골라 `/refactor-safe`를 실행하세요.

P0 후보가 없으면 P1 후보 1개를 고르도록 안내한다.

## 금지 사항

- 코드 수정 금지 (`unit_converter/`, `UnitConverter.py` 포함)
- 테스트 수정 금지 (`tests/` 본문·기대값)
- approved 파일 수정 금지 (`tests/golden/*.approved.txt`)
- docs 수정 금지 (`docs/*`, `README.md` 등)
- commit 금지
- `/refactor-safe` 실행 금지 (후보만 제안)
- 여러 후보를 한 번에 적용하라고 지시하지 말 것

## 중단 조건

- `pytest tests/ -v` 전체 PASS 아님
- Golden Master FAIL (존재 시)
- 스캔 범위 밖 파일 수정이 필요해 보이는 경우 — 분석만 하고 구현은 `/refactor-safe`로 위임

## ARRR 단계

- **REFACTOR 진입 시** — GREEN PASS·(선택) Golden Master 고정 후 **첫 단계**로 실행
- **REFACTOR 중** — 한 번의 `/refactor-safe` 적용 전마다 재실행 가능 (매번 PASS 전제 재확인)
- **RED / GREEN** — 이 Command 사용 대상 아님
