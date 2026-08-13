import csv
import os
import time
from pathlib import Path

from arango import ArangoClient
from dotenv import load_dotenv


load_dotenv()

ROOT = Path(__file__).resolve().parents[1]
NODES_FILE = ROOT / "data" / "benchmark" / "nodes_enriched.csv"
EDGES_FILE = ROOT / "data" / "benchmark" / "edges.csv"

GRAPH_NAME = "benchmark_graph"
VERTEX_COLLECTION = "persons"
EDGE_COLLECTION = "trusts"

BATCH_SIZE = 5000


def get_db():
    client = ArangoClient(hosts=os.environ["ARANGODB_URL"])
    return client.db(
        "_system",
        username=os.environ["ARANGODB_USERNAME"],
        password=os.environ["ARANGODB_PASSWORD"],
    )


def setup(db):
    print("Clearing existing benchmark data...")

    if db.has_graph(GRAPH_NAME):
        db.delete_graph(GRAPH_NAME, drop_collections=True)

    if db.has_collection(VERTEX_COLLECTION):
        db.delete_collection(VERTEX_COLLECTION)

    if db.has_collection(EDGE_COLLECTION):
        db.delete_collection(EDGE_COLLECTION)

    print("Creating collections...")

    db.create_collection(VERTEX_COLLECTION)
    db.create_collection(EDGE_COLLECTION, edge=True)

    graph = db.create_graph(GRAPH_NAME)

    graph.create_edge_definition(
        edge_collection=EDGE_COLLECTION,
        from_vertex_collections=[VERTEX_COLLECTION],
        to_vertex_collections=[VERTEX_COLLECTION],
    )

    persons = db.collection(VERTEX_COLLECTION)

    
    print("Collections, graph and indexes created.")

    return persons, db.collection(EDGE_COLLECTION)


def load_nodes(persons):
    print()
    print("Loading nodes...")

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
            rows.append(
                {
                    "_key": str(row["id"]),
                    "id": int(row["id"]),
                    "age": int(row["age"]),
                    "benchmark_group": row["benchmark_group"],
                }
            )

            if len(rows) >= BATCH_SIZE:
                persons.import_bulk(rows, on_duplicate="replace")
                total += len(rows)
                rows = []

    if rows:
        persons.import_bulk(rows, on_duplicate="replace")
        total += len(rows)

    elapsed = time.perf_counter() - start

    print(f"Nodes loaded: {total:,}")
    print(f"Node load time: {elapsed:.3f} seconds")
    print(
        f"Node throughput: "
        f"{total / elapsed:,.2f} nodes/sec"
    )


def load_edges(trusts):
    print()
    print("Loading relationships...")

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
            source = str(row["source_id"])
            target = str(row["target_id"])

            rows.append(
                {
                    "_from": f"{VERTEX_COLLECTION}/{source}",
                    "_to": f"{VERTEX_COLLECTION}/{target}",
                }
            )

            if len(rows) >= BATCH_SIZE:
                trusts.import_bulk(rows)
                total += len(rows)
                rows = []

    if rows:
        trusts.import_bulk(rows)
        total += len(rows)

    elapsed = time.perf_counter() - start

    print(f"Relationships loaded: {total:,}")
    print(
        f"Relationship load time: "
        f"{elapsed:.3f} seconds"
    )
    print(
        f"Relationship throughput: "
        f"{total / elapsed:,.2f} relationships/sec"
    )


def main():
    print("ArangoDB benchmark dataset loader")
    print("===================================")

    db = get_db()

    print("Connection: OK")

    persons, trusts = setup(db)

    load_nodes(persons)
    load_edges(trusts)

    print()
    print("ArangoDB dataset loading completed successfully.")


if __name__ == "__main__":
    main()