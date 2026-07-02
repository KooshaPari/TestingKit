"""Tests for mcp_qa.logging — Minimal structured logging."""
from __future__ import annotations

from mcp_qa.logging import get_logger


def test_get_logger_returns_logger() -> None:
    """get_logger returns a standard library logger."""
    logger = get_logger("test")
    assert logger.name == "test"


def test_get_logger_has_info() -> None:
    """Returned logger has the expected standard methods."""
    logger = get_logger("test")
    assert hasattr(logger, "info")
    assert hasattr(logger, "warning")
    assert hasattr(logger, "error")
    assert hasattr(logger, "debug")
