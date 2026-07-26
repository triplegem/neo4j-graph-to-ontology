from rdflib import Graph, Literal
from rdflib.namespace import OWL, RDF, RDFS, XSD

from ontology_toolkit.vocab import KGO

ONTOLOGY_NS = str(KGO)


def clean_inferred_graph(graph: Graph) -> Graph:
    """
    Remove OWL RL axiomatic triples from an inferred graph while
    preserving inferred facts about application resources.
    """

    cleaned = Graph()

    ontology_terms = {
        OWL.Class,
        OWL.ObjectProperty,
        OWL.DatatypeProperty,
        OWL.FunctionalProperty,
        OWL.Ontology,
    }

    for s, p, o in graph:

        # Remove reflexive owl:sameAs
        if p == OWL.sameAs and s == o:
            continue

        # Remove triples about built-in vocabularies
        if (
            str(s).startswith(str(OWL))
            or str(s).startswith(str(RDF))
            or str(s).startswith(str(RDFS))
            or str(s).startswith(str(XSD))
        ):
            continue

        # Remove datatype declarations
        if p == RDF.type and o == RDFS.Datatype:
            continue

        # Remove datatype typing of literals
        if isinstance(s, Literal) and p == RDF.type:
            continue

        # Remove ontology schema definitions
        if p == RDF.type and o in ontology_terms:
            continue

        # Remove metadata describing ontology terms
        if (
            str(s).startswith(ONTOLOGY_NS)
            and p in {
                RDFS.label,
                RDFS.comment,
                RDFS.domain,
                RDFS.range,
                RDFS.subClassOf,
                RDFS.subPropertyOf,
                OWL.equivalentClass,
                OWL.equivalentProperty,
                OWL.inverseOf,
            }
        ):
            continue

        # Remove ontology metadata
        if str(s) == ONTOLOGY_NS:
            continue

        cleaned.add((s, p, o))

    return cleaned