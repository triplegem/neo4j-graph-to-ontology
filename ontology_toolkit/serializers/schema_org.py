"""
schema_org.py

Schema.org serializers built on top of the SemanticGraph model.
"""

from typing import Optional

from ..semantic_model import (
    EntityInstance,
    RelationshipInstance,
    SemanticGraph,
)


# ----------------------------------------------------------------------
# Graph helpers
# ----------------------------------------------------------------------

def _get_entity(
    graph: SemanticGraph,
    uri: str,
) -> Optional[EntityInstance]:
    """
    Return an entity by URI.
    """
    for entity in graph.entities:
        if entity.uri == uri:
            return entity
    return None


def _outgoing(
    graph: SemanticGraph,
    source_uri: str,
    relationship_type: str,
) -> list[RelationshipInstance]:
    """
    Return outgoing relationships of a given Neo4j relationship type.
    """
    return [
        rel
        for rel in graph.relationships
        if rel.source_uri == source_uri
        and rel.relationship_type == relationship_type
    ]


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
        "@id": f"{profile_url}#person" if profile_url else person.uri,
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

    for rel in _outgoing(graph, person.uri, "WORKS_FOR"):

        university = _get_entity(graph, rel.target_uri)

        if university:

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

    for rel in _outgoing(graph, person.uri, "AFFILIATED_WITH"):

        department = _get_entity(graph, rel.target_uri)

        if department:

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

    for rel in _outgoing(graph, person.uri, "KNOWS_ABOUT"):

        concept = _get_entity(graph, rel.target_uri)

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

    for rel in _outgoing(graph, person.uri, "SAME_AS"):

        identifier = _get_entity(graph, rel.target_uri)

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