"""
Ontology Toolkit

Export a SemanticGraph as RDF/Turtle.
"""

from ontology_toolkit.serializers.rdf import serialize_rdf
from ontology_toolkit.semantic_model import SemanticGraph


def export_rdf(
    semantic_graph: SemanticGraph,
    filename: str = "graph.ttl",
):
    """
    Export a SemanticGraph as RDF/Turtle.
    """

    return serialize_rdf(
        semantic_graph,
        filename,
    )