from ontology_toolkit.paths import (
    REPORT,
    ONTOLOGY,
    ONTOLOGY_NARY,
    GRAPH,
)

from ontology_toolkit.report.layout import render_page
from ontology_toolkit.report.overview import render_overview
from ontology_toolkit.report.node_types import render_node_types
from ontology_toolkit.report.relationship_types import (
    render_relationship_types,
)
from ontology_toolkit.report.generated_artifacts import (
    render_generated_artifacts,
)
from ontology_toolkit.report.pipeline import render_pipeline
from ontology_toolkit.report.semantic_graph import render_semantic_graph
from ontology_toolkit.report.table_of_contents import (
    render_table_of_contents,
)
from ontology_toolkit.report.schema_summary import render_schema_summary
from ontology_toolkit.report.rdf_viewer import render_rdf_file


def export_html(schema, semantic_graph):

    body = ""

    body += render_table_of_contents()
    body += render_overview(schema, semantic_graph)
    body += render_schema_summary(schema)
    body += render_pipeline()
    body += render_node_types(schema)
    body += render_relationship_types(schema)
    body += render_generated_artifacts()

    body += render_rdf_file(
        ONTOLOGY,
        "OWL Ontology",
    )

    body += render_rdf_file(
        GRAPH,
        "RDF Graph",
    )

    body += render_rdf_file(
        ONTOLOGY_NARY,
        "N-ary Ontology",
    )

    html = render_page(
        title="Semantic Graph Report",
        body=body,
    )

    REPORT.write_text(
        html,
        encoding="utf-8",
    )