# /red-test-plan — RED 테스트 후보 제안

PRD와 TRACEABILITY를 근거로 **다음 RED 사이클**에 작성할 테스트 후보를 제안한다.  
**이 Command는 테스트 계획만 수립한다.** 구현 코드·실제 `tests/` 파일 생성은 하지 않는다.

## 사전 읽기 (필수)

다음 파일을 **읽은 뒤** 답변한다.

1. [docs/PRD.md](../../docs/PRD.md)
2. [docs/TRACEABILITY.md](../../docs/TRACEABILITY.md)
3. [docs/TEST_LOOP.md](../../docs/TEST_LOOP.md) — RED 단계 허용·금지
4. [.cursor/rules/unit-converter-tdd.mdc](../rules/unit-converter-tdd.mdc)

## 사용자 컨텍스트

명령 뒤에 붙은 텍스트(있으면)를 우선 반영한다.

- `P1`, `FR-02`, `T-CONV-01` 등 — 해당 요구·테스트 ID에 집중
- `다음`, `next` — TRACEABILITY 우선순위表에서 **아직 RED 미작성**으로 보이는 첫 항목
- 비어 있음 — **P1**부터 TRACEABILITY 순서대로 제안

## 수행 절차

1. **현재 상태 파악**
   - `tests/` 디렉터리·기존 테스트 파일 존재 여부 확인 (읽기만)
   - 이미 커버된 PRD ID / Test ID 추정 (파일명·docstring·주석 기준)

2. **대상 1건 선택**
   - TRACEABILITY 우선순위(P1→P4)와 C2C 원칙에 따라 **이번 RED 1건**만 선택
   - 선택 근거: PRD ID, Test ID, 아직 미커버 여부

3. **RED 테스트 후보 명세 작성**
   - TRACEABILITY 매트릭스의 Given / When / Then을 테스트 관점으로 구체화
   - PRD §10 SC-*·ERR-*와의 연결 명시

4. **RED 금지 사항 자가 점검**
   - 구현 코드 수정·추가 없음
   - skip / xfail / assert 약화 없음
   - 한 사이클에 무관한 FR 다건 뭉치기 지양

## 출력 형식

아래 구조로 **한국어**로 답변한다.

```markdown
## RED 테스트 계획 — <Test-ID>

### 추적성
| 항목 | 값 |
|------|-----|
| PRD ID | |
| Test ID | |
| 테스트 유형 | Domain / Boundary / Architecture / Extension |
| 우선순위 | P1~P4 |
| 연결 SC | SC-* |

### Given / When / Then
- **Given**:
- **When**:
- **Then**:

### 제안 테스트 케이스 (RED 후보)
| # | 테스트 함수명 (제안) | 입력·조건 | 기대 결과 |
|---|---------------------|-----------|-----------|
| 1 | | | |

### 배치 제안
- 파일: `tests/test_<영역>.py` (제안 경로)
- docstring·주석: `# <PRD-ID> / <Test-ID>`

### 예상 실패 유형 (RED 확인용)
- ImportError / ModuleNotFoundError / AssertionError 중 예상되는 것

### RED 단계 체크
- [ ] PRD ID · Test ID 명시
- [ ] 구현 코드 미수정
- [ ] skip/xfail/assert 약화 없음
- [ ] TEST_LOOP RED → GREEN 조건 충족 가능

### 다음 단계
- 사용자가 RED 테스트 작성 승인 후 `tests/`에 코드 추가
- `pytest tests/ -v -k "<키워드>"` 로 **의도된 실패** 확인
```

## 금지

- `UnitConverter.py`, `src/`, `unit_converter/` 등 **구현 코드** 작성·수정
- `tests/`에 실제 pytest 코드 **생성** (계획·제안만)
- GREEN·REFACTOR 단계 작업 선행
