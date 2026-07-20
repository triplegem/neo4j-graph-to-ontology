"""
Ontology Toolkit

Serialize a SemanticGraph as RDF/Turtle.
"""

from rdflib import Graph, Literal
from rdflib.namespace import RDF, RDFS, OWL, SKOS, XSD

from ontology_toolkit.semantic_model import SemanticGraph
from ontology_toolkit.vocab import (
    KGO,
    KGR,
    SCHEMA,
    CLASS_ALIGNMENT,
    STANDARD_PREDICATES,
)


def add_literal(graph, subject, predicate, value):
    """
    Add a literal using the most appropriate XSD datatype.
    """

    if value is None:
        return

    if isinstance(value, bool):

        graph.add((
            subject,
            predicate,
            Literal(value, datatype=XSD.boolean)
        ))
        return

    if isinstance(value, int):

        graph.add((
            subject,
            predicate,
            Literal(value, datatype=XSD.integer)
        ))
        return

    if isinstance(value, float):

        graph.add((
            subject,
            predicate,
            Literal(value, datatype=XSD.decimal)
        ))
        return

    text = str(value)

    #
    # ISO date
    #

    if (
        len(text) == 10
        and text[4] == "-"
        and text[7] == "-"
    ):

        graph.add((
            subject,
            predicate,
            Literal(text, datatype=XSD.date)
        ))
        return

    #
    # URI
    #

    if text.startswith("http://") or text.startswith("https://"):

        graph.add((
            subject,
            predicate,
            Literal(text, datatype=XSD.anyURI)
        ))
        return

    #
    # Default string
    #

    graph.add((
        subject,
        predicate,
        Literal(text)
    ))


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

    graph.bind("kgo", KGO)
    graph.bind("kgr", KGR)
    graph.bind("schema", SCHEMA)
    graph.bind("rdf", RDF)
    graph.bind("rdfs", RDFS)
    graph.bind("owl", OWL)
    graph.bind("skos", SKOS)
    graph.bind("xsd", XSD)

    #
    # Export entities
    #

    for entity in semantic_graph.entities:

        subject = entity.uri
        class_name = entity.class_name

        #
        # Local ontology class
        #

        graph.add((
            subject,
            RDF.type,
            KGO[class_name]
        ))

        #
        # Standard vocabulary alignment
        #

        if class_name in CLASS_ALIGNMENT:

            graph.add((
                subject,
                RDF.type,
                CLASS_ALIGNMENT[class_name]
            ))

        #
        # Datatype properties
        #

        for key, value in entity.properties.items():

            predicate = STANDARD_PREDICATES.get(
                key,
                KGO[key]
            )

            add_literal(
                graph,
                subject,
                predicate,
                value,
            )

    #
    # Export relationships
    #

    for relationship in semantic_graph.relationships:

        predicate = STANDARD_PREDICATES.get(
            relationship.predicate,
            KGO[relationship.predicate]
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

    graph = build_graph(semantic_graph)

    graph.serialize(
        destination=filename,
        format="turtle",
    )

    return filename