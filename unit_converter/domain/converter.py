# Conversion calculation between registered units.

from unit_converter.domain.unit_registry import UnitRegistry


class Converter:
    def __init__(self, registry: UnitRegistry) -> None:
        self._registry = registry

    def convert_all(self, unit: str, value: float) -> dict[str, float]:
        meter_value = value * self._registry.get_meters_per_unit(unit)
        return {
            name: meter_value / self._registry.get_meters_per_unit(name)
            for name in self._registry.all_units()
        }
