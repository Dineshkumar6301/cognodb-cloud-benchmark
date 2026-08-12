import time

from benchmark.metrics import run_workload


counter = 0


def fake_query():
    global counter

    counter += 1

    time.sleep(0.001)


result = run_workload(
    fake_query,
    warmup_iterations=5,
    measured_iterations=100,
)


print("Benchmark metrics test")
print("----------------------")

print("Count:", result["count"])
print("Successful:", result["successful_iterations"])
print("Failed:", result["failed_iterations"])
print("Error rate:", result["error_rate"])

print("Min ms:", round(result["min_ms"], 3))
print("Mean ms:", round(result["mean_ms"], 3))
print("P50 ms:", round(result["p50_ms"], 3))
print("P95 ms:", round(result["p95_ms"], 3))
print("Max ms:", round(result["max_ms"], 3))

print()
print("Fake query executions:", counter)