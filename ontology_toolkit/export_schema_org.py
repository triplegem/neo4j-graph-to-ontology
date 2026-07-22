"""
export_schema_org.py

Export schema.org JSON-LD documents.
"""

import json
from pathlib import Path

from ontology_toolkit.semantic_model import SemanticGraph
from ontology_toolkit.serializers.schema_org import serialize_person


def export_schema_org(
    graph: SemanticGraph,
    output_dir: str = "schema_org",
) -> None:
    """
    Export schema.org JSON-LD documents.

    Currently exports one Person document per Faculty entity.
    Additional serializers can be registered here in the future.
    """

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    count = 0

    for entity in graph.entities_by_class("Faculty"):

        document = serialize_person(entity, graph)

        filename = (
            entity.properties.get("slug")
            or entity.properties.get("netid")
            or f"person_{count}"
        )

        with (output / f"{filename}.json").open(
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(
                document,
                f,
                indent=2,
                ensure_ascii=False,
            )

        count += 1

    print(f"Exported {count} schema.org document(s).")