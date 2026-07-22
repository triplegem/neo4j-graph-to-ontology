def render_semantic_graph(semantic_graph):

    return f"""
<h2 id="semantic-graph">Semantic Graph</h2>

<div class="cards">

    <div class="card">
        <div class="label">Entities</div>
        <div class="value">{semantic_graph.entity_count}</div>
    </div>

    <div class="card">
        <div class="label">Relationships</div>
        <div class="value">{semantic_graph.relationship_count}</div>
    </div>

</div>

<p>
The SemanticGraph is a database-independent representation of the
instance data extracted from the property graph. It provides a
stable semantic model that can be serialized into RDF, JSON-LD,
schema.org JSON-LD, and other Semantic Web formats.
</p>
"""