import csv
import os
import time
import redis
from dotenv import load_dotenv

load_dotenv()

GRAPH = "benchmark"
BATCH_SIZE = 100

NODES_FILE = "data/benchmark/nodes_enriched.csv"
EDGES_FILE = "data/benchmark/edges.csv"


def get_client():
    return redis.Redis(
        host=os.environ["FALKORDB_HOST"],
        port=int(os.environ["FALKORDB_PORT"]),
        username=os.environ.get("FALKORDB_USERNAME"),
        password=os.environ["FALKORDB_PASSWORD"],
        decode_responses=True,
        ssl=True,
        socket_connect_timeout=15,
        socket_timeout=60,
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
    except Exception as e:
        print(f"Clear warning: {e}", flush=True)

    print("Graph cleared.", flush=True)


def create_indexes(client):
    print("Creating indexes...", flush=True)

    indexes = [
        "CREATE INDEX FOR (n:Person) ON (n.id)",
        "CREATE INDEX FOR (n:Person) ON (n.age)",
        "CREATE INDEX FOR (n:Person) ON (n.benchmark_group)",
    ]

    for statement in indexes:
        try:
            query(client, statement)
        except Exception as e:
            if "already exists" not in str(e).lower():
                print(f"Index warning: {e}", flush=True)

    print("Indexes ready.", flush=True)


def load_nodes(client):
    print()
    print("Loading nodes...", flush=True)

    total = 0
    start = time.perf_counter()
    batch = []

    with open(NODES_FILE, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            batch.append(row)

            if len(batch) >= BATCH_SIZE:
                insert_node_batch(client, batch)
                total += len(batch)
                batch = []

                if total % 1000 == 0:
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
        f"Nodes loaded: {total:,} | "
        f"time: {elapsed:.2f}s | "
        f"throughput: {total / elapsed:,.2f}/sec",
        flush=True,
    )


def insert_node_batch(client, rows):
    values = []

    for row in rows:
        group = row["benchmark_group"].replace("\\", "\\\\").replace('"', '\\"')

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

    with open(EDGES_FILE, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            batch.append(row)

            if len(batch) >= BATCH_SIZE:
                insert_edge_batch(client, batch)
                total += len(batch)
                batch = []

                if total % 1000 == 0:
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
        f"Relationships loaded: {total:,} | "
        f"time: {elapsed:.2f}s | "
        f"throughput: {total / elapsed:,.2f}/sec",
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
    print("FalkorDB dataset loading completed successfully.", flush=True)


if __name__ == "__main__":
    main()