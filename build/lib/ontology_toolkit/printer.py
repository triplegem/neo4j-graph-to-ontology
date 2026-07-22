from ontology_toolkit.schema_model import GraphSchema


def print_schema(schema: GraphSchema):

    print("\n" + "=" * 60)
    print("GRAPH SCHEMA")
    print("=" * 60)

    #
    # ----------------------------------------------------------
    # Nodes
    # ----------------------------------------------------------
    #

    print("\nNODE TYPES\n")

    for label in sorted(schema.node_types):

        node = schema.node_types[label]

        print(f"{node.label} ({node.count})")

        if node.properties:

            print("  Properties:")

            for property_name in sorted(node.properties):

                prop = node.properties[property_name]

                print(
                    f"    • {prop.name:<20} "
                    f"type={prop.data_type}"
                )

        print()

    #
    # ----------------------------------------------------------
    # Relationships
    # ----------------------------------------------------------
    #

    print("\nRELATIONSHIP TYPES\n")

    for relationship_name in sorted(schema.relationship_types):

        rel = schema.relationship_types[relationship_name]

        print(f"{rel.name} ({rel.count})")

        print(
            f"  Source: {', '.join(sorted(rel.source_labels))}"
        )

        print(
            f"  Target: {', '.join(sorted(rel.target_labels))}"
        )

        if rel.properties:

            print("  Properties:")

            for property_name in sorted(rel.properties):

                prop = rel.properties[property_name]

                print(
                    f"    • {prop.name:<20} "
                    f"type={prop.data_type}"
                )

        print()