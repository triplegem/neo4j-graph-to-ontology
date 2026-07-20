"""
Test reading a Neo4j database into a SemanticGraph.
"""

import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

from ontology_toolkit.neo4j_reader import read_graph


def main():
    load_dotenv()

    driver = GraphDatabase.driver(
        os.environ["NEO4J_URI"],
        auth=(
            os.environ["NEO4J_USERNAME"],
            os.environ["NEO4J_PASSWORD"],
        ),
    )

    print("Connected to Neo4j!\n")

    graph = read_graph(driver)

    print(graph)
    print()

    print(f"Entity count: {graph.entity_count}")
    print(f"Relationship count: {graph.relationship_count}")
    print(f"Total graph elements: {len(graph)}")
    print(f"Graph is empty: {graph.is_empty}")

    print("\nFirst five entities:\n")

    for entity in graph.entities[:5]:
        print(entity)

    driver.close()

    print("\n✓ Neo4j reader test passed.")


if __name__ == "__main__":
    main()