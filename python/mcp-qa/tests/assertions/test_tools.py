"""Tests for mcp_qa.assertions — tool call assertion utilities."""
from __future__ import annotations

import pytest
from mcp_qa.assertions.tools import (
    assert_tool_call_shape,
    assert_tool_call_has_argument,
    assert_tool_not_called,
    assert_tool_called_exactly,
    assert_no_unexpected_tool_calls,
)


class TestAssertToolCallShape:
    """Tests for assert_tool_call_shape."""

    def test_valid_call(self) -> None:
        call = {"name": "test", "arguments": {"a": 1}}
        assert_tool_call_shape(call)

    def test_missing_name_raises(self) -> None:
        with pytest.raises(AssertionError):
            assert_tool_call_shape({"arguments": {}})

    def test_missing_arguments_raises(self) -> None:
        with pytest.raises(AssertionError):
            assert_tool_call_shape({"name": "t"})

    def test_name_not_string_raises(self) -> None:
        with pytest.raises(AssertionError):
            assert_tool_call_shape({"name": 42, "arguments": {}})

    def test_arguments_not_dict_raises(self) -> None:
        with pytest.raises(AssertionError):
            assert_tool_call_shape({"name": "t", "arguments": "bad"})


class TestAssertToolCallHasArgument:
    """Tests for assert_tool_call_has_argument."""

    def test_argument_present(self) -> None:
        call = {"name": "t", "arguments": {"key": "val"}}
        assert_tool_call_has_argument(call, "key")

    def test_argument_missing_raises(self) -> None:
        with pytest.raises(AssertionError):
            assert_tool_call_has_argument({"name": "t", "arguments": {}}, "key")

    def test_value_match(self) -> None:
        call = {"name": "t", "arguments": {"count": 42}}
        assert_tool_call_has_argument(call, "count", expected_value=42)

    def test_value_mismatch_raises(self) -> None:
        with pytest.raises(AssertionError):
            assert_tool_call_has_argument(
                {"name": "t", "arguments": {"count": 42}}, "count", expected_value=99
            )


class TestToolCallCounting:
    """Tests for assert_tool_not_called and assert_tool_called_exactly."""

    def test_tool_not_called_with_empty(self) -> None:
        assert_tool_not_called([], "any-tool")

    def test_tool_not_called_with_different(self) -> None:
        assert_tool_not_called(
            [{"name": "other", "arguments": {}}], "any-tool"
        )

    def test_tool_called_exactly_pass(self) -> None:
        calls = [{"name": "t", "arguments": {}}]
        assert_tool_called_exactly(calls, "t", 1)

    def test_tool_called_exactly_wrong_count_raises(self) -> None:
        calls = [{"name": "t", "arguments": {}}, {"name": "t", "arguments": {}}]
        with pytest.raises(AssertionError):
            assert_tool_called_exactly(calls, "t", 1)

    def test_tool_called_exactly_zero(self) -> None:
        assert_tool_called_exactly([], "t", 0)


class TestNoUnexpectedToolCalls:
    """Tests for assert_no_unexpected_tool_calls."""

    def test_all_expected(self) -> None:
        calls = [{"name": "a", "arguments": {}}, {"name": "b", "arguments": {}}]
        assert_no_unexpected_tool_calls(calls, ["a", "b"])

    def test_unexpected_raises(self) -> None:
        calls = [{"name": "a", "arguments": {}}, {"name": "unexpected", "arguments": {}}]
        with pytest.raises(AssertionError):
            assert_no_unexpected_tool_calls(calls, ["a"])
