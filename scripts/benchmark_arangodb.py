import json
import os
import statistics
import time
from pathlib import Path

from arango import ArangoClient
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = PROJECT_ROOT / "results" / "raw"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

START_NODES = [70705, 8140, 1702, 22815, 19942] * 20


def get_db():
    client = ArangoClient(hosts=os.environ["ARANGODB_URL"])

    return client.db(
        "_system",
        username=os.environ["ARANGODB_USERNAME"],
        password=os.environ["ARANGODB_PASSWORD"],
    )


def run_query(db, query, bind_vars):
    return list(
        db.aql.execute(
            query,
            bind_vars=bind_vars,
        )
    )


def percentile(values, p):
    values = sorted(values)

    if not values:
        return 0

    index = (len(values) - 1) * p / 100
    lower = int(index)
    upper = min(lower + 1, len(values) - 1)

    if lower == upper:
        return values[lower]

    return values[lower] + (
        values[upper] - values[lower]
    ) * (index - lower)


def benchmark(db, name, query, bind_vars_factory):
    print()
    print(f"Benchmarking: {name}")
    print("-" * 40)

    timings = []
    successful = 0
    failed = 0

    for node_id in START_NODES:
        bind_vars = bind_vars_factory(node_id)

        start = time.perf_counter()

        try:
            run_query(db, query, bind_vars)
            elapsed = (time.perf_counter() - start) * 1000

            timings.append(elapsed)
            successful += 1

        except Exception as exc:
            failed += 1
            print(f"Query failed: {exc}")

    result = {
        "p50_ms": percentile(timings, 50),
        "p95_ms": percentile(timings, 95),
        "mean_ms": statistics.mean(timings) if timings else 0,
        "successful": successful,
        "failed": failed,
    }

    print(f"P50: {result['p50_ms']:.3f} ms")
    print(f"P95: {result['p95_ms']:.3f} ms")
    print(f"Mean: {result['mean_ms']:.3f} ms")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")

    return result


def main():
    print("ArangoDB Read Benchmark")
    print("=======================")
    print(f"Start nodes: {len(START_NODES)}")

    db = get_db()

    queries = {
        "Point lookup": (
            """
            FOR p IN persons
                FILTER p.id == @id
                RETURN p
            """,
            lambda node_id: {"id": node_id},
        ),

        "Indexed lookup": (
            """
            FOR p IN persons
                FILTER p.age == @age
                RETURN p
            """,
            lambda node_id: {"age": 21},
        ),

        "1-hop traversal": (
            """
            FOR v IN 1..1 OUTBOUND
                CONCAT("persons/", @id)
                trusts
                RETURN v
            """,
            lambda node_id: {"id": node_id},
        ),

        "2-hop traversal": (
            """
            FOR v IN 2..2 OUTBOUND
                CONCAT("persons/", @id)
                trusts
                RETURN v
            """,
            lambda node_id: {"id": node_id},
        ),

        "3-hop traversal": (
            """
            FOR v IN 3..3 OUTBOUND
                CONCAT("persons/", @id)
                trusts
                RETURN v
            """,
            lambda node_id: {"id": node_id},
        ),

        "Aggregation": (
            """
            FOR p IN persons
                COLLECT group = p.benchmark_group
                AGGREGATE count = COUNT()
                RETURN {
                    benchmark_group: group,
                    count: count
                }
            """,
            lambda node_id: {},
        ),
    }

    results = {}

    for name, (query, factory) in queries.items():
        results[name] = benchmark(
            db,
            name,
            query,
            factory,
        )

    output = {
        "database": "arangodb",
        "benchmark": "read",
        "start_nodes": len(START_NODES),
        "results": results,
    }

    output_file = (
        RESULTS_DIR
        / "arangodb_read_benchmark.json"
    )

    output_file.write_text(
        json.dumps(output, indent=2),
        encoding="utf-8",
    )

    print()
    print(f"Results saved to: {output_file}")
    print()
    print("ArangoDB read benchmark completed.")


if __name__ == "__main__":
    main()