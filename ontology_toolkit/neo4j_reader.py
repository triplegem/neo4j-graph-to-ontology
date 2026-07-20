"""
Ontology Toolkit

Read instance data from Neo4j into the toolkit's semantic graph model.
"""

from neo4j import Driver

from ontology_toolkit.semantic_model import (
    EntityInstance,
    SemanticGraph,
)
from ontology_toolkit.uri import make_uri


def read_graph(driver: Driver) -> SemanticGraph:
    """
    Read all instance data from Neo4j into a SemanticGraph.
    """

    entities = _read_entities(driver)

    return SemanticGraph(
        entities=entities,
        relationships=[],
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