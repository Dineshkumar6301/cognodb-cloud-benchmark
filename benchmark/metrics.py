import statistics
import time
from typing import Callable, Any


def percentile(values, percentile):
    """
    Calculate a percentile using linear interpolation.
    """
    if not values:
        raise ValueError("Cannot calculate percentile of empty data.")

    sorted_values = sorted(values)

    if len(sorted_values) == 1:
        return sorted_values[0]

    position = (len(sorted_values) - 1) * (percentile / 100)

    lower = int(position)
    upper = min(lower + 1, len(sorted_values) - 1)

    fraction = position - lower

    return (
        sorted_values[lower]
        + (sorted_values[upper] - sorted_values[lower]) * fraction
    )


def summarize_latencies(latencies):
    """
    Return standard latency statistics in milliseconds.
    """

    if not latencies:
        return {
            "count": 0,
            "min_ms": 0.0,
            "mean_ms": 0.0,
            "p50_ms": 0.0,
            "p95_ms": 0.0,
            "max_ms": 0.0,
        }

    latencies_ms = [
        value * 1000
        for value in latencies
    ]

    return {
        "count": len(latencies_ms),
        "min_ms": min(latencies_ms),
        "mean_ms": statistics.mean(latencies_ms),
        "p50_ms": percentile(latencies_ms, 50),
        "p95_ms": percentile(latencies_ms, 95),
        "max_ms": max(latencies_ms),
    }


def run_workload(
    operation: Callable[[], Any],
    warmup_iterations: int = 20,
    measured_iterations: int = 100,
):
    """
    Execute a workload with warm-up iterations followed
    by measured iterations.

    Returns latency statistics and error information.
    """

    # Warm-up
    for _ in range(warmup_iterations):
        try:
            operation()
        except Exception:
            # Warm-up failures do not contribute to measured results.
            pass

    latencies = []
    errors = []

    # Measured runs
    for iteration in range(measured_iterations):

        start = time.perf_counter()

        try:
            operation()

            elapsed = time.perf_counter() - start
            latencies.append(elapsed)

        except Exception as exc:

            elapsed = time.perf_counter() - start

            errors.append({
                "iteration": iteration + 1,
                "error": str(exc),
                "latency_ms": elapsed * 1000,
            })

    summary = summarize_latencies(latencies)

    summary["successful_iterations"] = len(latencies)
    summary["failed_iterations"] = len(errors)
    summary["error_rate"] = (
        len(errors) / measured_iterations
        if measured_iterations
        else 0
    )

    summary["errors"] = errors

    return summary