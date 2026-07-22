from pathlib import Path
from html import escape


def render_rdf_file(filename, title):
    """
    Render an RDF/Turtle file as a formatted code block.
    """

    path = Path(filename)

    if not path.exists():
        return f"""
<p id="viewers"></p>
<h2>{title}</h2>

<div class="card">
<p><strong>{path.name}</strong> was not found.</p>
</div>
"""

    rdf = path.read_text(encoding="utf-8")

    return f"""
<p id="viewers"></p>
<h2>{title}</h2>

<div class="card">

<p><strong>{path.name}</strong></p>

<pre class="rdf-viewer"><code>{escape(rdf)}</code></pre>

</div>
"""