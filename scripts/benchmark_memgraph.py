import json
import os
import statistics
import time
from pathlib import Path

from dotenv import load_dotenv
from gqlalchemy import Memgraph


load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RESULTS_DIR = PROJECT_ROOT / "results" / "raw"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

RESULT_FILE = (
    RESULTS_DIR / "memgraph_read_benchmark.json"
)

WARMUP_ITERATIONS = 20
MEASURED_ITERATIONS = 100

START_NODES = [
    70705,
    8140,
    1702,
    22815,
    19942,
    18003,
    10453,
    7433,
    55866,
    6238,
]


def connect():

    return Memgraph(
        host=os.environ["MEMGRAPH_HOST"],
        port=int(os.environ["MEMGRAPH_PORT"]),
        username=os.environ["MEMGRAPH_USERNAME"],
        password=os.environ["MEMGRAPH_PASSWORD"],
        encrypted=True,
    )


def point_lookup(db, node_id):

    query = """
    MATCH (p:Person {id: $id})
    RETURN p.id AS id
    """

    list(
        db.execute_and_fetch(
            query,
            {"id": node_id},
        )
    )


def indexed_lookup(db):

    query = """
    MATCH (p:Person)
    WHERE p.age = $age
    RETURN count(p) AS count
    """

    list(
        db.execute_and_fetch(
            query,
            {"age": 25},
        )
    )


def one_hop(db, node_id):

    query = """
    MATCH (p:Person {id: $id})
          -[:TRUSTS]->
          (friend)
    RETURN count(friend) AS count
    """

    list(
        db.execute_and_fetch(
            query,
            {"id": node_id},
        )
    )


def two_hop(db, node_id):

    query = """
    MATCH (p:Person {id: $id})
          -[:TRUSTS*2]->
          (friend)
    RETURN count(friend) AS count
    """

    list(
        db.execute_and_fetch(
            query,
            {"id": node_id},
        )
    )


def three_hop(db, node_id):

    query = """
    MATCH (p:Person {id: $id})
          -[:TRUSTS*3]->
          (friend)
    RETURN count(friend) AS count
    """

    list(
        db.execute_and_fetch(
            query,
            {"id": node_id},
        )
    )


def aggregation(db):

    query = """
    MATCH (p:Person)
    RETURN p.age AS age,
           count(p) AS count
    ORDER BY age
    """

    list(db.execute_and_fetch(query))


WORKLOADS = {
    "Point lookup": point_lookup,
    "Indexed lookup": indexed_lookup,
    "1-hop traversal": one_hop,
    "2-hop traversal": two_hop,
    "3-hop traversal": three_hop,
    "Aggregation": aggregation,
}


def run_workload(db, name, function):

    print()
    print(f"Benchmarking: {name}")
    print("-" * 40)

    # Warm-up
    for i in range(WARMUP_ITERATIONS):

        node_id = START_NODES[
            i % len(START_NODES)
        ]

        if name == "Point lookup":
            function(db, node_id)

        elif name == "Indexed lookup":
            function(db)

        elif name == "Aggregation":
            function(db)

        else:
            function(db, node_id)

    latencies = []
    failures = 0

    for i in range(MEASURED_ITERATIONS):

        node_id = START_NODES[
            i % len(START_NODES)
        ]

        try:

            start = time.perf_counter()

            if name == "Point lookup":
                function(db, node_id)

            elif name == "Indexed lookup":
                function(db)

            elif name == "Aggregation":
                function(db)

            else:
                function(db, node_id)

            elapsed_ms = (
                time.perf_counter() - start
            ) * 1000

            latencies.append(elapsed_ms)

        except Exception as exc:

            failures += 1

            print(
                f"Iteration {i + 1} failed: {exc}"
            )

    latencies.sort()

    successful = len(latencies)

    if successful:

        p50 = statistics.median(latencies)

        p95_index = max(
            0,
            int(0.95 * successful) - 1,
        )

        p95 = latencies[p95_index]

        mean = statistics.mean(latencies)

        minimum = min(latencies)

        maximum = max(latencies)

    else:

        p50 = None
        p95 = None
        mean = None
        minimum = None
        maximum = None

    print(f"P50: {p50:.3f} ms")
    print(f"P95: {p95:.3f} ms")
    print(f"Mean: {mean:.3f} ms")
    print(f"Successful: {successful}")
    print(f"Failed: {failures}")

    return {
        "iterations": MEASURED_ITERATIONS,
        "warmup_iterations": WARMUP_ITERATIONS,
        "successful": successful,
        "failed": failures,
        "p50_ms": p50,
        "p95_ms": p95,
        "mean_ms": mean,
        "min_ms": minimum,
        "max_ms": maximum,
        "latencies_ms": latencies,
    }


def main():

    print("Memgraph Read Benchmark")
    print("=======================")
    print(
        f"Start nodes: {len(START_NODES)}"
    )

    db = connect()

    results = {
        "database": "memgraph",
        "warmup_iterations": WARMUP_ITERATIONS,
        "measured_iterations": MEASURED_ITERATIONS,
        "start_nodes": START_NODES,
        "workloads": {},
    }

    try:

        for name, function in WORKLOADS.items():

            results["workloads"][name] = (
                run_workload(
                    db,
                    name,
                    function,
                )
            )

    finally:

        pass

    with RESULT_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            results,
            file,
            indent=2,
        )

    print()
    print(
        f"Results saved to: {RESULT_FILE}"
    )

    print()
    print(
        "Memgraph read benchmark completed."
    )


if __name__ == "__main__":
    main()