import os

import redis
from dotenv import load_dotenv


load_dotenv()


def main():

    print("FalkorDB connection test")
    print("=========================")

    host = os.environ["FALKORDB_HOST"]
    port = int(os.environ["FALKORDB_PORT"])
    username = os.environ.get("FALKORDB_USERNAME")
    password = os.environ["FALKORDB_PASSWORD"]

    client = redis.Redis(
        host=host,
        port=port,
        username=username,
        password=password,
        decode_responses=True,
        ssl=False,
    )

    result = client.ping()

    print(f"PING: {result}")

    print()
    print("FalkorDB connection successful.")


if __name__ == "__main__":
    main()