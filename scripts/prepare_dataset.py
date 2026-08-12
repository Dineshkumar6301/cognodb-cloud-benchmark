from pathlib import Path
import gzip
import random
import csv

SOURCE = Path("data/source/soc-Epinions1.txt.gz")
OUTPUT_DIR = Path("data/benchmark")

EDGE_LIMIT = 150_000
RANDOM_SEED = 42


def read_edges():
    edges = []

    with gzip.open(SOURCE, "rt", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            parts = line.split()

            if len(parts) < 2:
                continue

            source = int(parts[0])
            target = int(parts[1])

            edges.append((source, target))

    return edges


def main():
    if not SOURCE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {SOURCE}"
        )

    print("Reading official SNAP soc-Epinions1 dataset...")

    edges = read_edges()

    print(f"Original relationships: {len(edges):,}")

    if len(edges) < EDGE_LIMIT:
        raise RuntimeError(
            f"Dataset contains fewer than {EDGE_LIMIT:,} relationships."
        )

    random.seed(RANDOM_SEED)

    sampled_edges = random.sample(
        edges,
        EDGE_LIMIT
    )

    nodes = sorted(
        set(source for source, _ in sampled_edges)
        |
        set(target for _, target in sampled_edges)
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    edges_file = OUTPUT_DIR / "edges.csv"
    nodes_file = OUTPUT_DIR / "nodes.csv"

    with edges_file.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow(
            ["source_id", "target_id"]
        )

        writer.writerows(
            sampled_edges
        )

    with nodes_file.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow(
            ["id"]
        )

        for node in nodes:
            writer.writerow(
                [node]
            )

    print()
    print("Benchmark dataset created.")
    print(f"Nodes: {len(nodes):,}")
    print(f"Relationships: {len(sampled_edges):,}")
    print(f"Random seed: {RANDOM_SEED}")
    print(f"Edges file: {edges_file}")
    print(f"Nodes file: {nodes_file}")


if __name__ == "__main__":
    main()