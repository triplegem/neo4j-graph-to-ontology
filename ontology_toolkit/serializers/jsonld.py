from pathlib import Path

from ontology_toolkit.config import (
    ONTOLOGY_PREFIX,
    ONTOLOGY_NAMESPACE,
    SCHEMA_PREFIX,
    SCHEMA_NAMESPACE,
    SKOS_PREFIX,
    SKOS_NAMESPACE,
    OWL_PREFIX,
    OWL_NAMESPACE,
)
from ontology_toolkit.semantic_model import SemanticGraph
from ontology_toolkit.serializers.rdf import build_graph


JSONLD_CONTEXT = {
    SCHEMA_PREFIX: SCHEMA_NAMESPACE,
    SKOS_PREFIX: SKOS_NAMESPACE,
    OWL_PREFIX: OWL_NAMESPACE,
    ONTOLOGY_PREFIX: ONTOLOGY_NAMESPACE,
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