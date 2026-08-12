from pathlib import Path
import csv
import random

from benchmark.config import (
    NODES_FILE,
    EDGES_FILE,
    RANDOM_SEED,
)


def load_node_ids():
    """
    Load all node IDs from the enriched node CSV.
    """

    node_ids = set()

    with Path(NODES_FILE).open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:

        reader = csv.DictReader(file)

        required_columns = {
            "id",
            "age",
            "benchmark_group",
        }

        if not required_columns.issubset(reader.fieldnames):
            raise ValueError(
                f"Missing node columns. "
                f"Expected {required_columns}, "
                f"found {reader.fieldnames}"
            )

        for row_number, row in enumerate(reader, start=2):

            try:
                node_id = int(row["id"])
                int(row["age"])
                row["benchmark_group"]

            except (TypeError, ValueError) as exc:
                raise ValueError(
                    f"Invalid node at CSV line {row_number}: {row}"
                ) from exc

            if node_id in node_ids:
                raise ValueError(
                    f"Duplicate node ID found: {node_id}"
                )

            node_ids.add(node_id)

    return node_ids


def load_edges(node_ids):
    """
    Load and validate all relationships.
    """

    edges = []

    with Path(EDGES_FILE).open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:

        reader = csv.DictReader(file)

        required_columns = {
            "source_id",
            "target_id",
        }

        if not required_columns.issubset(reader.fieldnames):
            raise ValueError(
                f"Missing edge columns. "
                f"Expected {required_columns}, "
                f"found {reader.fieldnames}"
            )

        for row_number, row in enumerate(reader, start=2):

            try:
                source_id = int(row["source_id"])
                target_id = int(row["target_id"])

            except (TypeError, ValueError) as exc:
                raise ValueError(
                    f"Invalid edge at CSV line {row_number}: {row}"
                ) from exc

            if source_id not in node_ids:
                raise ValueError(
                    f"Unknown source node {source_id} "
                    f"at line {row_number}"
                )

            if target_id not in node_ids:
                raise ValueError(
                    f"Unknown target node {target_id} "
                    f"at line {row_number}"
                )

            if source_id == target_id:
                raise ValueError(
                    f"Self-loop found at line {row_number}: "
                    f"{source_id} -> {target_id}"
                )

            edges.append(
                (source_id, target_id)
            )

    return edges


def choose_start_nodes(node_ids, count=100):
    """
    Select deterministic start nodes for read workloads.
    """

    if count > len(node_ids):
        raise ValueError(
            "Requested more start nodes than available nodes."
        )

    random_generator = random.Random(
        RANDOM_SEED
    )

    return random_generator.sample(
        sorted(node_ids),
        count,
    )


def validate_dataset():
    """
    Validate the complete benchmark dataset.
    """

    node_ids = load_node_ids()

    edges = load_edges(node_ids)

    return {
        "node_count": len(node_ids),
        "edge_count": len(edges),
        "node_ids": node_ids,
        "edges": edges,
    }