# Domain / Logic Track tests.

import pytest

RATIO_FEET_PER_METER = 3.28084
RATIO_YARD_PER_METER = 1.09361


def _require_parse():
    try:
        from unit_converter.app.input_parser import parse
    except ImportError:
        pytest.fail("RED: T-PARSE-01 — parse API not implemented in unit_converter.app.input_parser")
    return parse


def _require_converter():
    try:
        from unit_converter.domain.converter import Converter
        from unit_converter.domain.unit_registry import UnitRegistry
    except ImportError:
        pytest.fail(
            "RED: T-CONV-01 — Converter/UnitRegistry API not implemented in unit_converter.domain"
        )
    registry = UnitRegistry.create_default()
    return Converter(registry)


def test_parse_meter_value_splits_unit_and_float():
    """FR-01 / T-PARSE-01"""
    parse = _require_parse()
    assert parse("meter:2.5") == ("meter", 2.5)


def test_parse_feet_value_splits_unit_and_float():
    """FR-01 / T-PARSE-01"""
    parse = _require_parse()
    assert parse("feet:8.2") == ("feet", 8.2)


def test_parse_yard_value_splits_unit_and_float():
    """FR-01 / T-PARSE-01"""
    parse = _require_parse()
    assert parse("yard:2.7") == ("yard", 2.7)


def test_parse_uses_first_colon_only():
    """FR-01 / T-PARSE-01"""
    parse = _require_parse()
    assert parse("meter:2.5:extra") == ("meter", 2.5)


def test_convert_meter_to_all_units():
    """FR-02 / T-CONV-01"""
    converter = _require_converter()
    results = converter.convert_all("meter", 2.5)
    assert results["meter"] == pytest.approx(2.5)
    assert results["feet"] == pytest.approx(2.5 * RATIO_FEET_PER_METER)
    assert results["yard"] == pytest.approx(2.5 * RATIO_YARD_PER_METER)


def test_convert_meter_feet_matches_readme_ratio():
    """FR-02 / T-CONV-01"""
    converter = _require_converter()
    results = converter.convert_all("meter", 2.5)
    assert results["feet"] == pytest.approx(2.5 * RATIO_FEET_PER_METER, rel=1e-4)


def test_convert_meter_yard_matches_readme_ratio():
    """FR-02 / T-CONV-01"""
    converter = _require_converter()
    results = converter.convert_all("meter", 2.5)
    assert results["yard"] == pytest.approx(2.5 * RATIO_YARD_PER_METER, rel=1e-4)


def test_convert_feet_to_all_units_sc1():
    """FR-03 / T-CONV-02"""
    converter = _require_converter()
    results = converter.convert_all("feet", 8.2)
    expected_meter = 8.2 / RATIO_FEET_PER_METER
    assert results["meter"] == pytest.approx(expected_meter, rel=1e-4)
    assert results["feet"] == pytest.approx(8.2)
    assert results["yard"] == pytest.approx(expected_meter * RATIO_YARD_PER_METER, rel=1e-4)


def test_convert_yard_to_all_units_sc1():
    """FR-03 / T-CONV-02"""
    converter = _require_converter()
    results = converter.convert_all("yard", 2.7)
    expected_meter = 2.7 / RATIO_YARD_PER_METER
    assert results["meter"] == pytest.approx(expected_meter, rel=1e-4)
    assert results["feet"] == pytest.approx(expected_meter * RATIO_FEET_PER_METER, rel=1e-4)
    assert results["yard"] == pytest.approx(2.7)


def test_feet_yard_conversion_via_meter_consistent():
    """FR-03 / T-CONV-02"""
    converter = _require_converter()
    results = converter.convert_all("feet", 8.2)
    yard_from_feet = results["yard"]
    yard_via_meter = (8.2 / RATIO_FEET_PER_METER) * RATIO_YARD_PER_METER
    assert yard_from_feet == pytest.approx(yard_via_meter, rel=1e-4)


def test_round_trip_meter_feet_meter():
    """FR-03 / T-CONV-02"""
    converter = _require_converter()
    forward = converter.convert_all("meter", 2.5)
    back = converter.convert_all("feet", forward["feet"])
    assert back["meter"] == pytest.approx(2.5, rel=1e-4)
