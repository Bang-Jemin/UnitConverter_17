# Format conversion results as json, csv, or table.


def format_text_lines(
    source_unit: str,
    source_value: float,
    results: dict[str, float],
    unit_order: list[str],
) -> list[str]:
    return [
        f"{source_value} {source_unit} = {results[target]} {target}"
        for target in unit_order
    ]
