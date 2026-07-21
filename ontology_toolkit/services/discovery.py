from ontology_toolkit.connection import get_driver
from ontology_toolkit.discover_schema import discover_schema
from ontology_toolkit.generate_ontology import save_ontology
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

            print("\nGenerated Ontology:")
            print("ontology.ttl")

            save_shacl(schema)

            print("\nGenerated SHACL:")
            print("shapes.ttl")

            print_schema(schema)

        finally:

            driver.close()