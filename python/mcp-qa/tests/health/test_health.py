"""Tests for mcp_qa.health — Health check utilities."""
from __future__ import annotations

import pytest
from mcp_qa.health import MCPQAHealthCheck, check_server_health, check_tool_health


class TestMCPQAHealthCheck:
    """Unit tests for the MCPQAHealthCheck dataclass."""

    def test_defaults(self) -> None:
        check = MCPQAHealthCheck(server_name="my-server")
        assert check.server_name == "my-server"
        assert check.status == "unknown"
        assert check.details == {}
        assert check.duration_ms is None

    def test_with_all_fields(self) -> None:
        check = MCPQAHealthCheck(
            server_name="srv",
            status="healthy",
            details={"uptime": "5m"},
            duration_ms=42,
        )
        assert check.server_name == "srv"
        assert check.status == "healthy"
        assert check.details["uptime"] == "5m"
        assert check.duration_ms == 42


class TestCheckServerHealth:
    """Unit tests for check_server_health."""

    def test_returns_health_check(self) -> None:
        result = check_server_health("my-server")
        assert isinstance(result, MCPQAHealthCheck)

    def test_reports_server_name(self) -> None:
        result = check_server_health("test-srv")
        assert result.server_name == "test-srv"


class TestCheckToolHealth:
    """Unit tests for check_tool_health."""

    def test_returns_health_check(self) -> None:
        result = check_tool_health("my-server", "my-tool")
        assert isinstance(result, MCPQAHealthCheck)

    def test_reports_names(self) -> None:
        result = check_tool_health("s", "t")
        assert result.server_name == "s"
        assert "t" in str(result.details)

    def test_status_is_string(self) -> None:
        result = check_tool_health("s", "t")
        assert isinstance(result.status, str)
