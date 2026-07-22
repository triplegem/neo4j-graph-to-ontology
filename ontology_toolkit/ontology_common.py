"""
Ontology Toolkit

Shared utilities for ontology generation.
"""


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