"""
Ontology Toolkit

Serialize a SemanticGraph as n-ary RDF/Turtle.
"""

from rdflib import Graph
from rdflib.namespace import RDF

from ontology_toolkit.export_common import (
    bind_namespaces,
    export_entities,
    add_literal,
)
from ontology_toolkit.semantic_model import SemanticGraph
from ontology_toolkit.vocab import (
    KGO,
)


def build_graph_nary(
    semantic_graph: SemanticGraph,
) -> Graph:
    """
    Build an RDFLib Graph from a SemanticGraph using
    n-ary relationship resources.
    """

    graph = Graph()

    #
    # Register namespaces
    #

    bind_namespaces(graph)

    #
    # Export entities
    #

    export_entities(
        graph,
        semantic_graph,
    )

    #
    # Export relationships as resources
    #

    for relationship in semantic_graph.relationships:

        relationship_uri = relationship.uri

        #
        # Relationship type
        #

        graph.add((
            relationship_uri,
            RDF.type,
            KGO[relationship.relationship_class],
        ))

        #
        # Source
        #

        graph.add((
            relationship_uri,
            KGO.source,
            relationship.source_uri,
        ))

        #
        # Target
        #

        graph.add((
            relationship_uri,
            KGO.target,
            relationship.target_uri,
        ))

        #
        # Relationship properties
        #

        for key, value in relationship.properties.items():

            add_literal(
                graph,
                relationship_uri,
                KGO[key],
                value,
            )

    return graph


def serialize_rdf_nary(
    semantic_graph: SemanticGraph,
    filename: str = "graph_nary.ttl",
):
    """
    Serialize a SemanticGraph as n-ary RDF/Turtle.
    """

    graph = build_graph_nary(
        semantic_graph,
    )

    graph.serialize(
        destination=filename,
        format="turtle",
    )

    return filename