"""
Ontology Toolkit

Serialize a SemanticGraph as RDF/Turtle.
"""

from rdflib import Graph

from ontology_toolkit.export_common import (
    bind_namespaces,
    export_entities,
)
from ontology_toolkit.semantic_model import SemanticGraph
from ontology_toolkit.vocab import (
    KGO,
    STANDARD_PREDICATES,
)


def build_graph(
    semantic_graph: SemanticGraph,
) -> Graph:
    """
    Build an RDFLib Graph from a SemanticGraph.
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
    # Export relationships
    #

    for relationship in semantic_graph.relationships:

        predicate = STANDARD_PREDICATES.get(
            relationship.predicate,
            KGO[relationship.predicate],
        )

        graph.add((
            relationship.source_uri,
            predicate,
            relationship.target_uri,
        ))

    return graph


def serialize_rdf(
    semantic_graph: SemanticGraph,
    filename: str = "graph.ttl",
):
    """
    Serialize a SemanticGraph as RDF/Turtle.
    """

    graph = build_graph(
        semantic_graph,
    )

    graph.serialize(
        destination=filename,
        format="turtle",
    )

    return filename