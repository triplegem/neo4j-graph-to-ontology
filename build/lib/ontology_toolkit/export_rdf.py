"""
Ontology Toolkit

Export a SemanticGraph as RDF/Turtle.
"""

from ontology_toolkit.serializers.rdf import serialize_rdf
from ontology_toolkit.semantic_model import SemanticGraph
from ontology_toolkit.paths import GRAPH


def export_rdf(
    semantic_graph: SemanticGraph,
    filename: str = GRAPH,
):
    """
    Export a SemanticGraph as RDF/Turtle.
    """

    return serialize_rdf(
        semantic_graph,
        filename,
    )