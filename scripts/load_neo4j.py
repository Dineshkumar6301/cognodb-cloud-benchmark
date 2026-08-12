from platforms.neo4j.loader import Neo4jLoader


def main():

    loader = Neo4jLoader()

    try:

        print("Neo4j benchmark dataset loader")
        print("===============================")

        print()
        print("Clearing existing graph...")

        loader.clear_database()

        print("Existing graph cleared.")

        print()
        print("Creating indexes...")

        loader.create_indexes()

        print("Indexes created.")

        print()
        print("Loading nodes...")

        node_result = loader.load_nodes()

        print(
            f"Nodes loaded: "
            f"{node_result['nodes']:,}"
        )

        print(
            f"Node load time: "
            f"{node_result['seconds']:.3f} seconds"
        )

        print(
            f"Node throughput: "
            f"{node_result['nodes_per_second']:,.2f} nodes/sec"
        )

        print()
        print("Loading relationships...")

        edge_result = loader.load_edges()

        print(
            f"Relationships loaded: "
            f"{edge_result['relationships']:,}"
        )

        print(
            f"Relationship load time: "
            f"{edge_result['seconds']:.3f} seconds"
        )

        print(
            f"Relationship throughput: "
            f"{edge_result['relationships_per_second']:,.2f} relationships/sec"
        )

        print()
        print(
            "Neo4j dataset loading completed successfully."
        )

    finally:

        loader.close()


if __name__ == "__main__":
    main()