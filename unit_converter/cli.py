# CLI entry point.

from dataclasses import dataclass, field

from unit_converter.app.input_parser import parse_input
from unit_converter.app.output_formatter import format_text_lines
from unit_converter.domain.converter import Converter
from unit_converter.domain.unit_registry import UnitRegistry


@dataclass
class HandleInputResult:
    ok: bool
    error_kind: str | None = None
    message: str | None = None
    output_lines: list[str] = field(default_factory=list)


def handle_input(raw: str) -> HandleInputResult:
    ok, unit_name, parsed_value, error_kind, message = parse_input(raw)
    if not ok:
        return HandleInputResult(ok=False, error_kind=error_kind, message=message)

    registry = UnitRegistry.create_default()
    converter = Converter(registry)
    results = converter.convert_all(unit_name, parsed_value)
    output_lines = format_text_lines(
        unit_name, parsed_value, results, registry.all_units()
    )
    return HandleInputResult(ok=True, output_lines=output_lines)
