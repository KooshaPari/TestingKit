"""Tests for mcp_qa.mocking.tools — tool call mocking.
"""
from __future__ import annotations

from mcp_qa.mocking.tools import (
    MockToolCallManager,
    create_mock_tool_call,
)


def test_mock_tool_call_manager_create() -> None:
    """MockToolCallManager can be instantiated."""
    mgr = MockToolCallManager()
    assert hasattr(mgr, "register_call")
    assert hasattr(mgr, "get_call")
    assert hasattr(mgr, "reset")


def test_create_mock_tool_call_returns_dict() -> None:
    """create_mock_tool_call returns a correctly shaped dict."""
    call = create_mock_tool_call("test_tool", {"arg1": "val1"})
    assert isinstance(call, dict)
    assert call["name"] == "test_tool"
    assert call["arguments"]["arg1"] == "val1"


def test_mock_tool_call_manager_round_trip() -> None:
    """Register and retrieve a mock call."""
    mgr = MockToolCallManager()
    call = create_mock_tool_call("round_trip", {"x": 1})
    mgr.register_call(call)
    retrieved = mgr.get_call("round_trip")
    assert retrieved is not None
    assert retrieved["arguments"]["x"] == 1


def test_mock_tool_call_manager_reset() -> None:
    """Reset clears all registered calls."""
    mgr = MockToolCallManager()
    mgr.register_call(create_mock_tool_call("a", {}))
    mgr.reset()
    assert mgr.get_call("a") is None
