"""
Ontology Toolkit

Generate an OWL ontology from the discovered graph schema.
"""

from rdflib import Graph, Literal
from rdflib.namespace import RDF, RDFS, OWL, XSD, SKOS

from ontology_toolkit.vocab import (
    KGO,
    SCHEMA,
    CLASS_ALIGNMENT,
    DATATYPE_MAPPING,
    STANDARD_PREDICATES,
    relationship_to_predicate,
)


def save_ontology(schema, filename="ontology.ttl"):

    graph = Graph()

    #
    # Namespaces
    #

    graph.bind("kgo", KGO)
    graph.bind("schema", SCHEMA)
    graph.bind("rdf", RDF)
    graph.bind("rdfs", RDFS)
    graph.bind("owl", OWL)
    graph.bind("xsd", XSD)
    graph.bind("skos", SKOS)

    #
    # Ontology header
    #

    ontology = KGO[""]

    graph.add((ontology, RDF.type, OWL.Ontology))

    graph.add((
        ontology,
        RDFS.label,
        Literal("Cornell Duffield College of Engineering Faculty Expertise Ontology")
    ))

    graph.add((
        ontology,
        RDFS.comment,
        Literal(
            "Ontology supporting an engineering faculty expertise knowledge graph."
        )
    ))

    graph.add((
        ontology,
        OWL.versionInfo,
        Literal("1.0")
    ))

    #
    # Classes
    #

    for label, node in sorted(schema.node_types.items()):

        cls = KGO[label]

        graph.add((cls, RDF.type, OWL.Class))

        graph.add((
            cls,
            RDFS.label,
            Literal(label)
        ))

        if label in CLASS_ALIGNMENT:

            graph.add((
                cls,
                RDFS.subClassOf,
                CLASS_ALIGNMENT[label]
            ))

    #
    # Datatype properties
    #

    for label, node in schema.node_types.items():

        for prop in node.properties.values():

            #
            # Reuse SKOS / OWL properties
            #

            if prop.name in STANDARD_PREDICATES:
                continue

            p = KGO[prop.name]

            graph.add((
                p,
                RDF.type,
                OWL.DatatypeProperty
            ))

            graph.add((
                p,
                RDFS.label,
                Literal(prop.name)
            ))

            graph.add((
                p,
                RDFS.domain,
                KGO[label]
            ))

            if prop.data_type in DATATYPE_MAPPING:

                graph.add((
                    p,
                    RDFS.range,
                    DATATYPE_MAPPING[prop.data_type]
                ))

    #
    # Object properties
    #

    for rel in schema.relationship_types.values():

        predicate_name = relationship_to_predicate(rel.name)

        #
        # Reuse SKOS / OWL predicates
        #

        if predicate_name in STANDARD_PREDICATES:
            continue

        predicate = KGO[predicate_name]

        graph.add((
            predicate,
            RDF.type,
            OWL.ObjectProperty
        ))

        graph.add((
            predicate,
            RDFS.label,
            Literal(predicate_name)
        ))

        for source in sorted(rel.source_labels):

            graph.add((
                predicate,
                RDFS.domain,
                KGO[source]
            ))

        for target in sorted(rel.target_labels):

            graph.add((
                predicate,
                RDFS.range,
                KGO[target]
            ))

    graph.serialize(
        destination=filename,
        format="turtle"
    )

    return filename