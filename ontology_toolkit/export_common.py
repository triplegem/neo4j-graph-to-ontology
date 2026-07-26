"""
Ontology Toolkit

Shared utilities for RDF serialization.
"""

from rdflib import Graph, Literal
from rdflib.namespace import RDF, RDFS, OWL, SKOS, XSD

from ontology_toolkit.semantic_model import SemanticGraph
from ontology_toolkit.vocab import (
    KGO,
    KGR,
    SCHEMA,
    PROV,
    STANDARD_PREDICATES,
)

from ontology_toolkit.profiles.faculty import FACULTY_PROFILE


def bind_namespaces(graph: Graph) -> None:
    """
    Register namespaces used by RDF serializers.
    """

    graph.bind("kgo", KGO)
    graph.bind("kgr", KGR)
    graph.bind("schema", SCHEMA)
    graph.bind("prov", PROV)
    graph.bind("rdf", RDF)
    graph.bind("rdfs", RDFS)
    graph.bind("owl", OWL)
    graph.bind("skos", SKOS)
    graph.bind("xsd", XSD)


def add_literal(
    graph: Graph,
    subject,
    predicate,
    value,
) -> None:
    """
    Add a literal using the most appropriate XSD datatype.
    """

    if value is None:
        return

    #
    # Boolean
    #

    if isinstance(value, bool):

        graph.add((
            subject,
            predicate,
            Literal(value, datatype=XSD.boolean),
        ))

        return

    #
    # Integer
    #

    if isinstance(value, int):

        graph.add((
            subject,
            predicate,
            Literal(value, datatype=XSD.integer),
        ))

        return

    #
    # Decimal
    #

    if isinstance(value, float):

        graph.add((
            subject,
            predicate,
            Literal(value, datatype=XSD.decimal),
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
            Literal(text, datatype=XSD.date),
        ))

        return

    #
    # URI
    #

    if (
        text.startswith("http://")
        or text.startswith("https://")
    ):

        graph.add((
            subject,
            predicate,
            Literal(text, datatype=XSD.anyURI),
        ))

        return

    #
    # Default string
    #

    graph.add((
        subject,
        predicate,
        Literal(text),
    ))


def export_entities(
    graph: Graph,
    semantic_graph: SemanticGraph,
) -> None:
    """
    Export all entity instances to an RDF graph.
    """

    for entity in semantic_graph.entities:

        subject = entity.uri
        class_name = entity.class_name

        #
        # Local ontology class
        #

        graph.add((
            subject,
            RDF.type,
            KGO[class_name],
        ))

        #
        # Standard vocabulary alignment
        #

        for alignment in FACULTY_PROFILE.class_alignments.get(class_name, []):

            graph.add((
                subject,
                RDF.type,
                alignment.target,
            ))

        #
        # Datatype properties
        #

        for key, value in entity.properties.items():

            predicate = STANDARD_PREDICATES.get(
                key,
                KGO[key],
            )

            add_literal(
                graph,
                subject,
                predicate,
                value,
            )