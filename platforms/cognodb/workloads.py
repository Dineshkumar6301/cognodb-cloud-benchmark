import os
from pathlib import Path

from dotenv import load_dotenv
from neo4j import GraphDatabase


PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / ".env")


class CognoDBWorkloads:

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

    def point_lookup(self, node_id):

        query = """
        MATCH (p:Person {id: $id})
        RETURN p.id AS id,
               p.age AS age,
               p.benchmark_group AS benchmark_group
        """

        with self.driver.session() as session:

            result = session.run(
                query,
                id=node_id,
            )

            return result.single()

    def indexed_lookup(self, age):

        query = """
        MATCH (p:Person)
        WHERE p.age = $age
        RETURN count(p) AS count
        """

        with self.driver.session() as session:

            result = session.run(
                query,
                age=age,
            )

            return result.single()

    def one_hop(self, node_id):

        query = """
        MATCH (p:Person {id: $id})
            -[:TRUSTS]->
            (friend)
        RETURN count(friend) AS count
        """

        with self.driver.session() as session:
            result = session.run(
                query,
                id=node_id,
            )
            return result.single()


    def two_hop(self, node_id):

        query = """
        MATCH (p:Person {id: $id})
            -[:TRUSTS*2]->
            (friend)
        RETURN count(friend) AS count
        """

        with self.driver.session() as session:
            result = session.run(
                query,
                id=node_id,
            )
            return result.single()


    def three_hop(self, node_id):

        query = """
        MATCH (p:Person {id: $id})
            -[:TRUSTS*3]->
            (friend)
        RETURN count(friend) AS count
        """

        with self.driver.session() as session:
            result = session.run(
                query,
                id=node_id,
            )
            return result.single()

    def aggregation(self):

        query = """
        MATCH (p:Person)
        RETURN p.age AS age,
               count(*) AS count
        ORDER BY age
        """

        with self.driver.session() as session:

            result = session.run(query)

            return list(result)