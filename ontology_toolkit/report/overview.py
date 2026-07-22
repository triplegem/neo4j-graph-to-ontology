def render_overview(schema, semantic_graph):

    return f"""
<h2 id="overview">Overview</h2>

<div class="cards">

    <div class="card">
        <div class="label">Node Types</div>
        <div class="value">{len(schema.node_types)}</div>
    </div>

    <div class="card">
        <div class="label">Relationship Types</div>
        <div class="value">{len(schema.relationship_types)}</div>
    </div>

    <div class="card">
        <div class="label">Entities</div>
        <div class="value">{semantic_graph.entity_count}</div>
    </div>

    <div class="card">
        <div class="label">Relationships</div>
        <div class="value">{semantic_graph.relationship_count}</div>
    </div>

</div>
"""