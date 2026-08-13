import os

from arango import ArangoClient
from dotenv import load_dotenv


load_dotenv()


def main():
    print("ArangoDB connection test")
    print("========================")

    client = ArangoClient(
        hosts=os.environ["ARANGODB_URL"]
    )

    db = client.db(
        "_system",
        username=os.environ["ARANGODB_USERNAME"],
        password=os.environ["ARANGODB_PASSWORD"],
    )

    version = db.version()

    print(f"Version: {version}")
    print()
    print("ArangoDB connection successful.")


if __name__ == "__main__":
    main()