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