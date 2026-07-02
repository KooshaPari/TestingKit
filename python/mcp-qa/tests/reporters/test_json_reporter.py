"""Tests for JSONReporter — summary calculation and metadata sanitization.

Tests the pure-function internals of JSONReporter without touching
the filesystem (except one test that exercises the full ``report()``
pipeline with a temporary file).
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from mcp_qa.reporters.json_reporter import JSONReporter


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_result(
    *,
    success: bool = True,
    skipped: bool = False,
    cached: bool = False,
    duration_ms: float = 100.0,
) -> dict:
    return {
        "test_name": "dummy",
        "tool_name": "dummy_tool",
        "success": success,
        "skipped": skipped,
        "cached": cached,
        "duration_ms": duration_ms,
    }


# ---------------------------------------------------------------------------
# _calculate_summary  (pure function)
# ---------------------------------------------------------------------------


def test_summary_empty_results() -> None:
    """Empty result list produces a zeroed summary."""
    reporter = JSONReporter("/tmp/never_written.json")
    summary = reporter._calculate_summary([])
    assert summary["total"] == 0
    assert summary["passed"] == 0
    assert summary["failed"] == 0
    assert summary["skipped"] == 0
    assert summary["pass_rate"] == 0.0
    assert summary["avg_duration_ms"] == 0.0
    assert summary["total_duration_ms"] == 0.0


def test_summary_all_passed() -> None:
    """All-pass results yield 100 % pass rate."""
    reporter = JSONReporter("/tmp/never_written.json")
    results = [_make_result(success=True) for _ in range(5)]
    summary = reporter._calculate_summary(results)
    assert summary["total"] == 5
    assert summary["passed"] == 5
    assert summary["failed"] == 0
    assert summary["pass_rate"] == 100.0


def test_summary_mixed_results() -> None:
    """Mixed pass/fail/skipped results produce correct counts."""
    reporter = JSONReporter("/tmp/never_written.json")
    results = [
        _make_result(success=True, duration_ms=50.0),
        _make_result(success=False, duration_ms=30.0),
        _make_result(skipped=True),
        _make_result(success=True, duration_ms=20.0),
    ]
    summary = reporter._calculate_summary(results)
    assert summary["total"] == 4
    assert summary["passed"] == 2
    assert summary["failed"] == 1
    assert summary["skipped"] == 1
    # pass_rate = 2 / (4-1) = 66.666...
    assert summary["pass_rate"] == pytest.approx(66.6667, rel=1e-3)
    # total_duration skips skipped results: 50 + 30 + 20 = 100
    assert summary["total_duration_ms"] == 100.0
    # avg_duration = 100 / 3 = 33.333...
    assert summary["avg_duration_ms"] == pytest.approx(33.3333, rel=1e-3)


def test_summary_with_cached_results() -> None:
    """Cached results are counted separately and not subtracted from pass rate."""
    reporter = JSONReporter("/tmp/never_written.json")
    results = [
        _make_result(success=True, cached=True, duration_ms=5.0),
        _make_result(success=True, duration_ms=50.0),
    ]
    summary = reporter._calculate_summary(results)
    assert summary["cached"] == 1
    assert summary["passed"] == 2  # cached + normal pass = 2 passed
    assert summary["total"] == 2
    assert summary["pass_rate"] == 100.0


def test_summary_all_skipped_does_not_divide_by_zero() -> None:
    """When every result is skipped, pass_rate is 0 (no division by zero)."""
    reporter = JSONReporter("/tmp/never_written.json")
    results = [_make_result(skipped=True) for _ in range(3)]
    summary = reporter._calculate_summary(results)
    assert summary["total"] == 3
    assert summary["skipped"] == 3
    assert summary["passed"] == 0
    assert summary["pass_rate"] == 0.0
    assert summary["avg_duration_ms"] == 0.0


# ---------------------------------------------------------------------------
# _sanitize_metadata  (pure function)
# ---------------------------------------------------------------------------


def test_sanitize_metadata_removes_callables() -> None:
    """Callable values are stripped from metadata."""
    reporter = JSONReporter("/tmp/never_written.json")

    def unused() -> str:
        return "nope"

    meta = {"endpoint": "http://localhost", "callback": unused, "port": 8080}
    sanitized = reporter._sanitize_metadata(meta)
    assert sanitized == {"endpoint": "http://localhost", "port": 8080}


def test_sanitize_metadata_falls_back_to_str() -> None:
    """Non-serializable values are converted to strings."""
    reporter = JSONReporter("/tmp/never_written.json")

    class Unserializable:
        pass

    meta = {"good": "hello", "bad": Unserializable()}
    sanitized = reporter._sanitize_metadata(meta)
    assert sanitized["good"] == "hello"
    assert isinstance(sanitized["bad"], str)


def test_sanitize_metadata_passthrough_clean() -> None:
    """Clean metadata passes through unchanged."""
    reporter = JSONReporter("/tmp/never_written.json")
    meta = {"endpoint": "http://localhost", "auth_status": "authenticated", "count": 42}
    assert reporter._sanitize_metadata(meta) == meta


# ---------------------------------------------------------------------------
# report()  integration  (temp file)
# ---------------------------------------------------------------------------


def test_report_writes_valid_json() -> None:
    """report() writes a valid JSON file with expected top-level keys."""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        path = Path(f.name)

    try:
        reporter = JSONReporter(str(path))
        results = [
            _make_result(success=True, duration_ms=10.0),
            _make_result(success=False, duration_ms=20.0),
        ]
        metadata = {"endpoint": "http://localhost", "auth_status": "authenticated"}
        reporter.report(results, metadata)

        assert path.exists()
        raw = path.read_text()
        data = json.loads(raw)
        assert "generated_at" in data
        assert "metadata" in data
        assert "summary" in data
        assert "results" in data
        assert data["metadata"]["endpoint"] == "http://localhost"
        assert data["summary"]["total"] == 2
        assert data["summary"]["passed"] == 1
        assert data["summary"]["failed"] == 1
    finally:
        path.unlink(missing_ok=True)
