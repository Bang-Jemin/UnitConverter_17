# TRACEABILITY — PRD ↔ RED 테스트 후보

> PRD: [PRD.md](./PRD.md) · README: [README.md](../README.md) · TDD 루프: [TEST_LOOP.md](./TEST_LOOP.md)

본 문서는 **C2C**(PRD → Test → Code) 추적을 위한 RED 단계 테스트 후보 명세이다.  
실제 `tests/` 코드는 RED 사이클에서 이 표를 근거로 작성한다.

## ID 매핑 (TRACEABILITY ↔ PRD 상세)

| TRACEABILITY ID | PRD / README 근거 |
|-----------------|-------------------|
| FR-01 | IN-01, FR-VAL-02(파싱 전제) |
| FR-02 | FR-CONV-01, R-02·R-03, OUT-01, SC-1 |
| FR-03 | FR-CONV-02, R-04, OUT-03, SC-1 |
| FR-04 | FR-VAL-03, IN-04, ERR-03, SC-3 |
| FR-05 | FR-VAL-01·02, IN-02, ERR-01·02, SC-3 |
| FR-06 | FR-VAL-04, IN-03, ERR-04, SC-2 |
| NFR-01 | NFR-01, G-02, README §품질 OCP |
| NFR-02 | NFR-02, G-02, README §품질 SRP |
| EXT-01 | FR-CFG-01, CFG-03, R-05 |
| EXT-02 | FR-REG-01, REG-01, FR-CONV-03, SC-4 |
| EXT-03 | FR-FMT-01, FMT-OUT-01~04, SC-5, NFR-06 |

---

## 추적성 매트릭스 (RED 테스트 후보)

| PRD ID | 요구사항 | 테스트 ID | 테스트 유형 | Given | When | Then | 우선순위 |
|--------|----------|-----------|-------------|-------|------|------|----------|
| FR-01 | `unit:value` 입력 파싱 — 첫 `:` 기준으로 단위·숫자 분리 | T-PARSE-01 | Domain | 지원 단위 `meter`, `feet`, `yard`가 Registry에 등록되어 있음 | `meter:2.5`, `feet:8.2`, `yard:2.7` 문자열을 Parser에 전달함 | 단위 문자열과 float 값이 각각 `(meter, 2.5)`, `(feet, 8.2)`, `(yard, 2.7)`로 분리됨 | P1 |
| FR-02 | meter 입력을 feet·yard로 변환 (README 비율) | T-CONV-01 | Domain | 기준 단위 meter, `1 m = 3.28084 ft`, `1 m = 1.09361 yd` (R-02·R-03) | `meter:2.5`를 변환함 | meter=2.5, feet≈8.2021, yard≈2.7340 (허용 오차 내); README 예시 8.2·2.7과 정합 | P1 |
| FR-03 | feet·yard 입력은 meter 기준으로 변환 — 상호·역변환 일치 | T-CONV-02 | Domain | 동일 README 비율 및 meter 경유 규칙 (R-04) | `feet:8.2`, `yard:2.7` 각각 변환함 | 각 입력에서 meter/feet/yard 전 단위 결과가 SC-1 기대값과 허용 오차 내 일치; feet↔yard는 meter 경유와 동일 | P1 |
| FR-04 | 미지원 단위 오류 | T-VAL-03 | Boundary | 기본 3단위(meter, feet, yard)만 지원 | `mile:1`을 처리함 | 변환 미실행; 알 수 없는 단위(ERR-03) 메시지 출력 | P2 |
| FR-05 | 잘못된 입력 형식 오류 | T-VAL-02 | Boundary | CLI 입력 검증기(Parser/Validator) 준비 | `:` 없는 `meter`, 숫자 불가 `meter:abc`, 단위 누락 `:2.5`를 각각 처리함 | 변환 미실행; 형식 오류(ERR-01) 또는 숫자 오류(ERR-02) 메시지가 케이스별로 구분됨 (SC-3) | P2 |
| FR-06 | 음수 입력 오류 | T-VAL-01 | Boundary | 양수만 허용하는 검증 규칙(FR-VAL-04) | `meter:-1`을 처리함 | 변환 미실행; 음수 거부(ERR-04) 메시지; 비정상 예외(Traceback) 발생하지 않음 (SC-2) | P2 |
| NFR-01 | OCP — 단위·비율·포맷 추가 시 기존 변환 핵심 변경 최소 | T-ARCH-OCP-01 | Architecture | meter/feet/yard 기본 변환 및 T-CONV-01·02가 통과된 상태 | Registry(또는 설정)에 `cubit`(0.4572 m)만 추가 등록함 | 기존 3단위 TC 전부 통과 유지; cubit 포함 전 단위 출력 추가; Converter `if/elif` 핵심 분기 확장 없이 등록만으로 확장 (SC-4) | P3 |
| NFR-02 | SRP — Parser / Registry / Converter / Formatter / CLI 책임 분리 | T-ARCH-SRP-01 | Architecture | 리팩터된 모듈 구조 | 각 컴포넌트의 공개 API와 import 관계를 검증함 | Parser는 파싱만, Registry는 단위·비율 SSOT만, Converter는 meter 기준 변환만, Formatter는 출력 서식만 담당; CLI는 조율만 수행 (NFR-02) | P3 |
| EXT-01 | 설정 파일(JSON/YAML)에서 단위 비율 로드 | T-EXT-CFG-01 | Extension | `units.json`(또는 `.yaml`)에 meter/feet/yard 비율 정의 (CFG-03) | Registry가 해당 파일을 로드함 | 코드 내 리터럴 없이 R-02·R-03 비율로 T-CONV-01·02와 동일 결과; SSOT가 설정 파일 한 곳 (R-05, FR-CFG-01) | P4 |
| EXT-02 | 동적 단위 등록 (`1 cubit = 0.4572 meter`) | T-EXT-REG-01 | Extension | 기본 3단위 설정 로드 완료 | `1 cubit = 0.4572 meter` 등록 후 `meter:1` 변환 | 기존 meter/feet/yard TC 회귀 통과; cubit≈2.19 ft 등 cubit 변환 결과 포함 (REG-01, SC-4) | P4 |
| EXT-03 | json / csv / table 출력 포맷 | T-EXT-FMT-01 | Extension | 동일 입력 `meter:2.5`에 대한 변환 결과 도메인 모델 | Formatter에 text / JSON / CSV / table(표) 포맷을 각각 적용함 | 포맷별 표현만 다르고 수치·단위 의미는 동일 (SC-5, FMT-OUT-01~04); Converter 로직 변경 없음 (NFR-06) | P4 |

