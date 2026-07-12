from ontology_toolkit.connection import get_driver
from ontology_toolkit.discover_schema import discover_schema
from ontology_toolkit.printer import print_schema
from ontology_toolkit.generate_shacl import save_shacl
from ontology_toolkit.export_rdf import export_rdf
from ontology_toolkit.generate_ontology import save_ontology


def main():

    driver = get_driver()

    try:

        driver.verify_connectivity()

        print("Connected to Neo4j!")

        #
        # Discover schema
        #

        schema = discover_schema(driver)

        save_ontology(schema)

        print("\nGenerated Ontology:")
        print("ontology.ttl")

        #
        # Export RDF
        #

        export_rdf(driver)

        print("\nGenerated RDF:")
        print("graph.ttl")

        #
        # Generate SHACL
        #

        save_shacl(schema)

        print("\nGenerated SHACL:")
        print("shapes.ttl")

        #
        # Print discovered schema
        #

        print_schema(schema)

    finally:

        driver.close()


if __name__ == "__main__":
    main()