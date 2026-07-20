"""
Ontology Toolkit

Read instance data from Neo4j into the toolkit's semantic graph model.
"""

from neo4j import Driver

from ontology_toolkit.semantic_model import (
    EntityInstance,
    RelationshipInstance,
    SemanticGraph,
)
from ontology_toolkit.uri import make_uri
from ontology_toolkit.vocab import relationship_to_predicate


def read_graph(driver: Driver) -> SemanticGraph:
    """
    Read all instance data from Neo4j into a SemanticGraph.
    """

    entities = _read_entities(driver)
    relationships = _read_relationships(driver, entities)

    return SemanticGraph(
        entities=entities,
        relationships=relationships,
    )


def _read_entities(driver: Driver) -> list[EntityInstance]:
    """
    Read all nodes from Neo4j.
    """

    entities = []

    with driver.session() as session:

        result = session.run("""
            MATCH (n)

            RETURN
                elementId(n) AS id,
                labels(n)[0] AS label,
                properties(n) AS props
        """)

        for record in result:

            class_name = record["label"]
            properties = record["props"]

            entity = EntityInstance(
                uri=make_uri(class_name, properties),
                element_id=record["id"],
                class_name=class_name,
                properties=properties,
            )

            entities.append(entity)

    return entities


def _read_relationships(
    driver: Driver,
    entities: list[EntityInstance],
) -> list[RelationshipInstance]:
    """
    Read all relationships from Neo4j.
    """

    uri_map = {
        entity.element_id: entity.uri
        for entity in entities
    }

    relationships = []

    with driver.session() as session:

        result = session.run("""
            MATCH (a)-[r]->(b)

            RETURN
                elementId(r) AS id,
                elementId(a) AS source,
                type(r) AS rel,
                elementId(b) AS target,
                properties(r) AS props
        """)

        for record in result:

            relationship = RelationshipInstance(
                element_id=record["id"],
                relationship_type=record["rel"],
                predicate=relationship_to_predicate(
                    record["rel"]
                ),
                source_uri=uri_map[record["source"]],
                target_uri=uri_map[record["target"]],
                properties=record["props"],
            )

            relationships.append(relationship)

    return relationships