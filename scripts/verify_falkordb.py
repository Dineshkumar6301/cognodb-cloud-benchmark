import os
from pathlib import Path

import redis
from dotenv import load_dotenv

load_dotenv()
GRAPH_NAME = "benchmark"


def get_client():
    return redis.Redis(
        host=os.environ["FALKORDB_HOST"],
        port=int(os.environ["FALKORDB_PORT"]),
        username=os.environ.get("FALKORDB_USERNAME"),
        password=os.environ["FALKORDB_PASSWORD"],
        decode_responses=True,
        ssl=False,
        socket_connect_timeout=30,
        socket_timeout=120,
    )


def query(client, cypher):
    return client.execute_command(
        "GRAPH.QUERY", GRAPH_NAME, cypher, "--compact"
    )


def main():
    client = get_client()
    print("FalkorDB dataset verification")
    print("=============================")

    nodes = query(client, "MATCH (n:Person) RETURN count(n) AS count")
    rels = query(client, "MATCH ()-[r:TRUSTS]->() RETURN count(r) AS count")

    print(f"Person nodes: {nodes}")
    print(f"TRUSTS relationships: {rels}")

    print()
    print("Index information:")
    try:
        indexes = client.execute_command("GRAPH.ROUTING", GRAPH_NAME)
        print(indexes)
    except Exception:
        print("Index details not exposed by this endpoint.")

    print()
    print("FalkorDB verification completed.")


if __name__ == "__main__":
    main()
