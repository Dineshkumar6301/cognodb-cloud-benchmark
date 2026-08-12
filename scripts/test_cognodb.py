import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

driver = GraphDatabase.driver(
    os.getenv("COGNODB_URI"),
    auth=(
        os.getenv("COGNODB_USERNAME"),
        os.getenv("COGNODB_PASSWORD")
    )
)

try:
    with driver.session() as session:
        session.run("""
            MATCH (n:Person)
            WHERE n.name IN ['BenchmarkTestA', 'BenchmarkTestB']
            DETACH DELETE n
        """)

    print("Test data removed successfully.")

finally:
    driver.close()