"""
Ontology Toolkit

Generate SHACL Shapes from a discovered graph schema.
"""

from pathlib import Path

from ontology_toolkit.models import GraphSchema


PREFIXES = """
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix ex: <https://example.org/kg/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

"""


#
# Datatype mapping
#

XSD_TYPES = {
    "string": "xsd:string",
    "integer": "xsd:integer",
    "float": "xsd:decimal",
    "boolean": "xsd:boolean",
    "date": "xsd:date",
    "datetime": "xsd:dateTime",
    "uri": "xsd:anyURI",
    "email": "xsd:string",
    "doi": "xsd:string",
    "orcid": "xsd:string",
    "wikidata_identifier": "xsd:string",
}


#
# Ontology design rules
#

REQUIRED_PROPERTIES = {
    "name",
    "identifier",
    "title",
    "prefLabel",
    "uri",
}

IDENTIFIER_PROPERTIES = {
    "identifier",
    "id",
    "uri",
    "netid",
    "awardNumber",
}


def shacl_datatype(property_definition):

    return XSD_TYPES.get(
        property_definition.data_type,
        "xsd:string"
    )


def generate_shacl(schema: GraphSchema):

    lines = []

    lines.append(PREFIXES)

    #
    # One NodeShape per node label
    #

    for node in sorted(schema.node_types.values(), key=lambda n: n.label):

        lines.append(f"ex:{node.label}Shape")
        lines.append("    a sh:NodeShape ;")
        lines.append(f"    sh:targetClass ex:{node.label} ;")

        #
        # Properties
        #

        for prop in sorted(node.properties.values(), key=lambda p: p.name):

            lines.append("    sh:property [")

            lines.append(
                f"        sh:path ex:{prop.name} ;"
            )

            lines.append(
                f"        sh:datatype {shacl_datatype(prop)} ;"
            )

            #
            # Required property?
            #

            if prop.name in REQUIRED_PROPERTIES:

                lines.append(
                    "        sh:minCount 1 ;"
                )

            #
            # Identifier property?
            #

            if (
                prop.inferred_identifier
                or prop.name in IDENTIFIER_PROPERTIES
            ):

                lines.append(
                    "        sh:maxCount 1 ;"
                )

            lines.append("    ] ;")

        #
        # Remove trailing semicolon
        #

        lines[-1] = lines[-1].rstrip(";")

        lines.append(".")
        lines.append("")

    return "\n".join(lines)


def save_shacl(schema: GraphSchema, filename="shapes.ttl"):

    ttl = generate_shacl(schema)

    Path(filename).write_text(
        ttl,
        encoding="utf-8"
    )

    return filename