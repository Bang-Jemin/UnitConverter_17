# CLI entry point.

from dataclasses import dataclass, field

from unit_converter.app.input_parser import parse
from unit_converter.domain.converter import Converter
from unit_converter.domain.unit_registry import UnitRegistry


@dataclass
class HandleInputResult:
    ok: bool
    error_kind: str | None = None
    message: str | None = None
    output_lines: list[str] = field(default_factory=list)


def handle_input(raw: str) -> HandleInputResult:
    if ":" not in raw:
        return HandleInputResult(
            ok=False,
            error_kind="format",
            message="Invalid format. Use unit:value (ex: meter:2.5)",
        )

    unit, value_str = raw.split(":", 1)

    if not unit.strip():
        return HandleInputResult(
            ok=False,
            error_kind="format",
            message="Invalid format. Missing unit.",
        )

    try:
        value = float(value_str)
    except ValueError:
        return HandleInputResult(
            ok=False,
            error_kind="number",
            message=f"Invalid number: {value_str}",
        )

    if value < 0:
        return HandleInputResult(
            ok=False,
            error_kind="negative",
            message="Negative values are not allowed",
        )

    registry = UnitRegistry.create_default()
    converter = Converter(registry)
    unit_name, parsed_value = parse(raw)
    results = converter.convert_all(unit_name, parsed_value)
    output_lines = [
        f"{parsed_value} {unit_name} = {results[target]} {target}"
        for target in registry.all_units()
    ]
    return HandleInputResult(ok=True, output_lines=output_lines)
