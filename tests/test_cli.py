# Boundary / UI Track tests.

import pytest


def _require_cli_handler(test_id: str):
    try:
        from unit_converter.cli import handle_input
    except ImportError:
        pytest.fail(f"RED: {test_id} — handle_input API not implemented in unit_converter.cli")
    return handle_input


def test_missing_colon_rejects_with_format_error():
    """FR-05 / T-VAL-02"""
    handle_input = _require_cli_handler("T-VAL-02")
    result = handle_input("meter")
    assert result.ok is False
    assert result.error_kind == "format"
    assert result.output_lines == []


def test_non_numeric_value_rejects_with_number_error():
    """FR-05 / T-VAL-02"""
    handle_input = _require_cli_handler("T-VAL-02")
    result = handle_input("meter:abc")
    assert result.ok is False
    assert result.error_kind == "number"
    assert result.output_lines == []


def test_missing_unit_rejects_with_format_or_number_error():
    """FR-05 / T-VAL-02"""
    handle_input = _require_cli_handler("T-VAL-02")
    result = handle_input(":2.5")
    assert result.ok is False
    assert result.error_kind in ("format", "number")
    assert result.output_lines == []


def test_format_and_number_errors_are_distinguishable():
    """FR-05 / T-VAL-02"""
    handle_input = _require_cli_handler("T-VAL-02")
    format_result = handle_input("meter")
    number_result = handle_input("meter:abc")
    assert format_result.error_kind != number_result.error_kind


def test_negative_value_rejects_without_conversion():
    """FR-06 / T-VAL-01"""
    handle_input = _require_cli_handler("T-VAL-01")
    result = handle_input("meter:-1")
    assert result.ok is False
    assert result.output_lines == []


def test_negative_value_emits_rejection_message():
    """FR-06 / T-VAL-01"""
    handle_input = _require_cli_handler("T-VAL-01")
    result = handle_input("meter:-1")
    assert result.error_kind == "negative"
    assert result.message
    assert "negative" in result.message.lower()


def test_negative_value_does_not_raise_unhandled_exception():
    """FR-06 / T-VAL-01"""
    handle_input = _require_cli_handler("T-VAL-01")
    result = handle_input("meter:-1")
    assert result.ok is False
