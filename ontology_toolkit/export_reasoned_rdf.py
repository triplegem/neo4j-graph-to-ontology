from rdflib import Graph

from ontology_toolkit.clean_inferred import clean_inferred_graph
from ontology_toolkit.paths import GRAPH_INFERRED, GRAPH_INFERRED_CLEAN, ONTOLOGY
from ontology_toolkit.reasoning import apply_reasoning


def export_reasoned_rdf(graph: Graph, filename=GRAPH_INFERRED):
    """
    Apply OWL RL reasoning and serialize both the raw and cleaned
    inferred graphs.
    """

    reasoned_graph = Graph()

    reasoned_graph.parse(ONTOLOGY, format="turtle")

    for triple in graph:
        reasoned_graph.add(triple)

    apply_reasoning(reasoned_graph)

    # Raw output
    reasoned_graph.serialize(filename, format="turtle")

    # Clean output
    clean_graph = clean_inferred_graph(reasoned_graph)
    clean_graph.serialize(GRAPH_INFERRED_CLEAN, format="turtle")