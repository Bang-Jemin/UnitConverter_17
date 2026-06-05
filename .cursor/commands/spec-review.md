# /spec-review — spec 브랜치 완료 판정

UnitConverter **spec** 단계 산출물을 검토하고, **red 브랜치로 넘어가도 되는지** GO / NO-GO를 판정한다.

## 사전 읽기 (필수)

| # | 파일 | 확인 목적 |
|---|------|-----------|
| 1 | [docs/PRD.md](../../docs/PRD.md) | 요구·SC·범위 완전성 |
| 2 | [docs/TRACEABILITY.md](../../docs/TRACEABILITY.md) | PRD ↔ RED 테스트 후보 연결 |
| 3 | [docs/TEST_LOOP.md](../../docs/TEST_LOOP.md) | ARRR·C2C·커밋 기준 |
| 4 | [.cursor/rules/unit-converter-tdd.mdc](../rules/unit-converter-tdd.mdc) | TDD·SRP·OCP 규칙 |
| 5 | [docs/SPEC_REVIEW_CHECKLIST.md](../../docs/SPEC_REVIEW_CHECKLIST.md) | 체크리스트 (본 Command와 동기화) |
| 6 | [Report/01.MomTest_ProblemDefinition_Report.md](../../Report/01.MomTest_ProblemDefinition_Report.md) | PRD 배경·증거 일치 |
| 7 | [README.md](../../README.md) | PRD·TRACEABILITY가 README 요구 반영 |

선택: [.cursor/commands/](../../commands/) 내 `red-test-plan.md`, `pytest-check.md` 존재 여부

## 사용자 컨텍스트

- `strict` — 필수 항목 하나라도 미충족 시 무조건 NO-GO
- 비어 있음 — 체크리스트 기준으로 판정, 경미한 gap은 조건부 GO 가능

## 수행 절차

1. **SPEC_REVIEW_CHECKLIST.md** 항목을 하나씩 검증 (파일 존재·내용·상호 일관성)
2. **교차 일관성** 검사
   - PRD FR/NFR/EXT ↔ TRACEABILITY ID 매핑 누락·모순
   - TEST_LOOP 우선순위 ↔ TRACEABILITY P1~P4 순서
   - Mom Test 증거 ↔ PRD §1·§10 SC
   - README 기본·추가 요구 ↔ PRD In Scope
3. **spec 범위 준수**
   - spec 단계에서 **구현·테스트 코드가 추가되지 않았는지** (선택적: `tests/`·`unit_converter/` diff 확인)
   - `UnitConverter.py`는 Mom Test 스냅샷 유지 (spec에서 불필요 변경 없음)
4. **red 브랜치 준비도**
   - RED 첫 대상(T-PARSE-01 / FR-01) 명확
   - Command·Rule·TEST_LOOP로 RED 작성 가능
5. **판정** — GO / CONDITIONAL GO / NO-GO

## 판정 기준

| 판정 | 조건 |
|------|------|
| **GO** | SPEC_REVIEW_CHECKLIST 필수 항목 전부 충족, 교차 일관성 이슈 없음 |
| **CONDITIONAL GO** | 필수 충족, 사소한 문서 보완 1~2건(판정 시 Must-fix 목록 명시) |
| **NO-GO** | PRD·TRACEABILITY·TEST_LOOP·Rule 중 누락, ID 추적 단절, README/PRD 범위 불일치 |

`strict` 모드: CONDITIONAL GO 불허 → 미충족 시 NO-GO

## 출력 형식

```markdown
## spec-review 판정

### 최종 판정: GO | CONDITIONAL GO | NO-GO

### SPEC_REVIEW_CHECKLIST 요약
| 섹션 | 상태 | 비고 |
|------|------|------|
| Mom Test · Report | ✅/❌ | |
| PRD | ✅/❌ | |
| TRACEABILITY | ✅/❌ | |
| TEST_LOOP | ✅/❌ | |
| Cursor Rule | ✅/❌ | |
| Cursor Commands | ✅/❌ | |
| spec 범위 준수 | ✅/❌ | |

### 교차 일관성
- PRD ↔ TRACEABILITY: ...
- TRACEABILITY ↔ TEST_LOOP: ...
- Mom Test ↔ PRD SC: ...

### 발견 이슈
| # | 심각도 | 항목 | 조치 |
|---|--------|------|------|
| | blocker/major/minor | | |

### red 브랜치 전환 시 권장 첫 작업
1. 브랜치: `spec` → `red` (또는 `red` 생성)
2. 첫 RED: `<Test-ID>` / `<PRD-ID>` ([TRACEABILITY](../../docs/TRACEABILITY.md) P1)
3. Command: `/red-test-plan` 또는 `/red-test-plan FR-01`

### Must-fix (NO-GO · CONDITIONAL GO 시)
- [ ] ...
```

## 금지

- spec-review 중 **구현 코드·테스트 코드 작성**
- `UnitConverter.py` 수정
- 판정 없이 "넘어가도 됩니다"만 단정
