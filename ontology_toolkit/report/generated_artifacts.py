from ontology_toolkit.paths import (
    ONTOLOGY,
    ONTOLOGY_NARY,
    GRAPH,
    GRAPH_JSONLD,
    SHAPES,
    VALIDATION_REPORT,
    SCHEMA_ORG_DIR,
)


def render_generated_artifacts():

    html = '<h2 id="generated-artifacts">Generated Artifacts</h2>'
    html += '<div class="cards">'

    artifacts = [
        (ONTOLOGY, "OWL ontology"),
        (ONTOLOGY_NARY, "N-ary OWL ontology"),
        (GRAPH, "RDF graph"),
        (GRAPH_JSONLD, "JSON-LD export"),
        (SHAPES, "SHACL shapes"),
        (VALIDATION_REPORT, "SHACL validation report"),
        (SCHEMA_ORG_DIR, "schema.org JSON-LD"),
    ]

    for path, description in artifacts:

        exists = path.exists()

        if exists:

            status = "✅ Generated"

            if path.is_file():

                size = path.stat().st_size

                if size < 1024:
                    size_text = f"{size} bytes"
                elif size < 1024 * 1024:
                    size_text = f"{size / 1024:.1f} KB"
                else:
                    size_text = f"{size / (1024 * 1024):.1f} MB"

            else:
                size_text = "Directory"

        else:

            status = "❌ Missing"
            size_text = "—"

        html += f"""
<div class="card">

<h3>{path.name}</h3>

<p>{description}</p>

<p><strong>Status:</strong> {status}</p>

<p><strong>Size:</strong> {size_text}</p>

</div>
"""

    html += "</div>"

    return html