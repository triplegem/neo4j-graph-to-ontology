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


#
# --------------------------------------------------------------------
# Helper Functions
# --------------------------------------------------------------------
#

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

    graph.bind("kgo", KGO)
    graph.bind("schema", SCHEMA)
    graph.bind("rdf", RDF)
    graph.bind("rdfs", RDFS)
    graph.bind("owl", OWL)
    graph.bind("xsd", XSD)
    graph.bind("skos", SKOS)
    graph.bind("dcterms", DCTERMS)

    #
    # ----------------------------------------------------------------
    # Ontology metadata
    # ----------------------------------------------------------------
    #

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

    #
    # ----------------------------------------------------------------
    # Classes
    # ----------------------------------------------------------------
    #

    for label, node in sorted(schema.node_types.items()):

        cls = KGO[label]

        graph.add((
            cls,
            RDF.type,
            OWL.Class
        ))

        graph.add((
            cls,
            RDFS.label,
            Literal(label)
        ))

        graph.add((
            cls,
            RDFS.comment,
            Literal(class_comment(label))
        ))

        #
        # Align with standard vocabularies
        #

        if label in CLASS_ALIGNMENT:

            graph.add((
                cls,
                RDFS.subClassOf,
                CLASS_ALIGNMENT[label]
            ))
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

            