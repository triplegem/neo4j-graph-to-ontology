from ontology_toolkit.semantic_model import (
    EntityInstance,
    RelationshipInstance,
    SemanticGraph,
)


faculty = EntityInstance(
    uri="https://example.org/faculty/chris",
    element_id="1",
    class_name="Faculty",
    properties={
        "name": "Chris",
    },
)

publication = EntityInstance(
    uri="https://example.org/publication/1",
    element_id="2",
    class_name="Publication",
    properties={
        "title": "KG Toolkit",
    },
)

relationship = RelationshipInstance(
    element_id="3",
    relationship_type="AUTHOR_OF",
    predicate="authorOf",
    source_uri=faculty.uri,
    target_uri=publication.uri,
    properties={
        "authorOrder": 1,
    },
)

graph = SemanticGraph(
    entities=[faculty, publication],
    relationships=[relationship],
)

print(graph)
print()

print("Entities:")
for entity in graph.entities:
    print(f"  {entity}")

print()

print("Relationships:")
for rel in graph.relationships:
    print(f"  {rel}")

print()

print(f"Entity count: {graph.entity_count}")
print(f"Relationship count: {graph.relationship_count}")
print(f"Total graph elements: {len(graph)}")
print(f"Graph is empty: {graph.is_empty}")

# Verify graph connectivity
assert graph.relationships[0].source_uri == faculty.uri
assert graph.relationships[0].target_uri == publication.uri

print("\n✓ Semantic graph test passed.")