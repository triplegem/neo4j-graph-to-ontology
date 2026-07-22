"""
Ontology Toolkit

Shared ontology vocabulary definitions.
"""

from rdflib import Namespace
from rdflib.namespace import RDF, RDFS, OWL, SKOS, XSD

#
# Namespaces
#

KGO = Namespace("https://kg.engineering.cornell.edu/ontology#")
KGR = Namespace("https://kg.engineering.cornell.edu/resource/")
SCHEMA = Namespace("https://schema.org/")

#
# Align local classes with well-known vocabularies
#

CLASS_ALIGNMENT = {
    "Faculty": SCHEMA.Person,
    "Publication": SCHEMA.ScholarlyArticle,
    "Department": SCHEMA.Organization,
    "College": SCHEMA.CollegeOrUniversity,
    "University": SCHEMA.CollegeOrUniversity,
    "Campus": SCHEMA.Place,
    "Concept": SKOS.Concept,
    "ConceptScheme": SKOS.ConceptScheme,
}

#
# Reuse standard predicates
#

STANDARD_PREDICATES = {

    # SKOS
    "prefLabel": SKOS.prefLabel,
    "broader": SKOS.broader,
    "inScheme": SKOS.inScheme,
    "exactMatch": SKOS.exactMatch,

    # OWL
    "sameAs": OWL.sameAs,
}

#
# Datatype mapping
#

DATATYPE_MAPPING = {

    "string": XSD.string,
    "integer": XSD.integer,
    "float": XSD.decimal,
    "boolean": XSD.boolean,
    "date": XSD.date,
    "uri": XSD.anyURI,

    #
    # Custom inferred types
    #

    "email": XSD.string,
    "doi": XSD.string,
    "orcid": XSD.string,
    "wikidata_identifier": XSD.string,
}


def relationship_to_predicate(name: str) -> str:
    """
    Convert Neo4j relationship names to RDF-style camelCase.

    AUTHOR_OF -> authorOf
    SAME_AS -> sameAs
    """

    words = name.lower().split("_")

    return words[0] + "".join(
        word.capitalize()
        for word in words[1:]
    )


def relationship_to_class(name: str) -> str:
    """
    Convert Neo4j relationship names to ontology relationship classes.

    AUTHOR_OF -> AuthorOfRelationship
    SAME_AS -> SameAsRelationship
    """

    words = name.lower().split("_")

    return "".join(
        word.capitalize()
        for word in words
    ) + "Relationship"