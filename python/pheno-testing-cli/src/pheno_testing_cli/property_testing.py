"""Property-based testing helpers built on Hypothesis.

Provides reusable strategies and pre-built property tests for common invariants
(idempotency, round-trip, monotonicity, ordering) used across the Phenotype
fleet. Designed as a thin layer over Hypothesis so callers can compose the
strategies with their domain types.

Usage:
    from hypothesis import given, strategies as st
    from pheno_testing_cli.property_testing import (
        roundtrip_property, idempotent_property, ascii_identifier,
    )

    @given(st.builds(MyType, ...))
    def test_roundtrip(value: MyType) -> None:
        roundtrip_property(value, serializer, deserializer)

    @given(ascii_identifier())
    def test_id_parsing(s: str) -> None:
        # ...
"""
from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

from hypothesis import assume, strategies as st

T = TypeVar("T")

__all__ = [
    "ascii_identifier",
    "bounded_string",
    "hex_color",
    "idempotent_property",
    "monotonic_property",
    "roundtrip_property",
    "safe_int",
    "small_dict",
]


# ---------------------------------------------------------------------------
# Strategies — composable Hypothesis strategies for common domain types.
# ---------------------------------------------------------------------------


def ascii_identifier(min_size: int = 1, max_size: int = 64) -> st.SearchStrategy[str]:
    """Strategy producing ASCII identifiers matching ``[A-Za-z_][A-Za-z0-9_]*``.

    Useful for token / slug / variable-name properties.
    """
    head = st.sampled_from(list("_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"))
    tail = st.sampled_from(
        list("_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    )
    return st.builds(
        lambda h, rest: h + "".join(rest),
        head,
        st.lists(tail, min_size=max(0, min_size - 1), max_size=max(0, max_size - 1)),
    )


def bounded_string(min_size: int = 0, max_size: int = 256) -> st.SearchStrategy[str]:
    """Strategy producing printable ASCII strings within a size bound."""
    return st.text(
        alphabet=st.characters(
            whitelist_categories=("L", "N", "P", "Zs"),
            whitelist_characters="\t\n",
        ),
        min_size=min_size,
        max_size=max_size,
    )


def hex_color() -> st.SearchStrategy[str]:
    """Strategy producing ``#rrggbb`` hex color strings."""
    return st.builds(
        lambda r, g, b: "#{:02x}{:02x}{:02x}".format(r, g, b),
        st.integers(min_value=0, max_value=255),
        st.integers(min_value=0, max_value=255),
        st.integers(min_value=0, max_value=255),
    )


def small_dict(
    max_size: int = 10,
) -> st.SearchStrategy[dict[str, str]]:
    """Strategy producing small string→string dicts (good for serialization tests)."""
    return st.dictionaries(
        keys=ascii_identifier(min_size=1, max_size=16),
        values=bounded_string(max_size=32),
        max_size=max_size,
    )


def safe_int(min_value: int = -(2**31), max_value: int = 2**31 - 1) -> st.SearchStrategy[int]:
    """Strategy producing safe-range integers (no overflow surprises)."""
    return st.integers(min_value=min_value, max_value=max_value)


# ---------------------------------------------------------------------------
# Property templates — pre-built assertions for common invariants.
# ---------------------------------------------------------------------------


def roundtrip_property(
    value: T,
    encode: Callable[[T], object],
    decode: Callable[[object], T],
) -> None:
    """Assert that ``decode(encode(value)) == value``.

    Args:
        value: The original value.
        encode: Serialization function (returns an intermediate representation).
        decode: Inverse of ``encode``.

    Raises:
        AssertionError: If the round-trip fails.
    """
    assume(value is not None)
    intermediate = encode(value)
    assume(intermediate is not None)
    decoded = decode(intermediate)
    assert decoded == value, (
        f"Round-trip failed: {value!r} -> {intermediate!r} -> {decoded!r}"
    )


def idempotent_property(value: T, fn: Callable[[T], T]) -> None:
    """Assert that ``fn(fn(value)) == fn(value)``.

    Args:
        value: The input value.
        fn: Operation expected to be idempotent.

    Raises:
        AssertionError: If applying ``fn`` twice produces a different result.
    """
    once = fn(value)
    twice = fn(once)
    assert once == twice, f"Idempotency violated: fn({value!r})={once!r} -> fn(once)={twice!r}"


def monotonic_property(
    a: T,
    b: T,
    fn: Callable[[T], float],
    *,
    less: bool = True,
) -> None:
    """Assert monotonicity of ``fn`` between ``a`` and ``b``.

    Args:
        a: First input.
        b: Second input (``a <= b`` if ``less=True``, else ``a >= b``).
        fn: Function whose output should respect the order.
        less: If ``True``, assert ``fn(a) <= fn(b)``; else ``fn(a) >= fn(b)``.

    Raises:
        AssertionError: If the monotonicity invariant is violated.
    """
    fa, fb = fn(a), fn(b)
    if less:
        assert fa <= fb, f"Expected {fa} <= {fb} (a={a!r}, b={b!r})"
    else:
        assert fa >= fb, f"Expected {fa} >= {fb} (a={a!r}, b={b!r})"
