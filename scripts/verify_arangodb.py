import os

from arango import ArangoClient
from dotenv import load_dotenv

load_dotenv()

GRAPH_NAME = "benchmark_graph"
VERTEX_COLLECTION = "persons"
EDGE_COLLECTION = "trusts"


def main():
    print("ArangoDB dataset verification")
    print("=============================")

    client = ArangoClient(
        hosts=os.environ["ARANGODB_URL"]
    )

    db = client.db(
        "_system",
        username=os.environ["ARANGODB_USERNAME"],
        password=os.environ["ARANGODB_PASSWORD"],
    )

    persons = db.collection(VERTEX_COLLECTION)
    trusts = db.collection(EDGE_COLLECTION)

    print(f"Person nodes: {persons.count()}")
    print(f"TRUSTS relationships: {trusts.count()}")

    print()
    print(f"Graph exists: {db.has_graph(GRAPH_NAME)}")
    print(f"Person collection exists: {db.has_collection(VERTEX_COLLECTION)}")
    print(f"TRUSTS collection exists: {db.has_collection(EDGE_COLLECTION)}")

    if persons.count() != 43824:
        raise RuntimeError("Unexpected Person node count")

    if trusts.count() != 150000:
        raise RuntimeError("Unexpected TRUSTS relationship count")

    print()
    print("ArangoDB verification successful.")


if __name__ == "__main__":
    main()