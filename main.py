from discover import main as discover_main
from validate import main as validate_main

from ontology_toolkit.export_html import export_html


def main():

    print("=" * 60)
    print("Semantic Graph Toolkit")
    print("=" * 60)

    print("\nStep 1: Discovering schema...")
    schema = discover_main()

    print("\nStep 2: Validating graph...")
    semantic_graph = validate_main()

    export_html(schema, semantic_graph)

    print("\nGenerated HTML Report:")
    print("report.html")

    print("\nDone.")


if __name__ == "__main__":
    main()