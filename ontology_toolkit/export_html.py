from datetime import datetime, UTC

from ontology_toolkit.paths import (
    REPORT,
    ONTOLOGY,
    ONTOLOGY_NARY,
    GRAPH,
    GRAPH_NARY,
    GRAPH_INFERRED,
    GRAPH_INFERRED_CLEAN,
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

    generated = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")

    body = f"""
<p><strong>Generated:</strong> {generated}</p>
"""

    body += render_table_of_contents()
    body += render_overview(schema, semantic_graph)
    body += render_schema_summary(schema)
    body += render_pipeline()
    body += render_node_types(schema)
    body += render_relationship_types(schema)
    body += render_generated_artifacts()

    #
    # RDF / OWL Viewers
    #

    body += """
<p id="viewers"></p>

<h2>Viewers</h2>

<div class="viewer-layout">

    <aside class="viewer-nav">

        <a href="#ontology">OWL Ontology</a>

        <a href="#ontology-nary">N-ary OWL</a>

        <a href="#graph">Binary RDF</a>

        <a href="#graph-nary">N-ary RDF</a>

        <a href="#graph-inferred">Inferred RDF</a>

        <a href="#graph-inferred-clean">Cleaned Inferred RDF</a>

    </aside>

    <div class="viewer-content">
"""

    body += render_rdf_file(
        ONTOLOGY,
        "OWL Ontology",
    )

    body += render_rdf_file(
        ONTOLOGY_NARY,
        "N-ary OWL Ontology",
    )

    body += render_rdf_file(
        GRAPH,
        "Binary RDF Graph",
    )

    body += render_rdf_file(
        GRAPH_NARY,
        "N-ary RDF Graph",
    )

    body += render_rdf_file(
        GRAPH_INFERRED,
        "OWL RL Inferred RDF Graph",
    )

    body += render_rdf_file(
        GRAPH_INFERRED_CLEAN,
        "Cleaned Inferred RDF Graph",
    )

    body += """
    </div>

</div>
"""

    html = render_page(
        title="Report: Neo4j to Ontology",
        body=body,
    )

    REPORT.write_text(
        html,
        encoding="utf-8",
    )