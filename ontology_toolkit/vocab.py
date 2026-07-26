"""
Ontology Toolkit

Shared namespaces, datatype mappings, standard predicates,
and helper functions used across ontology generation and RDF serialization.
"""

from rdflib import Namespace
from rdflib.namespace import OWL, SKOS, XSD

from ontology_toolkit.config import (
    ONTOLOGY_NAMESPACE,
    RESOURCE_NAMESPACE,
    SCHEMA_NAMESPACE,
    PROV_NAMESPACE,
)

#
# Namespaces
#

KGO = Namespace(ONTOLOGY_NAMESPACE)
KGR = Namespace(RESOURCE_NAMESPACE)
SCHEMA = Namespace(SCHEMA_NAMESPACE)
PROV = Namespace(PROV_NAMESPACE)

#
# Reuse standard predicates
#

STANDARD_PREDICATES = {

    "prefLabel": SKOS.prefLabel,
    "broader": SKOS.broader,
    "inScheme": SKOS.inScheme,

}

#
# Datatype mapping
#

DATATYPE_MAPPING = {

    "string": XSD.string,
    "integer": XSD.integer,
    "float": XSD.decimal,
    "boolean": XSD.boolean,
    "date": XSD.date,
    "uri": XSD.anyURI,

    #
    # Custom inferred types
    #

    "email": XSD.string,
    "doi": XSD.string,
    "orcid": XSD.string,
    "wikidata_identifier": XSD.string,
}


def relationship_to_predicate(name: str) -> str:
    """
    Convert Neo4j relationship names to RDF-style camelCase.

    AUTHOR_OF -> authorOf
    SAME_AS -> sameAs
    """

    words = name.lower().split("_")

    return words[0] + "".join(
        word.capitalize()
        for word in words[1:]
    )


def relationship_to_class(name: str) -> str:
    """
    Convert Neo4j relationship names to ontology relationship classes.

    AUTHOR_OF -> AuthorOfRelationship
    SAME_AS -> SameAsRelationship
    """

    words = name.lower().split("_")

    return "".join(
        word.capitalize()
        for word in words
    ) + "Relationship"