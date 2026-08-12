import os

from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv()


def main():

    uri = os.environ["NEO4J_URI"]
    username = os.environ["NEO4J_USERNAME"]
    password = os.environ["NEO4J_PASSWORD"]

    driver = GraphDatabase.driver(
        uri,
        auth=(username, password),
    )

    try:

        with driver.session() as session:

            node_result = session.run(
                """
                MATCH (p:Person)
                RETURN count(p) AS count
                """
            ).single()

            edge_result = session.run(
                """
                MATCH ()-[r:TRUSTS]->()
                RETURN count(r) AS count
                """
            ).single()

            index_result = session.run(
                """
                SHOW INDEXES
                """
            )

            print("Neo4j dataset verification")
            print("===========================")
            print()

            print(
                f"Person nodes: "
                f"{node_result['count']:,}"
            )

            print(
                f"TRUSTS relationships: "
                f"{edge_result['count']:,}"
            )

            print()
            print("Indexes:")

            for record in index_result:

                print(
                    f"- {record['name']} | "
                    f"state={record['state']}"
                )

            print()
            
            if (
                node_result["count"] == 43824
                and edge_result["count"] == 150000
            ):
                print(
                    "Neo4j verification successful."
                )
            else:
                print(
                    "WARNING: Dataset counts do not match."
                )

    finally:

        driver.close()


if __name__ == "__main__":
    main()