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

    emitted_properties = set()

    for label, node in sorted(schema.node_types.items()):

        for prop in sorted(
            node.properties.values(),
            key=lambda p: p.name
        ):

            #
            # Skip properties already emitted
            #

            if prop.name in emitted_properties:
                continue

            emitted_properties.add(prop.name)

            #
            # Reuse standard vocabularies
            #

            if prop.name in STANDARD_PREDICATES:
                continue

            predicate = KGO[prop.name]

            graph.add((
                predicate,
                RDF.type,
                OWL.DatatypeProperty
            ))

            #
            # Functional property
            #
            # Only if:
            #   - inferred unique
            #   - used by exactly one class
            #

            classes = property_domains[prop.name]["classes"]

            if (
                prop.unique
                and len(classes) == 1
            ):

                graph.add((
                    predicate,
                    RDF.type,
                    OWL.FunctionalProperty
                ))

            #
            # Label
            #

            graph.add((
                predicate,
                RDFS.label,
                Literal(make_label(prop.name))
            ))

            #
            # Comment
            #

            graph.add((
                predicate,
                RDFS.comment,
                Literal(property_comment(prop.name))
            ))

            #
            # Domain
            #
            # IMPORTANT:
            # Only emit when exactly one class owns
            # the property. Otherwise OWL interprets
            # multiple domains as intersection.
            #

            if len(classes) == 1:

                owner = next(iter(classes))

                graph.add((
                    predicate,
                    RDFS.domain,
                    KGO[owner]
                ))

            #
            # Range
            #

            datatype = DATATYPE_MAPPING.get(prop.data_type)

            if datatype is not None:

                graph.add((
                    predicate,
                    RDFS.range,
                    datatype
                ))
        #
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

            