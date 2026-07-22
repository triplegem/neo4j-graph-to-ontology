from pathlib import Path

from ontology_toolkit.semantic_model import SemanticGraph
from ontology_toolkit.serializers.rdf import build_graph

JSONLD_CONTEXT = {
    "schema": "https://schema.org/",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "kgo": "https://kg.engineering.cornell.edu/ontology#",
}


def serialize_jsonld(
    semantic_graph: SemanticGraph,
    filename: str | Path,
):
    """
    Serialize a SemanticGraph as JSON-LD.
    """

    graph = build_graph(semantic_graph)

    graph.serialize(
        destination=filename,
        format="json-ld",
        context=JSONLD_CONTEXT,
        auto_compact=True,
        indent=4,
    )

    return filename