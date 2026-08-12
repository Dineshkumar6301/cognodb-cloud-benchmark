from benchmark.dataset import (
    validate_dataset,
    choose_start_nodes,
)


def main():

    print("Benchmark dataset validation")
    print("============================")

    result = validate_dataset()

    node_count = result["node_count"]
    edge_count = result["edge_count"]
    node_ids = result["node_ids"]

    print()
    print("Dataset validation successful.")
    print()
    print(f"Nodes:         {node_count:,}")
    print(f"Relationships: {edge_count:,}")

    start_nodes = choose_start_nodes(
        node_ids,
        count=100,
    )

    print()
    print("Benchmark start-node sample:")
    print(f"Count: {len(start_nodes)}")
    print(f"First 10: {start_nodes[:10]}")

    print()
    print("All validation checks passed.")


if __name__ == "__main__":
    main()