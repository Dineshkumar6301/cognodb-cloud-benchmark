import os

from dotenv import load_dotenv
from gqlalchemy import Memgraph


load_dotenv()


def main():

    host = os.environ["MEMGRAPH_HOST"]
    port = int(os.environ["MEMGRAPH_PORT"])
    username = os.environ["MEMGRAPH_USERNAME"]
    password = os.environ["MEMGRAPH_PASSWORD"]

    memgraph = Memgraph(
        host=host,
        port=port,
        username=username,
        password=password,
        encrypted=True,
    )

    result = memgraph.execute_and_fetch(
        "RETURN 1 AS result"
    )

    row = next(result)

    print("Memgraph connection successful.")
    print(
        f"Test query result: {row['result']}"
    )


if __name__ == "__main__":
    main()