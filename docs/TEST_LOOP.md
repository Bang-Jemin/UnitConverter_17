# TEST_LOOP — UnitConverter TDD 사이클

> PRD: [PRD.md](./PRD.md) · Cursor 규칙: [.cursor/rules/unit-converter-tdd.mdc](../.cursor/rules/unit-converter-tdd.mdc)

UnitConverter 실습은 **C2C**(PRD → Test → Code) 추적성과 **ARRR** TDD 사이클로 진행한다.

| ARRR | TDD 단계 | 한 줄 요약 |
|------|----------|------------|
| **A**sk | RED | PRD 요구를 실패하는 테스트를 먼저 쓴다 |
| **R**espond | GREEN | 테스트를 통과시키는 최소 구현만 한다 |
| **R**efine | REFACTOR | 외부 동작은 그대로, 구조만 개선한다 |
| **R**epeat | REPEAT | 다음 PRD 요구로 같은 루프를 반복한다 |

---

## 공통 원칙

### C2C 추적성

| 순서 | 산출물 | 규칙 |
|------|--------|------|
| 1 | PRD | `FR-*`, `SC-*`, `ERR-*` 중 **이번 사이클 1건** 선택 |
| 2 | Test | 테스트 docstring·주석에 PRD ID 기록 (예: `# FR-CONV-01 / D-CONV-01`) |
| 3 | Code | 해당 테스트만 통과하는 최소 코드 |

PRD §12 C2C 표를 참고해 Test ID(`D-*`)를 부여한다.

### 전 단계 금지 (위반 시 사이클 무효)

- `@pytest.mark.skip`, `@pytest.mark.xfail`, `pytest.skip()` 사용
- assert 삭제·완화, 허용 오차 임의 확대로 통과 우회
- PRD 범위 밖 기능 선행 구현
- RED 단계에서 구현 코드 작성

### 아키텍처 가이드 (REFACTOR · GREEN 후반)

| 컴포넌트 | 책임 |
|----------|------|
| **Parser** | `단위:값` 분리, `float` 파싱, 형식 전처리 |
| **Registry** | 단위·비율 SSOT, 동적 등록(2차) |
| **Converter** | meter 기준 변환; feet↔yard는 meter 경유 |
| **Formatter** | text / JSON / CSV / 표 출력 (2차) |

- **OCP**: 단위·포맷 추가 시 Converter 핵심 변경 최소
- **SRP**: Parser / Registry / Converter / Formatter / CLI 조율 분리

---

## 1. RED — Ask

### 목적

선택한 PRD 요구가 **아직 구현되지 않았음**을 테스트로 증명한다. 실패하는 테스트가 다음 GREEN의 명세가 된다.

### 허용 작업

- `tests/` 아래 테스트 함수·클래스 **추가**
- 테스트 docstring·주석에 **PRD ID · Test ID** 기록
- PRD `SC-*`·`ERR-*`에 맞는 입력·기대값·메시지 검증 작성
- `pytest` 실행하여 **의도된 실패** 확인

### 금지 작업

- `UnitConverter.py`, `src/` 등 **구현 코드** 작성·수정
- skip / xfail / assert 약화
- 한 사이클에 서로 무관한 FR 여러 건을 한 테스트에 뭉치기 (1 FR : 1~N focused test 권장)

### 실행 명령

```bash
pytest tests/ -v
pytest tests/ -v -k "<새_테스트_키워드>"
```

### 다음 단계 조건 (→ GREEN)

- [ ] 대상 PRD ID가 테스트에 명시됨
- [ ] 새·수정 테스트가 **실패**함 (ImportError·AssertionError 등 — skip 아님)
- [ ] 실패 원인이 「아직 구현 안 됨」임이 명확함
- [ ] 구현 코드 diff 없음

### 커밋 기준

```
test(RED): <Test-ID> — <PRD-ID> 실패 테스트 추가
```

예: `test(RED): D-VAL-01 — FR-VAL-04 음수 거부 실패 테스트 추가`

- 커밋 범위: `tests/` (+ 필요 시 PRD ID 주석만)
- 구현 파일 미포함

---

## 2. GREEN — Respond

### 목적

RED에서 작성한 테스트만 **통과**시키는 최소 구현을 추가한다. 설계 완성이 아니라 「테스트를 녹색으로 만드는 것」이 목표다.

### 허용 작업

- 실패 테스트를 통과시키는 **최소** 코드 추가·수정
- 테스트가 요구하는 공개 API·함수·클래스 도입
- `pytest tests/ -v` **전체 통과** 확인

### 금지 작업

- RED 범위 밖 FR 구현
- skip / xfail / assert 약화
- REFACTOR 성격의 대규모 구조 변경 (GREEN에서는 「돌아가게」가 우선)
- Mom Test에서 지적된 상수를 **새 위치에 또 중복** 정의

### 실행 명령

```bash
pytest tests/ -v
pytest tests/ -v -k "<대상_테스트>"
```

### 다음 단계 조건 (→ REFACTOR 또는 REPEAT)

**→ REFACTOR** (구조 부채가 보일 때):

- [ ] 대상 RED 테스트 포함 **전체** `pytest` 통과
- [ ] `if/elif`·`print`·비율 리터럴이 한 함수에 뭉치거나 SRP/OCP 위반
- [ ] GREEN 과정에서 「일단」 넣은 중복·임시 코드 존재

**→ REPEAT** (구조가 충분히 단순할 때):

