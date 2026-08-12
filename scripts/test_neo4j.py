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

            result = session.run(
                "RETURN 1 AS result"
            ).single()

            print(
                "Neo4j connection successful."
            )

            print(
                f"Test query result: "
                f"{result['result']}"
            )

    finally:

        driver.close()


if __name__ == "__main__":
    main()