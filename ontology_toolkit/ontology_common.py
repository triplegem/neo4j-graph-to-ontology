"""
Ontology Toolkit

Shared utilities for ontology generation.
"""

from datetime import date
from rdflib import Literal, URIRef

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

def make_label(name: str) -> str:
    """
    Convert camelCase into a human-readable label.

    authorOf -> author of
    knowsAbout -> knows about
    hasLocation -> has location
    """

    label = ""

    for i, ch in enumerate(name):

        if i > 0 and ch.isupper():
            label += " "

        label += ch.lower()

    return label


def class_comment(label: str) -> str:
    """
    Generate documentation for ontology classes.
    """

    comments = {

        "Faculty":
            "A faculty member within the College of Engineering.",

        "Department":
            "An academic department within the university.",

        "College":
            "An academic college.",

        "University":
            "A university.",

        "Campus":
            "A physical campus location.",

        "Publication":
            "A scholarly publication.",

        "Grant":
            "A sponsored research award.",

        "Concept":
            "A research topic or area of expertise.",

        "ConceptScheme":
            "A controlled vocabulary of research concepts.",

        "ORCID":
            "An ORCID identifier resource.",

        "Wikidata":
            "A Wikidata entity.",
    }

    return comments.get(
        label,
        f"Ontology class representing {label.lower()}."
    )


def property_comment(name: str) -> str:
    """
    Generate documentation for ontology properties.
    """

    comments = {

        "authorOf":
            "Relates a faculty member to a publication.",

        "knowsAbout":
            "Relates a faculty member to an area of expertise.",

        "affiliatedWith":
            "Relates a faculty member to an academic department.",

        "investigatorOn":
            "Relates a faculty member to a research grant.",

        "about":
            "Associates a publication or grant with a research topic.",

        "hasLocation":
            "Associates an entity with a campus.",

        "subOrganization":
            "Relates an organization to one of its sub-organizations.",

        "name":
            "Human-readable name of the resource.",

        "identifier":
            "Unique identifier for the resource.",

        "title":
            "Title of the resource.",

        "uri":
            "Canonical URI identifying the resource.",
    }

    return comments.get(
        name,
        f"Ontology property '{make_label(name)}'."
    )

def bind_namespaces(graph):
    """
    Register namespaces used throughout the ontology.
    """

    graph.bind("kgo", KGO)
    graph.bind("schema", SCHEMA)
    graph.bind("rdf", RDF)
    graph.bind("rdfs", RDFS)
    graph.bind("owl", OWL)
    graph.bind("xsd", XSD)
    graph.bind("skos", SKOS)
    graph.bind("dcterms", DCTERMS)

def write_metadata(graph):
    """
    Write ontology metadata.
    """

    ontology = KGO[""]

    graph.add((ontology, RDF.type, OWL.Ontology))

    graph.add((
        ontology,
        RDFS.label,
        Literal("Cornell Engineering Faculty Expertise Ontology")
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
        DCTERMS.creator,
        Literal("Chris Lastovicka")
    ))

    graph.add((
        ontology,
        DCTERMS.created,
        Literal(str(date.today()), datatype=XSD.date)
    ))

    graph.add((
        ontology,
        DCTERMS.title,
        Literal("Faculty Expertise Ontology")
    ))

    graph.add((
        ontology,
        OWL.versionInfo,
        Literal("1.0")
    ))

def collect_property_domains(schema):
    """
    Collect property usage information.

    We use this to determine:

    1. Which classes use each property
    2. Whether a property should be Functional
    3. Whether a domain can safely be emitted
    """

    property_domains = {}

    for label, node in schema.node_types.items():

        for prop in node.properties.values():

            property_domains.setdefault(
                prop.name,
                {
                    "classes": set(),
                    "properties": []
                }
            )

            property_domains[prop.name]["classes"].add(label)
            property_domains[prop.name]["properties"].append(prop)

    return property_domains

def write_classes(graph, schema):
    """
    Write OWL classes for each node label.
    """

    for label in sorted(schema.node_types):

        cls = KGO[label]

        graph.add((cls, RDF.type, OWL.Class))
        graph.add((cls, RDFS.label, Literal(label)))
        graph.add((cls, RDFS.comment, Literal(class_comment(label))))

        if label in CLASS_ALIGNMENT:
            graph.add((
                cls,
                RDFS.subClassOf,
                URIRef(CLASS_ALIGNMENT[label])
            ))

