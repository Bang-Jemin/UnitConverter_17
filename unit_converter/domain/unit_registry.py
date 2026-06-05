# Unit registration and lookup (OCP core).

RATIO_FEET_PER_METER = 3.28084
RATIO_YARD_PER_METER = 1.09361


class UnitRegistry:
    def __init__(self) -> None:
        self._meters_per_unit: dict[str, float] = {}

    @classmethod
    def create_default(cls) -> "UnitRegistry":
        registry = cls()
        registry.register("meter", 1.0)
        registry.register("feet", 1.0 / RATIO_FEET_PER_METER)
        registry.register("yard", 1.0 / RATIO_YARD_PER_METER)
        return registry

    def register(self, name: str, meters_per_unit: float) -> None:
        self._meters_per_unit[name] = meters_per_unit

    def all_units(self) -> list[str]:
        return list(self._meters_per_unit.keys())

    def get_meters_per_unit(self, name: str) -> float:
        return self._meters_per_unit[name]
