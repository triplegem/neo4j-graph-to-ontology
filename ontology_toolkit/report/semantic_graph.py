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

<div class="report-text">
<p>
The Semantic Graph Toolkit discovers the schema of a Neo4j property graph and generates Semantic Web artifacts including OWL ontologies, RDF graphs, JSON-LD, schema.org JSON-LD, SHACL shapes, validation reports, provenance-aware RDF, and OWL RL inferred knowledge graphs.
</p>
</div>
"""