from ontology_toolkit.schema_model import (
    GraphSchema,
    NodeType,
    RelationshipType,
)

from ontology_toolkit.property_analysis import analyze_property


def discover_schema(driver):

    schema = GraphSchema()

    with driver.session() as session:

        #
        # ----------------------------------------------------------
        # Discover node labels
        # ----------------------------------------------------------
        #

        result = session.run("""
            MATCH (n)
            RETURN labels(n)[0] AS label,
                   count(*) AS count
            ORDER BY label
        """)

        for record in result:

            schema.node_types[record["label"]] = NodeType(
                label=record["label"],
                count=record["count"]
            )

        #
        # ----------------------------------------------------------
        # Discover node properties
        # ----------------------------------------------------------
        #

        result = session.run("""
            MATCH (n)

            UNWIND labels(n) AS label

            UNWIND keys(n) AS property

            RETURN
                label,
                property,
                collect(n[property]) AS values

            ORDER BY
                label,
                property
        """)

        for record in result:

            label = record["label"]
            prop = record["property"]

            schema.node_types[label].properties[prop] = analyze_property(
                prop,
                record["values"]
            )

        #
        # ----------------------------------------------------------
        # Discover relationship types
        # ----------------------------------------------------------
        #

        result = session.run("""
            MATCH ()-[r]->()

            RETURN
                type(r) AS relationship,
                count(*) AS count

            ORDER BY relationship
        """)

        for record in result:

            schema.relationship_types[record["relationship"]] = RelationshipType(
                name=record["relationship"],
                count=record["count"]
            )

        #
        # ----------------------------------------------------------
        # Discover relationship properties
        # ----------------------------------------------------------
        #

        result = session.run("""
            MATCH ()-[r]->()

            UNWIND keys(r) AS property

            RETURN
                type(r) AS relationship,
                property,
                collect(r[property]) AS values

            ORDER BY
                relationship,
                property
        """)

        for record in result:

            rel = record["relationship"]
            prop = record["property"]

            schema.relationship_types[rel].properties[prop] = analyze_property(
                prop,
                record["values"]
            )

        #
        # ----------------------------------------------------------
        # Discover graph topology
        # ----------------------------------------------------------
        #

        result = session.run("""
            MATCH (a)-[r]->(b)

            RETURN DISTINCT
                labels(a)[0] AS source,
                type(r) AS relationship,
                labels(b)[0] AS target

            ORDER BY relationship, source, target
        """)

        for record in result:

            rel = schema.relationship_types[record["relationship"]]

            source = record["source"]
            target = record["target"]

            rel.source_labels.add(source)
            rel.target_labels.add(target)
            rel.allowed_label_pairs.add((source, target))

    return schema