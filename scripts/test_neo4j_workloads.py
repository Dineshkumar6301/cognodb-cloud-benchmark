from platforms.neo4j.workloads import (
    Neo4jWorkloads,
)


START_NODES = [
    70705,
    8140,
    1702,
    22815,
    19942,
]


def main():

    db = Neo4jWorkloads()

    try:

        print("Neo4j workload test")
        print("===================")

        print()
        print("Test start nodes:")
        print(START_NODES)

        print()
        print("1. Point lookup")

        result = db.point_lookup(
            START_NODES[0]
        )

        print(result)

        print()
        print("2. Indexed lookup")

        result = db.indexed_lookup(25)

        print(result)

        print()
        print("3. One-hop traversal")

        result = db.one_hop(
            START_NODES[0]
        )

        print(result)

        print()
        print("4. Two-hop traversal")

        result = db.two_hop(
            START_NODES[0]
        )

        print(result)

        print()
        print("5. Three-hop traversal")

        result = db.three_hop(
            START_NODES[0]
        )

        print(result)

        print()
        print("6. Aggregation")

        result = db.aggregation()

        print(
            f"Aggregation groups: {len(result)}"
        )

        print()
        print(
            "All Neo4j workload queries "
            "executed successfully."
        )

    finally:

        db.close()


if __name__ == "__main__":
    main()