def write_datatype_properties(
    graph,
    property_domains,
):
    """
    Write OWL datatype properties.
    """

    for prop_name in sorted(property_domains):

        #
        # Reuse standard vocabularies
        #

        if prop_name in STANDARD_PREDICATES:
            continue

        predicate = KGO[prop_name]

        graph.add((
            predicate,
            RDF.type,
            OWL.DatatypeProperty
        ))

        classes = property_domains[prop_name]["classes"]

        #
        # Functional property
        #

        prop = property_domains[prop_name]["properties"][0]

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
            Literal(make_label(prop_name))
        ))

        #
        # Comment
        #

        graph.add((
            predicate,
            RDFS.comment,
            Literal(property_comment(prop_name))
        ))

        #
        # Domain
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

def write_object_properties(
    graph,
    schema,
):
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

def write_nary_relationship_model(
    graph,
    schema,
):
    """
    Write the relationship model for the n-ary ontology.
    """

    #
    # Base entity class
    #

    graph.add((
        KGO.Entity,
        RDF.type,
        OWL.Class,
    ))

    graph.add((
        KGO.Entity,
        RDFS.label,
        Literal("Entity"),
    ))

    graph.add((
        KGO.Entity,
        RDFS.comment,
        Literal(
            "Base class for entity instances in the knowledge graph."
        ),
    ))

    #
    # Base relationship class
    #

    graph.add((
        KGO.Relationship,
        RDF.type,
        OWL.Class,
    ))

    graph.add((
        KGO.Relationship,
        RDFS.label,
        Literal("Relationship"),
    ))

    graph.add((
        KGO.Relationship,
        RDFS.comment,
        Literal(
            "Base class for relationship instances in the n-ary ontology."
        ),
    ))

    #
    # Relationship subclasses
    #

    for relationship_type in schema.relationship_types:

        class_name = relationship_type.title().replace("_", "") + "Relationship"

        relationship_class = KGO[class_name]

        graph.add((
            relationship_class,
            RDF.type,
            OWL.Class,
        ))

        graph.add((
            relationship_class,
            RDFS.subClassOf,
            KGO.Relationship,
        ))

        graph.add((
            relationship_class,
            RDFS.label,
            Literal(make_label(class_name)),
        ))

        graph.add((
            relationship_class,
            RDFS.comment,
            Literal(
                f"Represents a {relationship_type} relationship."
            ),
        ))

    #
    # Shared relationship properties
    #

    graph.add((
        KGO.source,
        RDF.type,
        OWL.ObjectProperty,
    ))

    graph.add((
        KGO.source,
        RDFS.label,
        Literal("source"),
    ))

    graph.add((
        KGO.source,
        RDFS.comment,
        Literal(
            "The source entity of a relationship."
        ),
    ))

    graph.add((
        KGO.source,
        RDFS.domain,
        KGO.Relationship,
    ))

    graph.add((
        KGO.source,
        RDFS.range,
        KGO.Entity,
    ))

    graph.add((
        KGO.target,
        RDF.type,
        OWL.ObjectProperty,
    ))

    graph.add((
        KGO.target,
        RDFS.label,
        Literal("target"),
    ))

    graph.add((
        KGO.target,
        RDFS.comment,
        Literal(
            "The target entity of a relationship."
        ),
    ))

    graph.add((
        KGO.target,
        RDFS.domain,
        KGO.Relationship,
    ))

    graph.add((
        KGO.target,
        RDFS.range,
        KGO.Entity,
    ))

def write_entity_hierarchy(
    graph,
    schema,
):
    """
    Make every node class a subclass of kgo:Entity.
    """

    for label in sorted(schema.node_types):

        graph.add((
            KGO[label],
            RDFS.subClassOf,
            KGO.Entity,
        ))

def write_entity_hierarchy(
    graph,
    schema,
):
    """
    Make every node class a subclass of kgo:Entity.
    """

    for label in sorted(schema.node_types):

        graph.add((
            KGO[label],
            RDFS.subClassOf,
            KGO.Entity,
        ))