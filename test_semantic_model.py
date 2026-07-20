from ontology_toolkit.semantic_model import (
    EntityInstance,
    RelationshipInstance,
    SemanticGraph,
)


faculty = EntityInstance(
    uri="https://example.org/faculty/chris",
    element_id="4:123",
    label="Faculty",
    properties={
        "name": "Chris Lastovicka",
        "orcid": "0000-0000-0000-0000",
    },
)

publication = EntityInstance(
    uri="https://example.org/publication/123",
    element_id="4:456",
    label="Publication",
    properties={
        "title": "Knowledge Graphs in Higher Education",
        "year": 2026,
    },
)

relationship = RelationshipInstance(
    element_id="5:789",
    relationship_type="AUTHOR_OF",
    predicate_name="authorOf",
    source_uri=faculty.uri,
    target_uri=publication.uri,
    properties={
        "authorOrder": 1,
        "corresponding": True,
    },
)

graph = SemanticGraph()

graph.entities.append(faculty)
graph.entities.append(publication)
graph.relationships.append(relationship)

print(graph)

print(f"Entities: {graph.entity_count}")
print(f"Relationships: {graph.relationship_count}")
print(f"Total graph elements: {len(graph)}")