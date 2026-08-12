import csv
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from neo4j import GraphDatabase


PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / ".env")


PROJECT_ROOT = Path(__file__).resolve().parents[2]

NODES_FILE = PROJECT_ROOT / "data" / "benchmark" / "nodes_enriched.csv"
EDGES_FILE = PROJECT_ROOT / "data" / "benchmark" / "edges.csv"


BATCH_SIZE = 500


class CognoDBLoader:

    def __init__(self):
        uri = os.environ["COGNODB_URI"]
        username = os.environ.get(
            "COGNODB_USERNAME",
            "cognodb",
        )
        password = os.environ["COGNODB_PASSWORD"]

        self.driver = GraphDatabase.driver(
            uri,
            auth=(username, password),
        )

    def close(self):
        self.driver.close()

    def clear_database(self):

        query = """
        MATCH (n)
        DETACH DELETE n
        """

        with self.driver.session() as session:
            session.run(query).consume()

    def create_indexes(self):

        queries = [
            """
            CREATE INDEX person_id_index IF NOT EXISTS
            FOR (p:Person)
            ON (p.id)
            """,
            """
            CREATE INDEX person_age_index IF NOT EXISTS
            FOR (p:Person)
            ON (p.age)
            """,
            """
            CREATE INDEX person_group_index IF NOT EXISTS
            FOR (p:Person)
            ON (p.benchmark_group)
            """,
        ]

        with self.driver.session() as session:

            for query in queries:
                session.run(query).consume()

    def load_nodes(self):

        start_time = time.perf_counter()

        total_nodes = 0

        batch = []

        with NODES_FILE.open(
            "r",
            newline="",
            encoding="utf-8",
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                batch.append(
                    {
                        "id": int(row["id"]),
                        "age": int(row["age"]),
                        "benchmark_group": row[
                            "benchmark_group"
                        ],
                    }
                )

                if len(batch) >= BATCH_SIZE:

                    self._write_nodes(batch)

                    total_nodes += len(batch)

                    batch.clear()

            if batch:
                self._write_nodes(batch)
                total_nodes += len(batch)

        elapsed = time.perf_counter() - start_time

        nodes_per_second = (
            total_nodes / elapsed
            if elapsed > 0
            else 0
        )

        return {
            "nodes": total_nodes,
            "seconds": elapsed,
            "nodes_per_second": nodes_per_second,
        }

    def _write_nodes(self, batch):

        query = """
        UNWIND $rows AS row

        CREATE (p:Person {
            id: row.id,
            age: row.age,
            benchmark_group: row.benchmark_group
        })
        """

        with self.driver.session() as session:
            session.run(
                query,
                rows=batch,
            ).consume()

    def load_edges(self):

        start_time = time.perf_counter()

        total_edges = 0

        batch = []

        with EDGES_FILE.open(
            "r",
            newline="",
            encoding="utf-8",
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                batch.append(
                    {
                        "source_id": int(
                            row["source_id"]
                        ),
                        "target_id": int(
                            row["target_id"]
                        ),
                    }
                )

                if len(batch) >= BATCH_SIZE:

                    self._write_edges(batch)

                    total_edges += len(batch)

                    batch.clear()

            if batch:
                self._write_edges(batch)
                total_edges += len(batch)

        elapsed = time.perf_counter() - start_time

        edges_per_second = (
            total_edges / elapsed
            if elapsed > 0
            else 0
        )

        return {
            "relationships": total_edges,
            "seconds": elapsed,
            "relationships_per_second": edges_per_second,
        }

    def _write_edges(self, batch):

        query = """
        UNWIND $rows AS row

        MATCH (source:Person {id: row.source_id})
        MATCH (target:Person {id: row.target_id})

        CREATE (source)-[:TRUSTS]->(target)
        """

        with self.driver.session() as session:
            session.run(
                query,
                rows=batch,
            ).consume()