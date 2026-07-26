from rdflib import Graph
from owlrl import DeductiveClosure, OWLRL_Semantics

def apply_reasoning(graph: Graph) -> Graph:
    """
    Apply OWL RL reasoning to an RDF graph.

    Returns the expanded graph.
    """
    DeductiveClosure(OWLRL_Semantics).expand(graph)
    return graph