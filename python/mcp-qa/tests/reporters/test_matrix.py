"""Tests for FunctionalityMatrixReporter — coverage mapping and result lookup.

Tests the pure-function ``_find_test_result()`` method, default tool
capabilities structure, and custom configuration.
"""

from __future__ import annotations

import pytest

from mcp_qa.reporters.matrix import FunctionalityMatrixReporter


# ---------------------------------------------------------------------------
# _find_test_result  (pure function)
# ---------------------------------------------------------------------------


def _result_dicts() -> dict:
    """Helper: returns a ``results_by_test`` dict keyed by test name."""
    return {
        "test_workspace_list": {
            "test_name": "test_workspace_list",
            "tool_name": "workspace_tool",
            "success": True,
            "duration_ms": 100,
        },
        "test_entity_create": {
            "test_name": "test_entity_create",
            "tool_name": "entity_tool",
            "success": False,
            "duration_ms": 50,
        },
        "test_query_search": {
            "test_name": "test_query_search",
            "tool_name": "query_tool",
            "success": True,
            "duration_ms": 75,
        },
    }


class TestFindTestResult:
    """Tests for ``_find_test_result()``."""

    def test_finds_by_operation_name(self) -> None:
        """Operation name present in a test name is found."""
        reporter = FunctionalityMatrixReporter("/tmp/never_written.md")
        results = _result_dicts()
        match = reporter._find_test_result(results, "workspace_tool", "list")
        assert match is not None
        assert match["test_name"] == "test_workspace_list"

    def test_returns_none_when_no_match(self) -> None:
        """When no test name contains the operation name, returns None."""
        reporter = FunctionalityMatrixReporter("/tmp/never_written.md")
        results = _result_dicts()
        match = reporter._find_test_result(results, "workspace_tool", "nonexistent_op")
        assert match is None

    def test_empty_tool_name_searches_all(self) -> None:
        """An empty tool_name string matches across all tools."""
        reporter = FunctionalityMatrixReporter("/tmp/never_written.md")
        results = _result_dicts()
        match = reporter._find_test_result(results, "", "search")
        assert match is not None
        assert match["tool_name"] == "query_tool"

    def test_tool_name_filters_correctly(self) -> None:
        """When tool_name is specified, results from other tools are
        excluded."""
        reporter = FunctionalityMatrixReporter("/tmp/never_written.md")
        results = _result_dicts()
        # "create" exists in entity_tool but the query is for workspace_tool
        match = reporter._find_test_result(results, "workspace_tool", "create")
        assert match is None

    def test_case_insensitive_matching(self) -> None:
        """Matching is case-insensitive for both test name and operation
        name."""
        reporter = FunctionalityMatrixReporter("/tmp/never_written.md")
        results = _result_dicts()
        match = reporter._find_test_result(results, "", "LIST")
        assert match is not None
        assert match["test_name"] == "test_workspace_list"


# ---------------------------------------------------------------------------
# DEFAULT_TOOL_CAPABILITIES  (data structure)
# ---------------------------------------------------------------------------


class TestDefaultCapabilities:
    """Structural validation of ``DEFAULT_TOOL_CAPABILITIES``."""

    def test_has_expected_tools(self) -> None:
        """Default capabilities include the five expected tools."""
        reporter = FunctionalityMatrixReporter("/tmp/never_written.md")
        caps = reporter.tool_capabilities
        expected = {"workspace_tool", "entity_tool", "query_tool",
                     "relationship_tool", "workflow_tool"}
        assert set(caps.keys()) == expected

    def test_each_tool_has_description(self) -> None:
        """Every tool entry has a non-empty description."""
        reporter = FunctionalityMatrixReporter("/tmp/never_written.md")
        for name, info in reporter.tool_capabilities.items():
            assert "description" in info, f"{name} missing description"
            assert info["description"]

    def test_each_tool_has_operations(self) -> None:
        """Every tool entry has a non-empty operations dict."""
        reporter = FunctionalityMatrixReporter("/tmp/never_written.md")
        for name, info in reporter.tool_capabilities.items():
            assert "operations" in info, f"{name} missing operations"
            assert info["operations"]

    def test_each_operation_has_required_keys(self) -> None:
        """Every operation entry includes feature, user_story, data_items,
        and assertions."""
        reporter = FunctionalityMatrixReporter("/tmp/never_written.md")
        for tool_name, tool_info in reporter.tool_capabilities.items():
            for op_name, op_info in tool_info["operations"].items():
                assert "feature" in op_info, f"{tool_name}/{op_name} missing feature"
                assert "user_story" in op_info, f"{tool_name}/{op_name} missing user_story"
                assert "data_items" in op_info, f"{tool_name}/{op_name} missing data_items"
                assert "assertions" in op_info, f"{tool_name}/{op_name} missing assertions"

    def test_default_capabilities_are_not_mutated(self) -> None:
        """Instantiating with custom caps doesn't affect the class-level
        DEFAULT."""
        caps_before = len(FunctionalityMatrixReporter.DEFAULT_TOOL_CAPABILITIES)
        custom = {"custom_tool": {"description": "x", "operations": {}}}
        FunctionalityMatrixReporter("/tmp/never_written.md", tool_capabilities=custom)
        assert len(FunctionalityMatrixReporter.DEFAULT_TOOL_CAPABILITIES) == caps_before


# ---------------------------------------------------------------------------
# Custom capabilities
# ---------------------------------------------------------------------------


class TestCustomCapabilities:
    """Tests with custom (non-default) tool capabilities."""

    def test_custom_capabilities_override_defaults(self) -> None:
        """Custom tool_capabilities replaces DEFAULT_TOOL_CAPABILITIES."""
        custom = {
            "my_tool": {
                "description": "My custom tool",
                "operations": {
                    "do_thing": {
                        "feature": "Do a thing",
                        "user_story": "As a user, I want to do a thing",
                        "data_items": ["item1"],
                        "assertions": ["Does the thing"],
                    },
                },
            },
        }
        reporter = FunctionalityMatrixReporter("/tmp/never_written.md",
                                                tool_capabilities=custom)
        assert "my_tool" in reporter.tool_capabilities
        assert "workspace_tool" not in reporter.tool_capabilities
        assert reporter.tool_capabilities["my_tool"]["operations"]["do_thing"]["feature"] == "Do a thing"
