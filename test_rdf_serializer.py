from ontology_toolkit.connection import get_driver
from ontology_toolkit.neo4j_reader import read_graph
from ontology_toolkit.serializers.rdf import build_graph


def main():

    driver = get_driver()

    try:

        driver.verify_connectivity()

        print("Connected to Neo4j!")

        semantic_graph = read_graph(driver)

        graph = build_graph(semantic_graph)

        print(f"Entities: {semantic_graph.entity_count}")
        print(f"Relationships: {semantic_graph.relationship_count}")
        print(f"RDF triples: {len(graph)}")

        minimum_triples = (
            semantic_graph.entity_count
            + semantic_graph.relationship_count
        )

        assert len(graph) >= minimum_triples

        print("\n✓ RDF serializer test passed.")

    finally:

        driver.close()


if __name__ == "__main__":
    main()