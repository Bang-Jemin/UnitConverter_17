# Parse "unit:value" input strings.


def parse(raw: str) -> tuple[str, float]:
    unit, value_str = raw.split(":", 1)
    value_token, _, _ = value_str.partition(":")
    value = float(value_token)
    return (unit, value)


def parse_input(
    raw: str,
) -> tuple[bool, str | None, float | None, str | None, str | None]:
    if ":" not in raw:
        return (
            False,
            None,
            None,
            "format",
            "Invalid format. Use unit:value (ex: meter:2.5)",
        )

    unit, value_str = raw.split(":", 1)

    if not unit.strip():
        return (False, None, None, "format", "Invalid format. Missing unit.")

    try:
        value = float(value_str)
    except ValueError:
        return (False, None, None, "number", f"Invalid number: {value_str}")

    if value < 0:
        return (False, None, None, "negative", "Negative values are not allowed")

    return (True, unit, value, None, None)
