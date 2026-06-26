"""Property-based tests for pheno_testing_cli.property_testing.

Uses Hypothesis to verify that the helpers are themselves well-behaved:
strategies produce valid samples, and the property templates assert correct
invariants on arbitrary inputs.
"""
from __future__ import annotations

import json
import string

import pytest
from hypothesis import HealthCheck, assume, given, settings, strategies as st

from pheno_testing_cli.property_testing import (
    ascii_identifier,
    bounded_string,
    hex_color,
    idempotent_property,
    monotonic_property,
    roundtrip_property,
    safe_int,
    small_dict,
)

# Hypothesis can produce empty bytes-like or pathological strings in CI; keep
# deadline moderate to avoid flakiness on slow shared runners.
settings.register_profile(
    "ci",
    max_examples=50,
    deadline=None,
    suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much],
)
settings.load_profile("ci")


# ---------------------------------------------------------------------------
# Strategy tests — verify that the strategies produce values in their domains.
# ---------------------------------------------------------------------------


@given(ascii_identifier(min_size=1, max_size=32))
def test_ascii_identifier_matches_pattern(value: str) -> None:
    assert 1 <= len(value) <= 32
    assert value[0] in string.ascii_letters + "_"
    assert all(ch in string.ascii_letters + string.digits + "_" for ch in value)


@given(ascii_identifier())
def test_ascii_identifier_never_empty(value: str) -> None:
    # Default min_size=1 so this should always hold.
    assert value, "ascii_identifier() returned empty string"


@given(bounded_string(min_size=0, max_size=64))
def test_bounded_string_within_size(value: str) -> None:
    assert 0 <= len(value) <= 64


@given(hex_color())
def test_hex_color_format(value: str) -> None:
    assert len(value) == 7
    assert value.startswith("#")
    assert all(ch in string.hexdigits.lower() for ch in value[1:])


@given(safe_int())
def test_safe_int_in_safe_range(value: int) -> None:
    assert -(2**31) <= value <= 2**31 - 1


@given(small_dict(max_size=8))
def test_small_dict_keys_are_identifiers(value: dict[str, str]) -> None:
    for k in value:
        assert k, "small_dict produced empty key"
        assert k[0] in string.ascii_letters + "_"


# ---------------------------------------------------------------------------
# Property template tests — verify the templates assert the right invariants.
# ---------------------------------------------------------------------------


@given(st.integers(min_value=-(2**20), max_value=2**20))
def test_roundtrip_property_passes_for_identity(value: int) -> None:
    # encode = decode = identity is trivially a round-trip.
    roundtrip_property(value, encode=lambda x: x, decode=lambda x: x)


@given(st.lists(st.integers(), min_size=0, max_size=50))
def test_roundtrip_property_passes_for_json(value: list[int]) -> None:
    roundtrip_property(value, encode=list, decode=list)
    roundtrip_property(value, encode=lambda v: json.dumps(v), decode=json.loads)


def test_roundtrip_property_fails_on_broken_roundtrip() -> None:
    # encode adds 1; decode is identity -> mismatch should be detected.
    with pytest.raises(AssertionError, match="Round-trip failed"):
        roundtrip_property(0, encode=lambda x: x + 1, decode=lambda x: x)


@given(st.integers(), st.integers())
def test_idempotent_property_passes_for_abs(a: int, b: int) -> None:
    # abs() is idempotent: abs(abs(x)) == abs(x).
    idempotent_property(a, abs)
    idempotent_property(b, abs)


def test_idempotent_property_fails_for_non_idempotent_fn() -> None:
    # increment is NOT idempotent.
    with pytest.raises(AssertionError, match="Idempotency violated"):
        idempotent_property(0, lambda x: x + 1)


@given(st.integers(min_value=0, max_value=100), st.integers(min_value=0, max_value=100))
def test_monotonic_property_passes_for_sorted(a: int, b: int) -> None:
    assume(a <= b)
    monotonic_property(a, b, lambda x: x, less=True)


def test_monotonic_property_fails_when_violated() -> None:
    # For a < b, fn(a)=b, fn(b)=a violates monotonicity.
    with pytest.raises(AssertionError, match="Expected"):
        monotonic_property(0, 1, lambda x: 1 - x, less=True)


# ---------------------------------------------------------------------------
# Meta — confirm the module imports cleanly without side effects.
# ---------------------------------------------------------------------------


def test_module_imports() -> None:
    import pheno_testing_cli.property_testing as mod

    assert hasattr(mod, "roundtrip_property")
    assert hasattr(mod, "idempotent_property")
    assert hasattr(mod, "monotonic_property")
    assert hasattr(mod, "ascii_identifier")
