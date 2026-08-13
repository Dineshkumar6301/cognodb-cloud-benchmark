import os

from dotenv import load_dotenv
from gqlalchemy import Memgraph


load_dotenv()


class MemgraphWorkloads:

    def __init__(self):

        self.db = Memgraph(
            host=os.environ["MEMGRAPH_HOST"],
            port=int(os.environ["MEMGRAPH_PORT"]),
            username=os.environ["MEMGRAPH_USERNAME"],
            password=os.environ["MEMGRAPH_PASSWORD"],
            encrypted=True,
        )

    def point_lookup(self, node_id):

        query = """
        MATCH (p:Person {id: $id})
        RETURN p.id AS id,
               p.age AS age,
               p.benchmark_group AS benchmark_group
        """

        result = self.db.execute_and_fetch(
            query,
            {"id": node_id},
        )

        return next(result)

    def indexed_lookup(self, age):

        query = """
        MATCH (p:Person)
        WHERE p.age = $age
        RETURN count(p) AS count
        """

        result = self.db.execute_and_fetch(
            query,
            {"age": age},
        )

        return next(result)

    def one_hop(self, node_id):

        query = """
        MATCH (p:Person {id: $id})
              -[:TRUSTS]->
              (friend)
        RETURN count(friend) AS count
        """

        result = self.db.execute_and_fetch(
            query,
            {"id": node_id},
        )

        return next(result)

    def two_hop(self, node_id):

        query = """
        MATCH (p:Person {id: $id})
              -[:TRUSTS*2]->
              (friend)
        RETURN count(friend) AS count
        """

        result = self.db.execute_and_fetch(
            query,
            {"id": node_id},
        )

        return next(result)

    def three_hop(self, node_id):

        query = """
        MATCH (p:Person {id: $id})
              -[:TRUSTS*3]->
              (friend)
        RETURN count(friend) AS count
        """

        result = self.db.execute_and_fetch(
            query,
            {"id": node_id},
        )

        return next(result)

    def aggregation(self):

        query = """
        MATCH (p:Person)
        RETURN p.age AS age,
               count(p) AS count
        ORDER BY age
        """

        return list(
            self.db.execute_and_fetch(query)
        )