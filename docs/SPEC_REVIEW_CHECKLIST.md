# SPEC_REVIEW_CHECKLIST — spec 브랜치 완료 확인

> PRD: [PRD.md](./PRD.md) · 판정 Command: [/spec-review](../.cursor/commands/spec-review.md)

**spec** 브랜치를 **red** 브랜치로 넘기기 전에 아래 항목을 확인한다.  
자동 판정은 Cursor에서 `/spec-review` 를 실행한다.

---

## 1. Mom Test · Report

| # | 확인 항목 | 완료 |
|---|-----------|------|
| 1.1 | [Report/01.MomTest_ProblemDefinition_Report.md](../Report/01.MomTest_ProblemDefinition_Report.md) 존재 | [ ] |
| 1.2 | Mom Test 증거 5건이 PRD §1과 일치 | [ ] |
| 1.3 | 「진짜 문제」 한 문장이 PRD §1과 동일 | [ ] |
| 1.4 | 표면 문제(솔루션 선행)가 PRD 본문에 끼어들지 않음 | [ ] |

---

## 2. PRD (docs/PRD.md)

| # | 확인 항목 | 완료 |
|---|-----------|------|
| 2.1 | README 기본 요구(파싱, 3단위, OCP, SRP, 입력 검증) 반영 | [ ] |
| 2.2 | README 추가 요구(설정 외부화, 동적 등록, 출력 포맷) In Scope 2차에 포함 | [ ] |
| 2.3 | 도메인 규칙 R-01~R-05 (meter 기준, SSOT) 명시 | [ ] |
| 2.4 | 입력 IN-01~04, 오류 ERR-01~05 정의 | [ ] |
| 2.5 | 성공 기준 SC-1~5 (Mom Test · R-G-I-O) 정의 | [ ] |
| 2.6 | C2C 추적 예시 (§12) 존재 | [ ] |

---

## 3. TRACEABILITY (docs/TRACEABILITY.md)

| # | 확인 항목 | 완료 |
|---|-----------|------|
| 3.1 | 필수 FR-01~FR-06 매핑 존재 | [ ] |
| 3.2 | NFR-01(OCP), NFR-02(SRP) 매핑 존재 | [ ] |
| 3.3 | EXT-01~03(설정·등록·포맷) 매핑 존재 | [ ] |
| 3.4 | 각 행에 Test ID, 유형(Domain/Boundary/Architecture/Extension), Given/When/Then | [ ] |
| 3.5 | 우선순위 P1~P4 및 RED 진행 순서 명시 | [ ] |
| 3.6 | SC-1~5와 TRACEABILITY ID 연결표 존재 | [ ] |

---

## 4. TEST_LOOP (docs/TEST_LOOP.md)

| # | 확인 항목 | 완료 |
|---|-----------|------|
| 4.1 | ARRR ↔ RED/GREEN/REFACTOR/REPEAT 매핑 | [ ] |
| 4.2 | RED: 구현 금지 · GREEN: 최소 구현 · REFACTOR: 동작 동일 | [ ] |
| 4.3 | skip/xfail/assert 약화 금지 | [ ] |
| 4.4 | 단계별 실행 명령(`pytest tests/ -v`) | [ ] |
| 4.5 | 단계별 다음 조건·커밋 메시지 형식 | [ ] |
| 4.6 | Parser / Registry / Converter / Formatter SRP 가이드 | [ ] |

---

## 5. Cursor Rule

| # | 확인 항목 | 완료 |
|---|-----------|------|
| 5.1 | [.cursor/rules/unit-converter-tdd.mdc](../.cursor/rules/unit-converter-tdd.mdc) 존재 | [ ] |
| 5.2 | C2C · ARRR · 단계별 금지 사항 명시 | [ ] |
| 5.3 | SRP 컴포넌트 · OCP · 입력 검증(FR-VAL) 매핑 | [ ] |
| 5.4 | PRD · TEST_LOOP 링크 | [ ] |

---

## 6. Cursor Commands

| # | 확인 항목 | 완료 |
|---|-----------|------|
| 6.1 | [.cursor/commands/red-test-plan.md](../.cursor/commands/red-test-plan.md) — RED 후보 제안 | [ ] |
| 6.2 | [.cursor/commands/pytest-check.md](../.cursor/commands/pytest-check.md) — pytest 요약·분류 | [ ] |
| 6.3 | [.cursor/commands/spec-review.md](../.cursor/commands/spec-review.md) — spec 완료 판정 | [ ] |

---

## 7. spec 범위 준수 (red 전 코드)

| # | 확인 항목 | 완료 |
|---|-----------|------|
| 7.1 | spec 작업 중 **RED 테스트 코드 미작성** (또는 의도적 보류 명시) | [ ] |
| 7.2 | spec 작업 중 **GREEN 구현 미작성** (`unit_converter/` 등) | [ ] |
| 7.3 | `UnitConverter.py` Mom Test 스냅샷 — spec에서 불필요 변경 없음 | [ ] |
| 7.4 | spec 산출물은 **문서·Cursor 설정** 위주 | [ ] |

---

## 8. red 브랜치 전환 준비

| # | 확인 항목 | 완료 |
|---|-----------|------|
| 8.1 | 첫 RED 대상 확정: **FR-01 / T-PARSE-01** (P1) | [ ] |
| 8.2 | `/red-test-plan` 으로 첫 테스트 계획 수립 가능 | [ ] |
| 8.3 | `/pytest-check` 로 RED 실패 확인 절차 준비 | [ ] |
| 8.4 | 팀·본인: spec 브랜치 커밋·푸시 완료 (해당 시) | [ ] |

---

## 판정 요약

| 결과 | 조건 |
|------|------|
| **GO** | §1~§8 필수 항목(1.1~7.4) 전부 [x] |
| **CONDITIONAL GO** | blocker 없음, minor 문서 보완만 남음 — Must-fix 명시 후 red 진행 |
| **NO-GO** | PRD·TRACEABILITY·TEST_LOOP·Rule·Commands 중 누락 또는 ID 추적 단절 |

### Must-fix (판정 시 기록)

```
1.
2.
```

### spec 완료 서명 (선택)

| 항목 | 값 |
|------|-----|
| 검토일 | |
| 브랜치 | spec |
| 판정 | GO / CONDITIONAL GO / NO-GO |
| 검토者 | |

---

## red 브랜치 첫 커밋 가이드 (참고)

```
test(RED): T-PARSE-01 — FR-01 unit:value 파싱 실패 테스트 추가
```

상세: [TEST_LOOP.md](./TEST_LOOP.md) § RED
