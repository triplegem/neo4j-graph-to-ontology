"""
Ontology Toolkit

Export a SemanticGraph as n-ary RDF/Turtle.
"""

from ontology_toolkit.serializers.rdf_nary import serialize_rdf_nary
from ontology_toolkit.semantic_model import SemanticGraph


def export_rdf_nary(
    semantic_graph: SemanticGraph,
    filename: str = "graph_nary.ttl",
):
    """
    Export a SemanticGraph as n-ary RDF/Turtle.
    """

    return serialize_rdf_nary(
        semantic_graph,
        filename,
    )