import json
from pathlib import Path

from benchmark.dataset import (
    validate_dataset,
    choose_start_nodes,
)

from benchmark.metrics import run_workload

from platforms.neo4j.workloads import (
    Neo4jWorkloads,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RESULTS_DIR = PROJECT_ROOT / "results" / "raw"

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


def benchmark_single_workload(name, operation):

    print()
    print(f"Benchmarking: {name}")
    print("-" * 40)

    result = run_workload(
        operation,
        warmup_iterations=20,
        measured_iterations=100,
    )

    print(
        f"P50: {result['p50_ms']:.3f} ms"
    )

    print(
        f"P95: {result['p95_ms']:.3f} ms"
    )

    print(
        f"Mean: {result['mean_ms']:.3f} ms"
    )

    print(
        f"Successful: "
        f"{result['successful_iterations']}"
    )

    print(
        f"Failed: "
        f"{result['failed_iterations']}"
    )

    return result


def main():

    dataset = validate_dataset()

    start_nodes = choose_start_nodes(
        dataset["node_ids"],
        count=100,
    )

    db = Neo4jWorkloads()

    try:

        print("Neo4j Read Benchmark")
        print("====================")

        print(
            f"Start nodes: {len(start_nodes)}"
        )

        results = {}

        # Point lookup

        index = 0

        def point_lookup():

            nonlocal index

            node_id = start_nodes[
                index % len(start_nodes)
            ]

            index += 1

            return db.point_lookup(node_id)

        results["point_lookup"] = (
            benchmark_single_workload(
                "Point lookup",
                point_lookup,
            )
        )

        # Indexed lookup

        results["indexed_lookup"] = (
            benchmark_single_workload(
                "Indexed lookup",
                lambda: db.indexed_lookup(25),
            )
        )

        # 1-hop

        index = 0

        def one_hop():

            nonlocal index

            node_id = start_nodes[
                index % len(start_nodes)
            ]

            index += 1

            return db.one_hop(node_id)

        results["one_hop"] = (
            benchmark_single_workload(
                "1-hop traversal",
                one_hop,
            )
        )

        # 2-hop

        index = 0

        def two_hop():

            nonlocal index

            node_id = start_nodes[
                index % len(start_nodes)
            ]

            index += 1

            return db.two_hop(node_id)

        results["two_hop"] = (
            benchmark_single_workload(
                "2-hop traversal",
                two_hop,
            )
        )

        # 3-hop

        index = 0

        def three_hop():

            nonlocal index

            node_id = start_nodes[
                index % len(start_nodes)
            ]

            index += 1

            return db.three_hop(node_id)

        results["three_hop"] = (
            benchmark_single_workload(
                "3-hop traversal",
                three_hop,
            )
        )

        # Aggregation

        results["aggregation"] = (
            benchmark_single_workload(
                "Aggregation",
                db.aggregation,
            )
        )

        output_file = (
            RESULTS_DIR
            / "neo4j_read_benchmark.json"
        )

        with output_file.open(
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
            f"Results saved to: {output_file}"
        )

        print()
        print(
            "Neo4j read benchmark completed."
        )

    finally:

        db.close()


if __name__ == "__main__":
    main()