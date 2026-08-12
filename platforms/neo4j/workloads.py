import os

from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv()


class Neo4jWorkloads:

    def __init__(self):

        uri = os.environ["NEO4J_URI"]
        username = os.environ["NEO4J_USERNAME"]
        password = os.environ["NEO4J_PASSWORD"]

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

            return session.run(
                query,
                id=node_id,
            ).single()

    def indexed_lookup(self, age):

        query = """
        MATCH (p:Person)
        WHERE p.age = $age
        RETURN count(p) AS count
        """

        with self.driver.session() as session:

            return session.run(
                query,
                age=age,
            ).single()

    def one_hop(self, node_id):

        query = """
        MATCH (p:Person {id: $id})
              -[:TRUSTS]->
              (friend)
        RETURN count(friend) AS count
        """

        with self.driver.session() as session:

            return session.run(
                query,
                id=node_id,
            ).single()

    def two_hop(self, node_id):

        query = """
        MATCH (p:Person {id: $id})
              -[:TRUSTS*2]->
              (friend)
        RETURN count(friend) AS count
        """

        with self.driver.session() as session:

            return session.run(
                query,
                id=node_id,
            ).single()

    def three_hop(self, node_id):

        query = """
        MATCH (p:Person {id: $id})
              -[:TRUSTS*3]->
              (friend)
        RETURN count(friend) AS count
        """

        with self.driver.session() as session:

            return session.run(
                query,
                id=node_id,
            ).single()

    def aggregation(self):

        query = """
        MATCH (p:Person)
        RETURN p.age AS age,
               count(p) AS count
        ORDER BY age
        """

        with self.driver.session() as session:

            return list(
                session.run(query)
            )