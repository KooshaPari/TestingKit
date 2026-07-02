"""Tests for mcp_qa.mocking.server — fake MCP server creation.

All tests are purely local; no real MCP server is contacted.
"""
from __future__ import annotations

from mcp_qa.mocking.server import (
    FakeMCPServer,
    create_default_mock_server,
)


def test_fake_mcp_server_constructible() -> None:
    """FakeMCPServer can be instantiated without arguments."""
    server = FakeMCPServer()
    assert hasattr(server, "start")
    assert hasattr(server, "stop")
    assert hasattr(server, "port")
    assert hasattr(server, "tools")


def test_fake_mcp_server_default_port() -> None:
    """Default port assignment for FakeMCPServer."""
    server = FakeMCPServer()
    assert isinstance(server.port, int)
    assert 1024 <= server.port <= 65535


def test_fake_mcp_server_with_tools() -> None:
    """FakeMCPServer accepts a pre-configured tool list."""
    tools = [
        {"name": "test_tool", "description": "A test tool", "inputSchema": {}},
    ]
    server = FakeMCPServer(tools=tools)
    assert len(server.tools) == 1
    assert server.tools[0]["name"] == "test_tool"


def test_create_default_mock_server() -> None:
    """Factory function returns a FakeMCPServer instance."""
    server = create_default_mock_server()
    assert isinstance(server, FakeMCPServer)
    assert len(server.tools) > 0  # default tool set is non-empty
