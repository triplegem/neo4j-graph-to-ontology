from ontology_toolkit.connection import get_driver
from ontology_toolkit.discover_schema import discover_schema
from ontology_toolkit.generate_ontology import save_ontology
from ontology_toolkit.generate_ontology_nary import save_ontology as save_nary_ontology
from ontology_toolkit.generate_shacl import save_shacl
from ontology_toolkit.printer import print_schema


class DiscoveryService:

    def run(self):

        driver = get_driver()

        try:

            driver.verify_connectivity()

            print("Connected to Neo4j!")

            schema = discover_schema(driver)

            save_ontology(schema)
            save_nary_ontology(schema)

            print("\nGenerated Binary Ontology:")
            print("ontology.ttl")

            print("\nGenerated N-ary Ontology:")
            print("ontology_nary.ttl")

            save_shacl(schema)

            print("\nGenerated SHACL:")
            print("shapes.ttl")

            print_schema(schema)

            return schema

        finally:

            driver.close()