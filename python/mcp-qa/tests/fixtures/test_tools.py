"""Tests for mcp_qa.fixtures — test fixture factories."""
from __future__ import annotations

from mcp_qa.fixtures.tools import create_tool_call, create_tool, create_text_delta_content


def test_create_tool_call_creates_dict() -> None:
    """create_tool_call returns a dict with the expected keys."""
    call = create_tool_call(name="my_tool", arguments={"key": "val"})
    assert call["name"] == "my_tool"
    assert call["arguments"]["key"] == "val"


def test_create_tool_has_name_and_input_schema() -> None:
    """create_tool returns a dict with name and inputSchema."""
    tool = create_tool(name="echo", description="echoes input")
    assert tool["name"] == "echo"
    assert "inputSchema" in tool


def test_create_text_delta_content_str() -> None:
    """create_text_delta_content returns a valid text content block."""
    content = create_text_delta_content("hello")
    assert content["type"] == "text"
    assert content["text"] == "hello"
