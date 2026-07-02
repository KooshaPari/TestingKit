"""Tests for DetailedErrorReporter — error suggestion matching and known issues.

Tests the pure-function ``_get_suggestion()`` method and
``add_known_issue()`` without any console I/O or Rich formatting.
"""

from __future__ import annotations

import pytest

from mcp_qa.reporters.error_detail import DetailedErrorReporter


# ---------------------------------------------------------------------------
# _get_suggestion  (case-insensitive pattern matching)
# ---------------------------------------------------------------------------


@pytest.fixture
def reporter() -> DetailedErrorReporter:
    """A DetailedErrorReporter with Rich disabled (no console I/O)."""
    return DetailedErrorReporter(verbose=True, use_rich=False)


class TestGetSuggestion:
    """Tests for ``_get_suggestion()`` — matches error strings against
    known patterns."""

    def test_matches_connection_refused(self, reporter: DetailedErrorReporter) -> None:
        """'Connection refused' patterns return the MCP Server Connection
        suggestion."""
        suggestion = reporter._get_suggestion("Connection refused: unable to connect")
        assert suggestion is not None
        assert suggestion["title"] == "MCP Server Connection"
        assert "Unable to connect" in suggestion["description"]

    def test_matches_permission_denied(self, reporter: DetailedErrorReporter) -> None:
        """'Permission denied' patterns return the Authentication Error
        suggestion."""
        suggestion = reporter._get_suggestion("Permission denied: access token invalid")
        assert suggestion is not None
        assert suggestion["title"] == "Authentication Error"

    def test_matches_timeout(self, reporter: DetailedErrorReporter) -> None:
        """'Timeout' in the error message returns the Request Timeout
        suggestion."""
        suggestion = reporter._get_suggestion("Request timed out after 30s")
        assert suggestion is not None
        assert suggestion["title"] == "Request Timeout"
        assert "timed out" in suggestion["fix"].lower()

    def test_matches_known_issue_case_insensitive(self, reporter: DetailedErrorReporter) -> None:
        """Pattern matching is case-insensitive."""
        suggestion = reporter._get_suggestion("not null constraint failed: updated_by")
        assert suggestion is not None
        assert suggestion["title"] == "RLS Policy Constraint"

    def test_unknown_error_returns_none(self, reporter: DetailedErrorReporter) -> None:
        """An error string that matches no known pattern returns None."""
        suggestion = reporter._get_suggestion("Some completely unknown error occurred")
        assert suggestion is None

    def test_matches_db_constraint_violation(self, reporter: DetailedErrorReporter) -> None:
        """'DB_CONSTRAINT_VIOLATION' literal matches the first known issue
        entry."""
        suggestion = reporter._get_suggestion("DB_CONSTRAINT_VIOLATION on table users")
        assert suggestion is not None
        assert suggestion["title"] == "Database Constraint Violation"

    def test_matches_invalid_json(self, reporter: DetailedErrorReporter) -> None:
        """'Invalid JSON' returns the JSON Parse Error suggestion."""
        suggestion = reporter._get_suggestion("Invalid JSON response from server")
        assert suggestion is not None
        assert suggestion["title"] == "JSON Parse Error"

    def test_matches_http_404(self, reporter: DetailedErrorReporter) -> None:
        """'404' in the error string returns Resource Not Found."""
        suggestion = reporter._get_suggestion("HTTP 404: /api/tools not found")
        assert suggestion is not None
        assert suggestion["title"] == "Resource Not Found"

    def test_matches_http_500(self, reporter: DetailedErrorReporter) -> None:
        """'500' in the error string returns Server Error."""
        suggestion = reporter._get_suggestion("500 Internal Server Error")
        assert suggestion is not None
        assert suggestion["title"] == "Server Error"

    def test_matches_valid_slug(self, reporter: DetailedErrorReporter) -> None:
        """'valid_slug' in error matches the Invalid Slug Format pattern."""
        suggestion = reporter._get_suggestion("valid_slug constraint violated")
        assert suggestion is not None
        assert suggestion["title"] == "Invalid Slug Format"


# ---------------------------------------------------------------------------
# add_known_issue
# ---------------------------------------------------------------------------


class TestAddKnownIssue:
    """Tests for ``add_known_issue()`` — dynamically extending the known-issues
    registry."""

    def test_new_pattern_is_matched(self, reporter: DetailedErrorReporter) -> None:
        """A newly added pattern can be matched immediately."""
        reporter.add_known_issue(
            pattern="my_custom_error",
            title="Custom Error",
            description="A custom error for testing",
            fix="Do something else",
        )
        suggestion = reporter._get_suggestion("my_custom_error occurred")
        assert suggestion is not None
        assert suggestion["title"] == "Custom Error"

    def test_new_pattern_with_doc_link(self, reporter: DetailedErrorReporter) -> None:
        """A newly added pattern with a doc link preserves the link."""
        reporter.add_known_issue(
            pattern="custom_with_doc",
            title="Doc Error",
            description="Has docs",
            fix="Read the docs",
            doc_link="https://example.com/docs",
        )
        suggestion = reporter._get_suggestion("custom_with_doc happened")
        assert suggestion is not None
        assert suggestion["doc_link"] == "https://example.com/docs"

    def test_latest_add_wins_for_same_pattern(self, reporter: DetailedErrorReporter) -> None:
        """Adding the same pattern twice overwrites the earlier entry."""
        reporter.add_known_issue(
            pattern="dup_pattern",
            title="Original",
            description="Original description",
            fix="Original fix",
        )
        reporter.add_known_issue(
            pattern="dup_pattern",
            title="Override",
            description="Override description",
            fix="Override fix",
        )
        suggestion = reporter._get_suggestion("dup_pattern")
        assert suggestion is not None
        assert suggestion["title"] == "Override"


# ---------------------------------------------------------------------------
# Constructor defaults
# ---------------------------------------------------------------------------


class TestConstructor:
    """Tests for DetailedErrorReporter construction defaults."""

    def test_default_uses_rich_when_available(self) -> None:
        """By default use_rich is True and verbose is True."""
        rep = DetailedErrorReporter()
        assert rep.verbose is True
        # use_rich will be True if Rich is installed in the test env,
        # False otherwise — we just verify the attribute exists.
        assert hasattr(rep, "use_rich")

    def test_verbose_false_disables_locals(self) -> None:
        """With verbose=False, local variable display is skipped."""
        rep = DetailedErrorReporter(verbose=False, use_rich=False)
        assert rep.verbose is False
