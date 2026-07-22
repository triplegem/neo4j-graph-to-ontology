"""
Ontology Toolkit

Generate an OWL ontology from the discovered graph schema.
"""

from datetime import date

from rdflib import Graph, Literal
from rdflib.namespace import (
    RDF,
    RDFS,
    OWL,
    XSD,
    SKOS,
    DCTERMS,
)

from ontology_toolkit.vocab import (
    KGO,
    SCHEMA,
    CLASS_ALIGNMENT,
    DATATYPE_MAPPING,
    STANDARD_PREDICATES,
    relationship_to_predicate,
)

from ontology_toolkit.ontology_common import (
    make_label,
    class_comment,
    property_comment,
    bind_namespaces,
    write_metadata,
    collect_property_domains,
    write_classes,
    write_datatype_properties,
)

#
# --------------------------------------------------------------------
# Main Ontology Generation
# --------------------------------------------------------------------
#

def save_ontology(schema, filename="ontology.ttl"):

    graph = Graph()

    #
    # Register namespaces
    #

    bind_namespaces(graph)

    #
    # ----------------------------------------------------------------
    # Ontology metadata
    # ----------------------------------------------------------------
    #

    write_metadata(graph)

    #
    # ----------------------------------------------------------------
    # Collect property usage
    #
    # We use this to determine:
    #
    # 1. Which classes use each property
    # 2. Whether a property should be Functional
    # 3. Whether a domain can safely be emitted
    # ----------------------------------------------------------------
    #

    property_domains = collect_property_domains(schema)

    #
    # ----------------------------------------------------------------
    # Classes
    # ----------------------------------------------------------------
    #

    write_classes(graph, schema)
    
    #
    # ----------------------------------------------------------------
    # Datatype Properties
    # ----------------------------------------------------------------
    #

    write_datatype_properties(
        graph,
        property_domains,
    )

    # ----------------------------------------------------------------
    # Object Properties
    # ----------------------------------------------------------------
    #

    INVERSE_PROPERTIES = {

        "authorOf": "hasAuthor",
        "affiliatedWith": "hasFaculty",
        "investigatorOn": "hasInvestigator",
        "hasLocation": "locationOf",
        "subOrganization": "hasSubOrganization",

    }

    emitted_relationships = set()

    for rel in sorted(
        schema.relationship_types.values(),
        key=lambda r: r.name
    ):

        predicate_name = relationship_to_predicate(
            rel.name
        )

        #
        # Reuse SKOS / OWL predicates
        #

        if predicate_name in STANDARD_PREDICATES:
            continue

        if predicate_name in emitted_relationships:
            continue

        emitted_relationships.add(predicate_name)

        predicate = KGO[predicate_name]

        graph.add((
            predicate,
            RDF.type,
            OWL.ObjectProperty
        ))

        graph.add((
            predicate,
            RDFS.label,
            Literal(make_label(predicate_name))
        ))

        graph.add((
            predicate,
            RDFS.comment,
            Literal(property_comment(predicate_name))
        ))

        #
        # Domain
        #

        if len(rel.source_labels) == 1:

            graph.add((
                predicate,
                RDFS.domain,
                KGO[next(iter(rel.source_labels))]
            ))

        #
        # Range
        #

        if len(rel.target_labels) == 1:

            graph.add((
                predicate,
                RDFS.range,
                KGO[next(iter(rel.target_labels))]
            ))

        #
        # Automatically create inverse properties
        #

        if predicate_name in INVERSE_PROPERTIES:

            inverse_name = INVERSE_PROPERTIES[predicate_name]

            inverse = KGO[inverse_name]

            graph.add((
                inverse,
                RDF.type,
                OWL.ObjectProperty
            ))

            graph.add((
                inverse,
                RDFS.label,
                Literal(make_label(inverse_name))
            ))

            graph.add((
                inverse,
                RDFS.comment,
                Literal(f"Inverse of {predicate_name}.")
            ))

            graph.add((
                inverse,
                OWL.inverseOf,
                predicate
            ))

            graph.add((
                predicate,
                OWL.inverseOf,
                inverse
            ))

    #
    # ----------------------------------------------------------------
    # Serialize
    # ----------------------------------------------------------------
    #

    graph.serialize(
        destination=filename,
        format="turtle"
    )

    return filename

            