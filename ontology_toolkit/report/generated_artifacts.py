from pathlib import Path


def render_generated_artifacts():

    html = "<h2 id=\"generated-artifacts\">Generated Artifacts</h2>"
    html += '<div class="cards">'

    artifacts = [
        ("ontology.ttl", "OWL ontology"),
        ("ontology_nary.ttl", "N-ary OWL ontology"),
        ("graph.ttl", "RDF graph"),
        ("graph.jsonld", "JSON-LD export"),
        ("shapes.ttl", "SHACL shapes"),
        ("validation_report.txt", "SHACL validation report"),
        ("schema_org/", "schema.org JSON-LD"),
    ]

    for filename, description in artifacts:

        path = Path(filename)

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

<h3>{filename}</h3>

<p>{description}</p>

<p><strong>Status:</strong> {status}</p>

<p><strong>Size:</strong> {size_text}</p>

</div>
"""

    html += "</div>"

    return html