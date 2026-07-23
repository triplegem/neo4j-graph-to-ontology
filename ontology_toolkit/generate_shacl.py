"""
Ontology Toolkit

Generate SHACL Shapes from a discovered graph schema.
"""

from pathlib import Path

from ontology_toolkit.schema_model import GraphSchema
from ontology_toolkit.vocab import relationship_to_predicate
from ontology_toolkit.paths import SHAPES

from ontology_toolkit.config import (
    ONTOLOGY_PREFIX,
    RESOURCE_PREFIX,
    ONTOLOGY_NAMESPACE,
    RESOURCE_NAMESPACE,
)


PREFIXES = f"""
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix {ONTOLOGY_PREFIX}: <{ONTOLOGY_NAMESPACE}> .
@prefix {RESOURCE_PREFIX}: <{RESOURCE_NAMESPACE}> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

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
# Standard vocabulary mappings
#

STANDARD_PATHS = {
    "prefLabel": "skos:prefLabel",
    "broader": "skos:broader",
    "inScheme": "skos:inScheme",
    "exactMatch": "skos:exactMatch",
    "sameAs": "owl:sameAs",
}


#
# Explicit ontology design rules
#

DESIGN_RULES = {

    # Human-readable labels

    "name": {
        "minCount": 1,
        "maxCount": 1,
    },

    "title": {
        "minCount": 1,
        "maxCount": 1,
    },

    "prefLabel": {
        "minCount": 1,
        "maxCount": 1,
    },

    # Identifiers

    "identifier": {
        "minCount": 1,
        "maxCount": 1,
    },

    "uri": {
        "minCount": 1,
        "maxCount": 1,
    },

    "awardNumber": {
        "minCount": 1,
        "maxCount": 1,
    },

    "netid": {
        "maxCount": 1,
    },

    "email": {
        "maxCount": 1,
    },

}


def shacl_datatype(property_definition):

    return XSD_TYPES.get(
        property_definition.data_type,
        "xsd:string"
    )


def shacl_path(name: str) -> str:
    """
    Return the SHACL path for a property or relationship,
    reusing standard vocabularies where applicable.
    """

    return STANDARD_PATHS.get(
        name,
        f"kgo:{name}"
    )


def generate_shacl(schema: GraphSchema):

    lines = []

    lines.append(PREFIXES)

    #
    # One NodeShape per node label
    #

    for node in sorted(
        schema.node_types.values(),
        key=lambda n: n.label
    ):

        lines.append(f"kgo:{node.label}Shape")
        lines.append("    a sh:NodeShape ;")
        lines.append(f"    sh:targetClass kgo:{node.label} ;")

        #
        # Properties
        #

        for prop in sorted(
            node.properties.values(),
            key=lambda p: p.name
        ):

            lines.append("    sh:property [")

            #
            # Reuse standard vocabularies
            #

            path = shacl_path(prop.name)

            lines.append(
                f"        sh:path {path} ;"
            )

            lines.append(
                f"        sh:datatype {shacl_datatype(prop)} ;"
            )

            #
            # Explicit ontology rules
            #

            rules = DESIGN_RULES.get(prop.name, {})

            if "minCount" in rules:

                lines.append(
                    f"        sh:minCount {rules['minCount']} ;"
                )

            if "maxCount" in rules:

                lines.append(
                    f"        sh:maxCount {rules['maxCount']} ;"
                )

            #
            # Otherwise fall back to inferred identifier
            #

            elif prop.inferred_identifier:

                lines.append(
                    "        sh:maxCount 1 ;"
                )

            #
            # Suggested enumeration
            #

            if (
                prop.inferred_enum
                and prop.enum_values
            ):

                enum_values = " ".join(
                    f'"{value}"'
                    for value in prop.enum_values
                )

                lines.append(
                    f"        sh:in ( {enum_values} ) ;"
                )

            lines.append("    ] ;")

        #
        # Outgoing relationships
        #

        for relationship in sorted(
            schema.relationship_types.values(),
            key=lambda r: r.name
        ):

            predicate = relationship_to_predicate(
                relationship.name
            )

            path = shacl_path(predicate)

            #
            # Generate one constraint for each discovered
            # source → target label combination.
            #

            for source_label, target_label in sorted(
                relationship.allowed_label_pairs
            ):

                if source_label != node.label:
                    continue

                lines.append("    sh:property [")

                lines.append(
                    f"        sh:path {path} ;"
                )

                lines.append(
                    "        sh:nodeKind sh:IRI ;"
                )

                lines.append(
                    f"        sh:class kgo:{target_label} ;"
                )

                lines.append("    ] ;")

        #
        # Remove trailing semicolon from final property
        #

        lines[-1] = lines[-1].rstrip(" ;")

        lines.append(".")
        lines.append("")

    return "\n".join(lines)


def save_shacl(schema, filename=SHAPES):
    ttl = generate_shacl(schema)

    filename.write_text(ttl, encoding="utf-8")

    return filename