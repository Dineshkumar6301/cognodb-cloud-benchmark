from benchmark.dataset import (
    validate_dataset,
    choose_start_nodes,
)

from platforms.cognodb.workloads import (
    CognoDBWorkloads,
)


def main():

    dataset = validate_dataset()

    start_nodes = choose_start_nodes(
        dataset["node_ids"],
        count=5,
    )

    print("CognoDB workload test")
    print("=====================")

    print()
    print("Test start nodes:")
    print(start_nodes)

    db = CognoDBWorkloads()

    try:

        print()
        print("1. Point lookup")

        result = db.point_lookup(
            start_nodes[0]
        )

        print(
            result
        )

        print()
        print("2. Indexed lookup")

        result = db.indexed_lookup(
            25
        )

        print(
            result
        )

        print()
        print("3. One-hop traversal")

        result = db.one_hop(
            start_nodes[0]
        )

        print(
            result
        )

        print()
        print("4. Two-hop traversal")

        result = db.two_hop(
            start_nodes[0]
        )

        print(
            result
        )

        print()
        print("5. Three-hop traversal")

        result = db.three_hop(
            start_nodes[0]
        )

        print(
            result
        )

        print()
        print("6. Aggregation")

        result = db.aggregation()

        print(
            f"Aggregation groups: "
            f"{len(result)}"
        )

        print()
        print("All workload queries executed successfully.")

    finally:

        db.close()


if __name__ == "__main__":
    main()