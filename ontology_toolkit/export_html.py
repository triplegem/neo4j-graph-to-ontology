from pathlib import Path

from ontology_toolkit.report.layout import render_page
from ontology_toolkit.report.overview import render_overview
from ontology_toolkit.report.node_types import render_node_types
from ontology_toolkit.report.relationship_types import (
    render_relationship_types,
)


def export_html(schema, semantic_graph):

    body = ""

    body += render_overview(schema, semantic_graph)
    body += render_node_types(schema)
    body += render_relationship_types(schema)

    html = render_page(
        title="Semantic Graph Report",
        body=body,
    )

    Path("report.html").write_text(
        html,
        encoding="utf-8",
    )