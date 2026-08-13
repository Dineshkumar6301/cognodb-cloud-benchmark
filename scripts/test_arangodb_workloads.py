import os

from arango import ArangoClient
from dotenv import load_dotenv

load_dotenv()

GRAPH_NAME = "benchmark_graph"
VERTEX = "persons"
EDGE = "trusts"

START_NODES = [70705, 8140, 1702, 22815, 19942]


def get_db():
    client = ArangoClient(hosts=os.environ["ARANGODB_URL"])
    return client.db(
        "_system",
        username=os.environ["ARANGODB_USERNAME"],
        password=os.environ["ARANGODB_PASSWORD"],
    )


def query(db, text, bind_vars=None):
    cursor = db.aql.execute(
        text,
        bind_vars=bind_vars or {},
    )
    return list(cursor)


def main():
    print("ArangoDB workload test")
    print("======================")
    print()
    print("Test start nodes:")
    print(START_NODES)

    db = get_db()

    start = START_NODES[0]

    print()
    print("1. Point lookup")

    result = query(
        db,
        """
        FOR p IN persons
            FILTER p.id == @id
            RETURN p
        """,
        {"id": start},
    )

    print(result[0])

    print()
    print("2. Indexed lookup")

    result = query(
        db,
        """
        FOR p IN persons
            FILTER p.age == @age
            COLLECT WITH COUNT INTO count
            RETURN {count}
        """,
        {"age": 21},
    )

    print(result[0])

    print()
    print("3. One-hop traversal")

    result = query(
        db,
        """
        FOR v IN 1..1 OUTBOUND
            CONCAT(@collection, "/", @id)
            trusts
            RETURN v
        """,
        {
            "collection": VERTEX,
            "id": start,
        },
    )

    print({"count": len(result)})

    print()
    print("4. Two-hop traversal")

    result = query(
        db,
        """
        FOR v IN 2..2 OUTBOUND
            CONCAT(@collection, "/", @id)
            trusts
            RETURN v
        """,
        {
            "collection": VERTEX,
            "id": start,
        },
    )

    print({"count": len(result)})

    print()
    print("5. Three-hop traversal")

    result = query(
        db,
        """
        FOR v IN 3..3 OUTBOUND
            CONCAT(@collection, "/", @id)
            trusts
            RETURN v
        """,
        {
            "collection": VERTEX,
            "id": start,
        },
    )

    print({"count": len(result)})

    print()
    print("6. Aggregation")

    result = query(
        db,
        """
        FOR p IN persons
            COLLECT group = p.benchmark_group
            AGGREGATE count = COUNT()
            RETURN {
                benchmark_group: group,
                count: count
            }
        """,
    )

    print(f"Aggregation groups: {len(result)}")

    print()
    print("All ArangoDB workload queries executed successfully.")


if __name__ == "__main__":
    main()