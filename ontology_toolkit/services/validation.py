from pathlib import Path

from ontology_toolkit.connection import get_driver
from ontology_toolkit.neo4j_reader import read_graph

from ontology_toolkit.export_rdf import export_rdf
from ontology_toolkit.export_jsonld import export_jsonld
from ontology_toolkit.export_schema_org import export_schema_org

from ontology_toolkit.validate_shacl import validate_graph


class ValidationService:

    def run(self):

        #
        # Ensure a semantic contract exists
        #

        if not Path("shapes.ttl").exists():
            raise FileNotFoundError(
                "No shapes.ttl found. Run discover.py first to generate "
                "the ontology and SHACL shapes."
            )

        driver = get_driver()

        try:

            driver.verify_connectivity()

            print("Connected to Neo4j!")

            #
            # Read instance data
            #

            semantic_graph = read_graph(driver)

            #
            # Export schema.org JSON-LD
            #

            export_schema_org(semantic_graph)

            print("\nGenerated schema.org JSON-LD:")
            print("schema_org/")

            #
            # Export RDF
            #

            export_rdf(semantic_graph)

            print("\nGenerated RDF:")
            print("graph.ttl")

            #
            # Export JSON-LD
            #

            export_jsonld(semantic_graph)

            print("\nGenerated JSON-LD:")
            print("graph.jsonld")

            #
            # Validate against the existing semantic contract
            #

            validate_graph(
                rdf_file="graph.ttl",
                shacl_file="shapes.ttl",
                report_file="validation_report.txt",
            )

        finally:

            driver.close()