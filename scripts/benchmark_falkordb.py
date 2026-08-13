import json
import os
import random
import statistics
import time
from pathlib import Path

import redis
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_FILE = PROJECT_ROOT / "results" / "raw" / "falkordb_read_benchmark.json"
GRAPH_NAME = "benchmark"
ITERATIONS = 100
WARMUP = 20
RANDOM_SEED = 42
START_NODES = [70705, 8140, 1702, 22815, 19942]


def get_client():
    return redis.Redis(
        host=os.environ["FALKORDB_HOST"],
        port=int(os.environ["FALKORDB_PORT"]),
        username=os.environ.get("FALKORDB_USERNAME"),
        password=os.environ["FALKORDB_PASSWORD"],
        decode_responses=True,
        ssl=False,
        socket_connect_timeout=30,
        socket_timeout=120,
    )


def query(client, cypher):
    return client.execute_command(
        "GRAPH.QUERY", GRAPH_NAME, cypher, "--compact"
    )


def benchmark(client, name, make_query, nodes):
    print(f"\nBenchmarking: {name}")
    print("-" * 40)

    for node_id in nodes[:WARMUP]:
        query(client, make_query(node_id))

    latencies = []
    failures = 0

    for i in range(ITERATIONS):
        node_id = nodes[i % len(nodes)]
        start = time.perf_counter()
        try:
            query(client, make_query(node_id))
            latencies.append((time.perf_counter() - start) * 1000)
        except Exception:
            failures += 1

    latencies.sort()
    successful = len(latencies)

    def percentile(p):
        if not latencies:
            return None
        index = (len(latencies) - 1) * p
        lower = int(index)
        upper = min(lower + 1, len(latencies) - 1)
        weight = index - lower
        return latencies[lower] * (1 - weight) + latencies[upper] * weight

    result = {
        "iterations": ITERATIONS,
        "warmup_iterations": WARMUP,
        "successful": successful,
        "failed": failures,
        "error_rate": failures / ITERATIONS,
        "min_ms": min(latencies) if latencies else None,
        "mean_ms": statistics.mean(latencies) if latencies else None,
        "p50_ms": percentile(0.50),
        "p95_ms": percentile(0.95),
        "max_ms": max(latencies) if latencies else None,
    }

    print(f"P50: {result['p50_ms']:.3f} ms")
    print(f"P95: {result['p95_ms']:.3f} ms")
    print(f"Mean: {result['mean_ms']:.3f} ms")
    print(f"Successful: {successful}")
    print(f"Failed: {failures}")
    return result


def main():
    print("FalkorDB Read Benchmark")
    print("=======================")

    client = get_client()
    client.ping()

    random.seed(RANDOM_SEED)
    nodes = START_NODES * 20
    random.shuffle(nodes)

    workloads = {
        "point_lookup": lambda n: f"MATCH (x:Person {{id: {n}}}) RETURN x",
        "indexed_lookup": lambda n: "MATCH (x:Person {age: 21}) RETURN count(x)",
        "1_hop": lambda n: (
            f"MATCH (x:Person {{id: {n}}})-[:TRUSTS]->(y) RETURN count(y)"
        ),
        "2_hop": lambda n: (
            f"MATCH (x:Person {{id: {n}}})-[:TRUSTS*2]->(y) RETURN count(y)"
        ),
        "3_hop": lambda n: (
            f"MATCH (x:Person {{id: {n}}})-[:TRUSTS*3]->(y) RETURN count(y)"
        ),
        "aggregation": lambda n: (
            "MATCH (x:Person) RETURN x.benchmark_group, count(x)"
        ),
    }

    results = {}
    display_names = {
        "point_lookup": "Point lookup",
        "indexed_lookup": "Indexed lookup",
        "1_hop": "1-hop traversal",
        "2_hop": "2-hop traversal",
        "3_hop": "3-hop traversal",
        "aggregation": "Aggregation",
    }

    for key, workload in workloads.items():
        results[key] = benchmark(
            client, display_names[key], workload, nodes
        )

    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "database": "FalkorDB",
        "graph": GRAPH_NAME,
        "iterations": ITERATIONS,
        "warmup_iterations": WARMUP,
        "random_seed": RANDOM_SEED,
        "results": results,
    }

    RESULTS_FILE.write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )

    print(f"\nResults saved to: {RESULTS_FILE}")
    print("\nFalkorDB read benchmark completed.")


if __name__ == "__main__":
    main()
