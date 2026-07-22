"""
Ontology Toolkit

Generate an OWL ontology from the discovered graph schema.
"""

from datetime import date
from ontology_toolkit.paths import ONTOLOGY_NARY

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
    write_entity_hierarchy,
    write_datatype_properties,
    write_nary_relationship_model,
)

#
# --------------------------------------------------------------------
# Main Ontology Generation
# --------------------------------------------------------------------
#

def save_ontology(schema, filename=ONTOLOGY_NARY):

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

    write_classes(
        graph,
        schema,
    )

    write_entity_hierarchy(
        graph,
        schema,
    )
    
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
    # Relationship Properties
    # ----------------------------------------------------------------
    #

    write_nary_relationship_model(
        graph,
        schema,
    )
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

            