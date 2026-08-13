import csv
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from gqlalchemy import Memgraph


load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]

NODES_FILE = (
    PROJECT_ROOT
    / "data"
    / "benchmark"
    / "nodes_enriched.csv"
)

EDGES_FILE = (
    PROJECT_ROOT
    / "data"
    / "benchmark"
    / "edges.csv"
)


BATCH_SIZE = 1000


def get_memgraph():

    return Memgraph(
        host=os.environ["MEMGRAPH_HOST"],
        port=int(os.environ["MEMGRAPH_PORT"]),
        username=os.environ["MEMGRAPH_USERNAME"],
        password=os.environ["MEMGRAPH_PASSWORD"],
        encrypted=True,
    )


def clear_graph(db):

    print("Clearing existing graph...")

    db.execute(
        "MATCH (n) DETACH DELETE n"
    )

    print("Existing graph cleared.")


def create_indexes(db):

    print()
    print("Creating indexes...")

    statements = [
        """
        CREATE INDEX ON :Person(id)
        """,
        """
        CREATE INDEX ON :Person(age)
        """,
        """
        CREATE INDEX ON :Person(benchmark_group)
        """,
    ]

    for statement in statements:

        try:
            db.execute(statement)
        except Exception as exc:

            message = str(exc).lower()

            if "already exists" not in message:
                raise

    print("Indexes created.")


def load_nodes(db):

    print()
    print("Loading nodes...")

    query = """
    UNWIND $rows AS row
    CREATE (:Person {
        id: toInteger(row.id),
        age: toInteger(row.age),
        benchmark_group: row.benchmark_group
    })
    """

    rows = []

    total = 0
    start = time.perf_counter()

    with NODES_FILE.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            rows.append(row)

            if len(rows) >= BATCH_SIZE:

                db.execute(
                    query,
                    {"rows": rows},
                )

                total += len(rows)
                rows = []

    if rows:

        db.execute(
            query,
            {"rows": rows},
        )

        total += len(rows)

    elapsed = time.perf_counter() - start

    throughput = (
        total / elapsed
        if elapsed > 0
        else 0
    )

    print(
        f"Nodes loaded: {total:,}"
    )

    print(
        f"Node load time: {elapsed:.3f} seconds"
    )

    print(
        f"Node throughput: "
        f"{throughput:,.2f} nodes/sec"
    )


def load_relationships(db):

    print()
    print("Loading relationships...")

    query = """
    UNWIND $rows AS row

    MATCH (source:Person {
        id: toInteger(row.source_id)
    })

    MATCH (target:Person {
        id: toInteger(row.target_id)
    })

    CREATE (source)-[:TRUSTS]->(target)
    """

    rows = []

    total = 0
    start = time.perf_counter()

    with EDGES_FILE.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            rows.append(row)

            if len(rows) >= BATCH_SIZE:

                db.execute(
                    query,
                    {"rows": rows},
                )

                total += len(rows)
                rows = []

    if rows:

        db.execute(
            query,
            {"rows": rows},
        )

        total += len(rows)

    elapsed = time.perf_counter() - start

    throughput = (
        total / elapsed
        if elapsed > 0
        else 0
    )

    print(
        f"Relationships loaded: {total:,}"
    )

    print(
        f"Relationship load time: "
        f"{elapsed:.3f} seconds"
    )

    print(
        f"Relationship throughput: "
        f"{throughput:,.2f} relationships/sec"
    )


def main():

    print(
        "Memgraph benchmark dataset loader"
    )

    print(
        "=================================="
    )

    db = get_memgraph()

    clear_graph(db)

    create_indexes(db)

    load_nodes(db)

    load_relationships(db)

    print()
    print(
        "Memgraph dataset loading "
        "completed successfully."
    )


if __name__ == "__main__":
    main()
