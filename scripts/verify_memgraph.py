import os

from dotenv import load_dotenv
from gqlalchemy import Memgraph


load_dotenv()


def main():

    db = Memgraph(
        host=os.environ["MEMGRAPH_HOST"],
        port=int(os.environ["MEMGRAPH_PORT"]),
        username=os.environ["MEMGRAPH_USERNAME"],
        password=os.environ["MEMGRAPH_PASSWORD"],
        encrypted=True,
    )

    print("Memgraph dataset verification")
    print("=============================")
    print()

    # Count nodes
    result = db.execute_and_fetch(
        """
        MATCH (p:Person)
        RETURN count(p) AS count
        """
    )

    node_count = next(result)["count"]

    # Count relationships
    result = db.execute_and_fetch(
        """
        MATCH ()-[r:TRUSTS]->()
        RETURN count(r) AS count
        """
    )

    relationship_count = next(result)["count"]

    # Check indexes
    result = db.execute_and_fetch(
        """
        SHOW INDEX INFO
        """
    )

    indexes = list(result)

    print(
        f"Person nodes: {node_count:,}"
    )

    print(
        f"TRUSTS relationships: "
        f"{relationship_count:,}"
    )

    print()
    print("Indexes:")

    for index in indexes:
        print(index)

    print()

    if (
        node_count == 43824
        and relationship_count == 150000
    ):
        print(
            "Memgraph verification successful."
        )
    else:
        print(
            "WARNING: Dataset counts do not match."
        )


if __name__ == "__main__":
    main()