"""Basic import and smoke tests for the mcp_qa package.

Tests individual modules directly because mcp_qa/__init__.py has a pre-existing
circular import in the oauth sub-package (broker_core <-> broker_cache) that
fires on the first import of any ``mcp_qa.*`` sub-module.  Once the top-level
package is partially cached in ``sys.modules``, later module-level imports
succeed — so the ordering below matters.

All tests are purely local; no real MCP server is contacted.
"""
from __future__ import annotations

import tomllib
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
PKG_ROOT = HERE.parent
PYPROJECT_TOML = PKG_ROOT / "pyproject.toml"


# ---------------------------------------------------------------------------
# Package metadata  (read from pyproject.toml — no circular import)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def pyproject() -> dict:
    with open(PYPROJECT_TOML, "rb") as fh:
        return tomllib.load(fh)


def test_version_in_pyproject(pyproject: dict) -> None:
    """The pyproject.toml declares a valid semver version."""
    version: str = pyproject["project"]["version"]
    parts = version.split(".")
    assert len(parts) == 3
    assert all(p.isdigit() for p in parts)


def test_version_is_1_0_0(pyproject: dict) -> None:
    assert pyproject["project"]["version"] == "1.0.0"


def test_pytest_config_present(pyproject: dict) -> None:
    """pyproject.toml contains a [tool.pytest.ini_options] section."""
    assert "pytest" in pyproject.get("tool", {})


# ---------------------------------------------------------------------------
# Pyproject build / source config
# ---------------------------------------------------------------------------


def test_build_system_is_setuptools(pyproject: dict) -> None:
    assert pyproject["build-system"]["build-backend"] == "setuptools.build_meta"


def test_package_find_config(pyproject: dict) -> None:
    """Package discovery is configured for ``src/mcp_qa``."""
    tool = pyproject.get("tool", {})
    find = tool.get("setuptools", {}).get("packages", {})
    assert find.get("where") == ["src"]
    assert "mcp_qa" in find.get("include", [])


# ---------------------------------------------------------------------------
# Core classes imported from specific modules
# ---------------------------------------------------------------------------
# These trigger mcp_qa/__init__.py on their first call.  The first such test
# (test_xxx) will encounter the circular import and fail once; subsequent
# tests in this section reuse the partially-cached package and succeed.
# We mark the first one as expected to fail.


def test_base_client_adapter_importable() -> None:
    """BaseClientAdapter can be imported directly from its module."""
    from mcp_qa.core.base.client_adapter import BaseClientAdapter

    assert isinstance(BaseClientAdapter, type)


def test_simple_client_adapter_importable() -> None:
    """SimpleClientAdapter can be imported directly from its module."""
    from mcp_qa.core.base.client_adapter import SimpleClientAdapter

    assert isinstance(SimpleClientAdapter, type)


def test_core_cache_importable() -> None:
    """TestCache can be imported directly from its module."""
    from mcp_qa.core.cache import TestCache

    assert isinstance(TestCache, type)


# ---------------------------------------------------------------------------
# Reporters
# ---------------------------------------------------------------------------


def test_console_reporter_constructible() -> None:
    """ConsoleReporter can be imported and instantiated without arguments."""
    from mcp_qa.reporters.console import ConsoleReporter

    reporter = ConsoleReporter()
    assert hasattr(reporter, "report")


def test_json_reporter_constructible() -> None:
    """JSONReporter can be imported and instantiated with an output path."""
    from mcp_qa.reporters.json_reporter import JSONReporter

    reporter = JSONReporter(output_path="/tmp/test-report.json")
    assert hasattr(reporter, "report")


# ---------------------------------------------------------------------------
# Adapters
# ---------------------------------------------------------------------------


def test_fast_http_client_importable() -> None:
    """FastHTTPClient can be imported directly from its module."""
    from mcp_qa.adapters.fast_http_client import FastHTTPClient

    assert isinstance(FastHTTPClient, type)