- [ ] 전체 테스트 통과
- [ ] 추가 REFACTOR 없이도 PRD 요구 충족
- [ ] 다음 미처리 PRD FR 존재

### 커밋 기준

```
feat(GREEN): <PRD-ID> — <한 줄 요약>
```

예: `feat(GREEN): FR-VAL-04 — 음수 입력 거부`

- RED 커밋과 **분리** (RED 먼저, GREEN 다음)
- 테스트 + 구현 함께 커밋 가능

---

## 3. REFACTOR — Refine

### 목적

외부에서 관측 가능한 동작(변환 결과, 오류 메시지, 출력 형식)을 **변경하지 않고** Parser / Registry / Converter / Formatter 책임을 정렬한다.

### 허용 작업

- SRP에 맞는 모듈·클래스 분리
- 비율 SSOT화 (Registry 또는 단일 설정)
- 중복 제거, 이름 개선, dead code 제거
- OCP: 단위 추가 touch point 축소
- **전체 테스트 통과 유지**

### 금지 작업

- 관측 가능 동작 변경 (변환값, 오류 조건, 메시지 의미 변경)
- skip / xfail / assert 약화
- 새 FR 기능 추가 (→ REPEAT 후 RED에서)
- 테스트 수정으로 REFACTOR 「통과」 우회 (테스트 변경은 버그 수정·명세 오류 수정 때만)

### 실행 명령

```bash
pytest tests/ -v
pytest tests/ --tb=short
```

REFACTOR 전·후 모두 실행해 **동일 통과** 확인.

### 다음 단계 조건 (→ REPEAT)

- [ ] `pytest tests/ -v` 전체 통과
- [ ] Parser / Registry / Converter / Formatter(해당 시) 책임 분리 또는 OCP 개선 완료
- [ ] 비율 `3.28084` / `1.09361` 단일 출처 준수 (또는 명확한 SSOT 경로)
- [ ] diff에 기능 추가(FR) 없음

### 커밋 기준

```
refactor: <영역> — <PRD/NFR 연결 한 줄>
```

예: `refactor: registry — NFR-03 비율 SSOT 분리`

- `test:` / `feat:` 와 구분 — 동작 동일, 구조만 변경

---

## 4. REPEAT — 다음 요구

### 목적

완료한 FR·SC를 PRD 추적표에 반영하고, **다음 우선순위 PRD 요구**로 RED부터 재시작한다.

### 권장 진행 순서 (1차)

| 순서 | PRD | Test ID (예) | 내용 |
|------|-----|--------------|------|
| 1 | FR-CONV-01 | D-CONV-01 | meter 입력 → 전 단위 변환 |
| 2 | FR-CONV-02 | D-CONV-02 | feet/yard 입력 상호 일치 |
| 3 | FR-VAL-04 | D-VAL-01 | 음수 거부 (SC-2) |
| 4 | FR-VAL-01~03 | D-VAL-02, D-VAL-03 | 형식·숫자·없는 단위 (SC-3) |
| 5 | SC-1 | — | README 예시 일괄 회귀 |

2차: FR-CFG-01, FR-REG-01, FR-FMT-01 (`D-EXT-01`, `D-FMT-01`)

### 허용 작업

- PRD §12 C2C 표·로컬 체크리스트 갱신
- 완료 FR 표시
- 다음 FR 선택 후 **RED** 진입

### 금지 작업

- 완료되지 않은 FR 건너뛰기 (의존성 없는 한 순서 유지)
- skip으로 남은 실패 방치

### 실행 명령

```bash
pytest tests/ -v
```

REPEAT 시작 전 회귀 확인용 전체 실행.

### 다음 단계 조건 (→ RED)

- [ ] 이전 사이클 GREEN 또는 REFACTOR 완료·커밋됨
- [ ] 전체 테스트 통과 상태
- [ ] 다음 PRD ID가 명확히 선택됨

### 커밋 기준

REPEAT 자체는 커밋 불필요. 다음 **RED** 커밋으로 이어진다.

---

## 사이클 한 바퀴 요약

```
PRD FR 선택
    ↓
RED    — 실패 테스트 (구현 금지)
    ↓
GREEN  — 최소 구현 (전체 통과)
    ↓
REFACTOR? — SRP/OCP 정렬 (동작 동일)
    ↓
REPEAT — 다음 FR → RED
```

## 입력 검증 테스트 체크리스트 (FR-VAL)

| 입력 예시 | PRD | 기대 |
|-----------|-----|------|
| `meter` (콜론 없음) | FR-VAL-01 | ERR-01, 변환 미실행 |
| `meter:abc` | FR-VAL-02 | ERR-02, 변환 미실행 |
| `:2.5` | FR-VAL-01 | ERR-01 또는 ERR-02 (명세대로) |
| `mile:1` | FR-VAL-03 | ERR-03, 변환 미실행 |
| `meter:-1` | FR-VAL-04 | ERR-04, 변환 미실행, 비정상 예외 아님 |

## 성공 기준 (Mom Test · PRD §10)

| ID | 검증 포인트 |
|----|-------------|
| SC-1 | `meter:2.5`, `feet:8.2`, `yard:2.7` README 비율 일치 |
| SC-2 | `meter:-1` 음수 거부 |
| SC-3 | 형식·없는 단위 구분 가능 |
| SC-4 | cubit 등록 후 기존 TC + cubit 출력 |
| SC-5 | text/JSON/CSV/표 동일 수치 |

각 SC는 REPEAT 순서에 맞춰 RED → GREEN → (REFACTOR)로 커버한다.
