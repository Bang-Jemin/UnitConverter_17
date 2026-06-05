# Parse "unit:value" input strings.


def parse(raw: str) -> tuple[str, float]:
    unit, value_str = raw.split(":", 1)
    value = float(value_str.split(":", 1)[0])
    return (unit, value)
