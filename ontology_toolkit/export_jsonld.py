from ontology_toolkit.semantic_model import SemanticGraph
from ontology_toolkit.serializers.jsonld import serialize_jsonld


def export_jsonld(
    semantic_graph: SemanticGraph,
    filename="graph.jsonld",
):
    return serialize_jsonld(
        semantic_graph,
        filename,
    )