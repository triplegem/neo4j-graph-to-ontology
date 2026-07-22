from ontology_toolkit.connection import get_driver
from ontology_toolkit.discover_schema import discover_schema
from ontology_toolkit.generate_ontology import save_ontology
from ontology_toolkit.generate_ontology_nary import save_ontology as save_nary_ontology
from ontology_toolkit.generate_shacl import save_shacl
from ontology_toolkit.printer import print_schema
from ontology_toolkit.paths import ONTOLOGY, ONTOLOGY_NARY, SHAPES


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
            print(ONTOLOGY)

            print("\nGenerated N-ary Ontology:")
            print(ONTOLOGY_NARY)

            save_shacl(schema)

            print("\nGenerated SHACL:")
            print(SHAPES)

            print_schema(schema)

            return schema

        finally:

            driver.close()