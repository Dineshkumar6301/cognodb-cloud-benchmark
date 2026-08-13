import os

import redis
from dotenv import load_dotenv

load_dotenv()
GRAPH_NAME = "benchmark"
START_NODES = [70705, 8140, 1702, 22815, 19942]


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
    print("FalkorDB workload test")
    print("======================")
    print()
    print("Test start nodes:")
    print(START_NODES)

    node_id = START_NODES[0]

    print("\n1. Point lookup")
    print(query(client, f"MATCH (n:Person {{id: {node_id}}}) RETURN n"))

    print("\n2. Indexed lookup")
    print(query(client, "MATCH (n:Person {age: 21}) RETURN count(n) AS count"))

    print("\n3. One-hop traversal")
    print(query(
        client,
        f"MATCH (n:Person {{id: {node_id}}})-[:TRUSTS]->(m) "
        "RETURN count(m) AS count",
    ))

    print("\n4. Two-hop traversal")
    print(query(
        client,
        f"MATCH (n:Person {{id: {node_id}}})-[:TRUSTS*2]->(m) "
        "RETURN count(m) AS count",
    ))

    print("\n5. Three-hop traversal")
    print(query(
        client,
        f"MATCH (n:Person {{id: {node_id}}})-[:TRUSTS*3]->(m) "
        "RETURN count(m) AS count",
    ))

    print("\n6. Aggregation")
    print(query(
        client,
        "MATCH (n:Person) RETURN n.benchmark_group AS grp, count(n) AS count",
    ))

    print("\nAll FalkorDB workload queries executed successfully.")


if __name__ == "__main__":
    main()
