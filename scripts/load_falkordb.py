import csv
import os
import time

import redis
from dotenv import load_dotenv

load_dotenv()

GRAPH = "benchmark"

NODES_FILE = "data/benchmark/nodes_enriched.csv"
EDGES_FILE = "data/benchmark/edges.csv"

# Large batches = far fewer network round trips
NODE_BATCH_SIZE = 2000
EDGE_BATCH_SIZE = 2000


def get_client():
    return redis.Redis(
        host=os.environ["FALKORDB_HOST"],
        port=int(os.environ["FALKORDB_PORT"]),
        username=os.environ.get("FALKORDB_USERNAME"),
        password=os.environ["FALKORDB_PASSWORD"],
        decode_responses=True,
        ssl=True,
        socket_connect_timeout=15,
        socket_timeout=120,
    )


def query(client, cypher):
    return client.execute_command(
        "GRAPH.QUERY",
        GRAPH,
        cypher,
        "--compact",
    )


def clear_graph(client):
    print("Clearing existing graph...", flush=True)

    try:
        query(client, "MATCH (n) DETACH DELETE n")
    except Exception as exc:
        print(f"Clear warning: {exc}", flush=True)

    print("Graph cleared.", flush=True)


def create_indexes(client):
    print("Creating indexes...", flush=True)

    statements = [
        "CREATE INDEX FOR (n:Person) ON (n.id)",
        "CREATE INDEX FOR (n:Person) ON (n.age)",
        "CREATE INDEX FOR (n:Person) ON (n.benchmark_group)",
    ]

    for statement in statements:
        try:
            query(client, statement)
        except Exception as exc:
            if "already exists" not in str(exc).lower():
                print(f"Index warning: {exc}", flush=True)

    print("Indexes ready.", flush=True)


def escape_string(value):
    return (
        str(value)
        .replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\r", "\\r")
        .replace("\n", "\\n")
    )


def load_nodes(client):
    print()
    print("Loading nodes...", flush=True)

    total = 0
    start = time.perf_counter()
    batch = []

    with open(
        NODES_FILE,
        "r",
        encoding="utf-8",
        newline="",
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            batch.append(row)

            if len(batch) >= NODE_BATCH_SIZE:
                insert_node_batch(client, batch)

                total += len(batch)
                batch.clear()

                elapsed = time.perf_counter() - start
                rate = total / elapsed if elapsed else 0

                print(
                    f"Nodes: {total:,}/43,824 "
                    f"({rate:,.0f}/sec)",
                    flush=True,
                )

        if batch:
            insert_node_batch(client, batch)
            total += len(batch)

    elapsed = time.perf_counter() - start

    print(
        f"Nodes loaded: {total:,}",
        flush=True,
    )
    print(
        f"Node load time: {elapsed:.2f}s",
        flush=True,
    )
    print(
        f"Node throughput: "
        f"{total / elapsed:,.2f} nodes/sec",
        flush=True,
    )


def insert_node_batch(client, rows):
    values = []

    for row in rows:
        group = escape_string(row["benchmark_group"])

        values.append(
            "{"
            f"id:{int(row['id'])},"
            f"age:{int(row['age'])},"
            f'benchmark_group:"{group}"'
            "}"
        )

    cypher = (
        "UNWIND ["
        + ",".join(values)
        + "] AS row "
        "CREATE (:Person {"
        "id:row.id,"
        "age:row.age,"
        "benchmark_group:row.benchmark_group"
        "})"
    )

    query(client, cypher)


def load_edges(client):
    print()
    print("Loading relationships...", flush=True)

    total = 0
    start = time.perf_counter()
    batch = []

    with open(
        EDGES_FILE,
        "r",
        encoding="utf-8",
        newline="",
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            batch.append(row)

            if len(batch) >= EDGE_BATCH_SIZE:
                insert_edge_batch(client, batch)

                total += len(batch)
                batch.clear()

                elapsed = time.perf_counter() - start
                rate = total / elapsed if elapsed else 0

                print(
                    f"Relationships: {total:,}/150,000 "
                    f"({rate:,.0f}/sec)",
                    flush=True,
                )

        if batch:
            insert_edge_batch(client, batch)
            total += len(batch)

    elapsed = time.perf_counter() - start

    print(
        f"Relationships loaded: {total:,}",
        flush=True,
    )
    print(
        f"Relationship load time: "
        f"{elapsed:.2f}s",
        flush=True,
    )
    print(
        f"Relationship throughput: "
        f"{total / elapsed:,.2f} relationships/sec",
        flush=True,
    )


def insert_edge_batch(client, rows):
    values = []

    for row in rows:
        values.append(
            "{"
            f"source_id:{int(row['source_id'])},"
            f"target_id:{int(row['target_id'])}"
            "}"
        )

    cypher = (
        "UNWIND ["
        + ",".join(values)
        + "] AS row "
        "MATCH (source:Person {id:row.source_id}) "
        "MATCH (target:Person {id:row.target_id}) "
        "CREATE (source)-[:TRUSTS]->(target)"
    )

    query(client, cypher)


def main():
    print("FalkorDB FAST benchmark dataset loader")
    print("=======================================")

    client = get_client()

    print("Testing connection...", flush=True)
    client.ping()
    print("Connection: OK", flush=True)

    clear_graph(client)
    create_indexes(client)

    load_nodes(client)
    load_edges(client)

    print()
    print(
        "FalkorDB dataset loading completed successfully.",
        flush=True,
    )


if __name__ == "__main__":
    main()