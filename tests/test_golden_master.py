# Golden Master — approved CLI output contracts (REFACTOR safety net).

from unit_converter.cli import handle_input

from tests._approval import assert_matches_golden


def _capture_success_output(raw: str) -> str:
    result = handle_input(raw)
    assert result.ok is True, f"Expected success for {raw!r}, got: {result.message}"
    return "\n".join(result.output_lines) + "\n"


def test_gm01_meter_2_5_success_output():
    """GM-01 / FR-02, OUT-01, OUT-02, SC-1 / T-CONV-01"""
    actual = _capture_success_output("meter:2.5")
    assert_matches_golden(actual, "golden/GM-01_meter_2_5.approved.txt")


def test_gm02_feet_8_2_success_output():
    """GM-02 / FR-03, OUT-01, OUT-03, SC-1 / T-CONV-02"""
    actual = _capture_success_output("feet:8.2")
    assert_matches_golden(actual, "golden/GM-02_feet_8_2.approved.txt")


def _capture_error_output(raw: str) -> str:
    result = handle_input(raw)
    assert result.ok is False, f"Expected error for {raw!r}, got success output"
    assert result.output_lines == []
    return f"error_kind: {result.error_kind}\nmessage: {result.message}\n"


def test_gm03_yard_2_7_success_output():
    """GM-03 / FR-03, OUT-01, OUT-03, SC-1 / T-CONV-02"""
    actual = _capture_success_output("yard:2.7")
    assert_matches_golden(actual, "golden/GM-03_yard_2_7.approved.txt")


def test_gm04_meter_missing_colon_format_error():
    """GM-04 / FR-05, ERR-01, SC-3 / T-VAL-02"""
    actual = _capture_error_output("meter")
    assert_matches_golden(actual, "golden/GM-04_meter_format_error.approved.txt")


def test_gm05_meter_abc_number_error():
    """GM-05 / FR-05, ERR-02, SC-3 / T-VAL-02"""
    actual = _capture_error_output("meter:abc")
    assert_matches_golden(actual, "golden/GM-05_meter_abc_number_error.approved.txt")


def test_gm06_missing_unit_format_error():
    """GM-06 / FR-05, ERR-01, SC-3 / T-VAL-02"""
    actual = _capture_error_output(":2.5")
    assert_matches_golden(actual, "golden/GM-06_missing_unit_format_error.approved.txt")


def test_gm07_meter_negative_rejection():
    """GM-07 / FR-06, ERR-04, SC-2 / T-VAL-01"""
    actual = _capture_error_output("meter:-1")
    assert_matches_golden(actual, "golden/GM-07_meter_negative_rejection.approved.txt")
