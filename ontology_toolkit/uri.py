"""
Ontology Toolkit

Utilities for generating stable URIs for knowledge graph resources.
"""

from urllib.parse import quote

from ontology_toolkit.vocab import KGR

#
# Properties used to generate stable resource URIs.
# Earlier properties have higher priority.
#

IDENTIFIER_PROPERTIES = [
    "identifier",
    "netid",
    "uri",
    "awardNumber",
    "name",
]


def make_uri(class_name: str, properties: dict):
    """
    Create a stable URI for an instance resource.

    The first available identifier property is used to generate a
    human-readable URI. If no suitable identifier exists, a fallback
    URI is generated using Python's object id.
    """

    for key in IDENTIFIER_PROPERTIES:

        if key in properties and properties[key]:

            value = quote(
                str(properties[key])
                .lower()
                .replace(" ", "-")
            )

            return KGR[f"{class_name.lower()}/{value}"]

    #
    # Fallback
    #

    return KGR[f"{class_name.lower()}/{id(properties)}"]


def make_relationship_uri(
    relationship_type: str,
    element_id: str,
):
    """
    Create a stable URI for a relationship resource.

    Relationship resources are identified using their Neo4j
    relationship type together with the Neo4j elementId.
    """

    relationship = quote(relationship_type.lower())
    element = quote(element_id)

    return KGR[f"relationship/{relationship}/{element}"]