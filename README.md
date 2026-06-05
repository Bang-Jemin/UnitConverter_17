
## Unit Converter (Python)
![unit-converter](./unit-converter.jpg)

### Overview

- 사용자가 입력한 길이(`단위:값`)를 기반으로, 해당 값을 다른 모든 단위로 변환해 출력하는 프로그램.
- 새로운 단위를 추가할 때 기존 코드의 변경이 최소화되도록 설계한다.
- 각 단위 변환 로직은 테스트 코드로 검증한다.

실습 본체는 루트의 `UnitConverter.py`(레거시 시드)가 아니라 **`unit_converter/` 패키지**이다.  
파싱·변환·검증·CLI 조율은 모듈별로 분리되어 있으며, TDD·Golden Master 테스트로 회귀를 방지한다.

---

### 프로젝트 구조

```
unit_converter/
├── cli.py                    # CLI 진입 — handle_input(), HandleInputResult
├── app/
│   ├── input_parser.py       # "unit:value" 파싱
│   └── output_formatter.py   # JSON/CSV/표 출력 (2차 — stub)
├── domain/
│   ├── unit_registry.py      # 단위·비율 SSOT, 등록·조회
│   ├── converter.py          # meter 기준 변환
│   └── length_unit.py        # (stub)
└── infrastructure/
    └── config_loader.py      # JSON/YAML 설정 로드 (2차 — stub)

UnitConverter.py              # 레거시 시드 (Mom Test 참고용, 수정 최소화)
tests/
├── test_converter.py         # Domain — 파싱·변환
├── test_cli.py               # Boundary — 입력 검증
├── test_golden_master.py     # CLI 출력 Golden Master (GM-01~07)
└── golden/*.approved.txt     # approved 기준 파일
docs/                         # PRD, TRACEABILITY, TEST_LOOP
```

| 모듈 | 책임 |
|------|------|
| **Parser** (`app/input_parser`) | `단위:값` 분리, 숫자 파싱 |
| **Registry** (`domain/unit_registry`) | 단위·비율 SSOT, 등록·조회 |
| **Converter** (`domain/converter`) | meter 기준 변환, 전 단위 dict 반환 |
| **CLI** (`cli`) | 입출력 조율·검증 — 도메인 로직은 위 모듈에 위임 |
| **Formatter** (`app/output_formatter`) | text/JSON/CSV/표 출력 (2차) |
| **Config loader** (`infrastructure/config_loader`) | 설정 외부화 (2차) |

---

### 환경 설정 및 실행

```bash
# 가상환경 생성 (선택)
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate

# 개발 의존성 (pytest)
pip install -e ".[dev]"

# 테스트 실행
python -m pytest tests/ -v

# Golden Master만 실행
python -m pytest tests/test_golden_master.py -v
```

#### 프로그램 API 사용 (`unit_converter`)

```python
from unit_converter.cli import handle_input

result = handle_input("meter:2.5")
if result.ok:
    for line in result.output_lines:
        print(line)
else:
    print(result.message)  # error_kind: format | number | negative
```

**정상 출력 예** (`meter:2.5`):

```
2.5 meter = 2.5 meter
2.5 meter = 8.2021 feet
2.5 meter = 2.734025 yard
```

#### 레거시 시드 실행 (참고)

Mom Test 문제 코드 스냅샷. 실습·테스트의 기준 구현은 `unit_converter/`이다.

```bash
python UnitConverter.py
```

---

### 기본 요구사항

1. 사용자 입력 예시:
   ```
   meter:2.5
   ```
   → 출력 (줄 형식: `{value} {input_unit} = {converted} {target_unit}`):
   ```
   2.5 meter = 2.5 meter
   2.5 meter = 8.2021 feet
   2.5 meter = 2.734025 yard
   ```

2. 현재 지원 단위:
   - meter
   - feet
   - yard

3. 새로운 단위가 추가될 때도 기존 코드의 변경이 최소화되도록 할 것.  
   → `UnitRegistry.register()`로 등록; Converter 핵심 분기 확장 없이 확장 (OCP).

4. 각 단위 간 변환이 정확히 계산되도록 테스트 코드를 작성할 것.  
   → `tests/test_converter.py`, `tests/test_cli.py`, Golden Master `tests/test_golden_master.py`.

### 입력 검증 (현재 구현)

| 입력 예 | 기대 |
|---------|------|
| `meter` (콜론 없음) | 변환 미실행 + 형식 오류 |
| `meter:abc` | 변환 미실행 + 숫자 오류 |
| `:2.5` | 변환 미실행 + 형식 오류 |
| `meter:-1` | 변환 미실행 + 음수 거부 |
| `mile:1` | 변환 미실행 + 알 수 없는 단위 *(후속 구현)* |

---

### 비즈니스 로직

- `1 meter = 3.28084 feet`
- `1 meter = 1.09361 yard`
- feet/yard 간의 비율은 **meter 기준**으로 계산.
- 변환 비율은 `unit_converter/domain/unit_registry.py`에 **단일 정의** (SSOT).

### 품질 요구사항

- OCP를 만족하는 설계 — Registry 등록으로 단위 확장
- SRP를 만족하는 모듈 구성 — Parser / Registry / Converter / CLI 분리
- 입력 값 검증 (음수, 잘못된 형식, 없는 단위)
- Golden Master — REFACTOR 중 CLI 출력·오류 메시지 회귀 방지

상세 요구·추적: [docs/PRD.md](docs/PRD.md), [docs/TRACEABILITY.md](docs/TRACEABILITY.md), [docs/TEST_LOOP.md](docs/TEST_LOOP.md)

### 추가 요구사항 (2차 — 미구현)

- **설정 외부화** — 변환 비율을 외부 설정 파일(JSON/YAML)에서 로드 (`infrastructure/config_loader.py`)
- **동적 단위 등록** — `1 cubit = 0.4572 meter` 등록 후 즉시 변환·출력 대상 포함
- **출력 포맷 선택** — JSON / CSV / 표 형태 출력 (`app/output_formatter.py`)

---

## 생성형AI를 활용한 Activities (6 시간)

1. 문제 코드 및 기본 요구사항 분석 (0.5시간)
   - 기본 코드구조, 로직 이해
2. 기본 요구사항 및 품질 요구사항 구현 (2시간)
   - OCP를 만족하는 인터페이스 구현 
   - SRP를 만족하도록 클래스 구현 
   - 입력값 검증을 위한 구현
3. TC 구현 (0.5시간)
   - 단위변환 기능 검증 및 입력 값 검증 TC 작성 
4. 추가 요구사항 구현 (2시간)
   - 3개 요구사항 구현 및 TC 작성 
5. 회고 및 발표 (1시간)
   - 실습 목표와 달성도
   - AI를 어떻게 활용했나? 도움이 된 순간과 한계는?
   - TC를 추가해보면서 개선에 미친 영향, TC 작성 팁
   - 클린코드와 리팩토링에서 느낀 장점과 어려운점