---

## 우선순위 · RED 진행 순서

| 우선순위 | PRD ID | 테스트 ID | TDD 단계 메모 |
|----------|--------|-----------|---------------|
| P1 | FR-01 → FR-02 → FR-03 | T-PARSE-01 → T-CONV-01 → T-CONV-02 | 핵심 변환·파싱; SC-1 충족 |
| P2 | FR-04 → FR-05 → FR-06 | T-VAL-03 → T-VAL-02 → T-VAL-01 | 입력 검증; SC-2·SC-3 |
| P3 | NFR-02 → NFR-01 | T-ARCH-SRP-01 → T-ARCH-OCP-01 | REFACTOR 후 구조 검증; Mom Test 회귀 방지 |
| P4 | EXT-01 → EXT-02 → EXT-03 | T-EXT-CFG-01 → T-EXT-REG-01 → T-EXT-FMT-01 | README 추가 요구; SC-4·SC-5 |

---

## RED 작성 시 체크리스트

- [ ] 테스트 docstring·주석에 **PRD ID**와 **테스트 ID** 동시 기록
- [ ] Given / When / Then이 위 표와 모순되지 않음
- [ ] skip / xfail / assert 약화 없음 ([TEST_LOOP.md](./TEST_LOOP.md) 준수)
- [ ] GREEN 전까지 구현 코드 수정 없음

## 관련 성공 기준 (PRD §10)

| SC | 연결 TRACEABILITY |
|----|-------------------|
| SC-1 | FR-02, FR-03 (T-CONV-01, T-CONV-02) |
| SC-2 | FR-06 (T-VAL-01) |
| SC-3 | FR-04, FR-05 (T-VAL-02, T-VAL-03) |
| SC-4 | NFR-01, EXT-02 (T-ARCH-OCP-01, T-EXT-REG-01) |
| SC-5 | EXT-03 (T-EXT-FMT-01) |
