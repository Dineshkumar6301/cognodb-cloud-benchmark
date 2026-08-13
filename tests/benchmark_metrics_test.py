from benchmark.metrics import run_workload


def test_run_workload_success():
    calls = 0

    def successful_query():
        nonlocal calls
        calls += 1

    result = run_workload(
        successful_query,
        warmup_iterations=2,
        measured_iterations=5,
    )

    assert calls == 7
    assert result["count"] == 5
    assert result["successful_iterations"] == 5
    assert result["failed_iterations"] == 0
    assert result["error_rate"] == 0


def test_run_workload_all_failures():
    calls = 0

    def failing_query():
        nonlocal calls
        calls += 1
        raise RuntimeError("test failure")

    result = run_workload(
        failing_query,
        warmup_iterations=0,
        measured_iterations=5,
    )

    assert calls == 5
    assert result["count"] == 0
    assert result["successful_iterations"] == 0
    assert result["failed_iterations"] == 5
    assert result["error_rate"] == 1.0
    assert len(result["errors"]) == 5