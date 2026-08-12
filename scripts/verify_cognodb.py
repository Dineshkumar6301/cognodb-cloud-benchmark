import os
from pathlib import Path

from dotenv import load_dotenv
from neo4j import GraphDatabase


PROJECT_ROOT = Path(__file__).resolve().parents[1]

load_dotenv(PROJECT_ROOT / ".env")


def main():
    uri = os.environ["COGNODB_URI"]
    username = os.environ.get(
        "COGNODB_USERNAME",
        "cognodb",
    )
    password = os.environ["COGNODB_PASSWORD"]

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

            relationship_result = session.run(
                """
                MATCH ()-[r:TRUSTS]->()
                RETURN count(r) AS count
                """
            ).single()

            indexed_result = session.run(
                """
                SHOW INDEXES
                """
            )

            indexes = list(indexed_result)

            print("CognoDB dataset verification")
            print("============================")
            print()

            print(
                f"Person nodes: "
                f"{node_result['count']:,}"
            )

            print(
                f"TRUSTS relationships: "
                f"{relationship_result['count']:,}"
            )

            print()
            print("Indexes:")

            for index in indexes:
                print(
                    f"- {index.get('name')} "
                    f"| state={index.get('state')}"
                )

            print()

            if node_result["count"] != 43824:
                raise RuntimeError(
                    "Unexpected node count."
                )

            if relationship_result["count"] != 150000:
                raise RuntimeError(
                    "Unexpected relationship count."
                )

            print(
                "Verification successful."
            )

    finally:
        driver.close()


if __name__ == "__main__":
    main()