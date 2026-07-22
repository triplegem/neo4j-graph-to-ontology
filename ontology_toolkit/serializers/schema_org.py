"""
schema_org.py

Schema.org serializers built on top of the SemanticGraph model.
"""

from ..semantic_model import (
    EntityInstance,
    SemanticGraph,
)


# ----------------------------------------------------------------------
# Person serializer
# ----------------------------------------------------------------------

def serialize_person(
    person: EntityInstance,
    graph: SemanticGraph,
) -> dict:
    """
    Serialize a Faculty entity as a schema.org Person.

    Optional properties are omitted when no data exists.
    """

    profile_url = person.properties.get("url")

    data = {
        "@context": "https://schema.org",
        "@type": "Person",
        "@id": (
            f"{profile_url}#person"
            if profile_url
            else person.uri
        ),
        "name": person.properties.get("name"),
    }

    if profile_url:
        data["url"] = profile_url

    # --------------------------------------------------
    # Simple properties
    # --------------------------------------------------

    if person.properties.get("jobTitle"):
        data["jobTitle"] = person.properties["jobTitle"]

    if person.properties.get("description"):
        data["description"] = person.properties["description"]

    # --------------------------------------------------
    # worksFor
    # --------------------------------------------------

    for relationship in graph.outgoing(person.uri, "WORKS_FOR"):

        university = graph.get_entity(relationship.target_uri)

        if not university:
            continue

        works_for = {
            "@type": "CollegeOrUniversity",
            "name": university.properties.get("name"),
        }

        if university.properties.get("url"):
            works_for["@id"] = university.properties["url"]

        data["worksFor"] = works_for
        break

    # --------------------------------------------------
    # affiliation
    # --------------------------------------------------

    affiliations = []

    for relationship in graph.outgoing(
        person.uri,
        "AFFILIATED_WITH",
    ):

        department = graph.get_entity(
            relationship.target_uri
        )

        if not department:
            continue

        affiliation = {
            "@type": "CollegeOrUniversity",
            "name": department.properties.get("name"),
        }

        if department.properties.get("url"):
            affiliation["@id"] = department.properties["url"]

        affiliations.append(affiliation)

    if affiliations:
        data["affiliation"] = (
            affiliations[0]
            if len(affiliations) == 1
            else affiliations
        )

    # --------------------------------------------------
    # knowsAbout
    # --------------------------------------------------

    knows_about = []

    for relationship in graph.outgoing(
        person.uri,
        "KNOWS_ABOUT",
    ):

        concept = graph.get_entity(
            relationship.target_uri
        )

        if not concept:
            continue

        label = (
            concept.properties.get("prefLabel")
            or concept.properties.get("name")
            or concept.properties.get("label")
            or concept.properties.get("identifier")
        )

        if label:
            knows_about.append(label)

    if knows_about:
        data["knowsAbout"] = sorted(set(knows_about))

    # --------------------------------------------------
    # sameAs
    # --------------------------------------------------

    same_as = []

    for relationship in graph.outgoing(
        person.uri,
        "SAME_AS",
    ):

        identifier = graph.get_entity(
            relationship.target_uri
        )

        if not identifier:
            continue

        uri = (
            identifier.properties.get("uri")
            or identifier.properties.get("url")
            or identifier.properties.get("identifier")
        )

        if uri:
            same_as.append(uri)

    if same_as:
        data["sameAs"] = sorted(set(same_as))

    return data