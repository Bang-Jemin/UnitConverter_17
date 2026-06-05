import difflib
import os
from pathlib import Path

_TESTS_DIR = Path(__file__).resolve().parent


def assert_matches_golden(actual: str, relative_path: str) -> None:
    approved_path = _TESTS_DIR / relative_path

    if os.environ.get("UPDATE_GOLDEN") == "1":
        approved_path.parent.mkdir(parents=True, exist_ok=True)
        approved_path.write_text(actual, encoding="utf-8")
        return

    if not approved_path.is_file():
        raise AssertionError(
            f"Golden file missing: {relative_path}. "
            "Run with UPDATE_GOLDEN=1 to create."
        )

    expected = approved_path.read_text(encoding="utf-8")
    if actual == expected:
        return

    diff = difflib.unified_diff(
        expected.splitlines(keepends=True),
        actual.splitlines(keepends=True),
        fromfile=f"approved/{relative_path}",
        tofile="actual",
    )
    raise AssertionError(
        f"Golden mismatch for {relative_path}:\n{''.join(diff)}"
    )
