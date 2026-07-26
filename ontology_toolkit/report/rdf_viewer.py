from pathlib import Path
from html import escape


def render_rdf_file(filename, title):
    """
    Render an RDF/Turtle file as a formatted code block.
    """

    path = Path(filename)

    section_id = (
        path.stem
        .replace("_", "-")
        .replace(".", "-")
    )

    if not path.exists():
        return f"""
<h3 id="{section_id}">{title}</h3>

<div class="card">
<p><strong>{path.name}</strong> was not found.</p>
</div>
"""

    rdf = path.read_text(encoding="utf-8")

    return f"""
<h3 id="{section_id}">{title}</h3>

<div class="card">

<p><strong>{path.name}</strong></p>

<pre class="rdf-viewer"><code>{escape(rdf)}</code></pre>

</div>
"""