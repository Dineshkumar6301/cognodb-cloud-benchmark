from pathlib import Path
import csv


INPUT_FILE = Path("data/benchmark/nodes.csv")
OUTPUT_FILE = Path("data/benchmark/nodes_enriched.csv")


def calculate_age(node_id: int) -> int:
    """
    Deterministically generate an age between 18 and 70.
    The same node ID always gets the same age.
    """
    return 18 + (node_id % 53)


def calculate_group(node_id: int) -> str:
    """
    Deterministically assign every node to one of four groups.
    """
    groups = ["A", "B", "C", "D"]
    return groups[node_id % len(groups)]


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_FILE}"
        )

    count = 0

    with INPUT_FILE.open(
        "r",
        newline="",
        encoding="utf-8"
    ) as source:

        reader = csv.DictReader(source)

        with OUTPUT_FILE.open(
            "w",
            newline="",
            encoding="utf-8"
        ) as destination:

            writer = csv.writer(destination)

            writer.writerow(
                [
                    "id",
                    "age",
                    "benchmark_group"
                ]
            )

            for row in reader:

                node_id = int(row["id"])

                age = calculate_age(node_id)

                group = calculate_group(node_id)

                writer.writerow(
                    [
                        node_id,
                        age,
                        group
                    ]
                )

                count += 1

    print("Enriched benchmark node dataset created.")
    print(f"Nodes: {count:,}")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()