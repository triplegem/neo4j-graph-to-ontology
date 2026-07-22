def render_pipeline():

    return """
<h2 id="pipeline">Semantic Pipeline</h2>

<div class="card">

<p>
This toolkit transforms a Neo4j property graph into a
database-independent semantic graph model that serves as the
foundation for multiple Semantic Web serializations.
</p>

<pre>

Neo4j Property Graph
        │
        ▼
Schema Discovery
        │
        ▼
GraphSchema
        │
        ▼
SemanticGraph
        │
        ├── ontology.ttl
        ├── ontology_nary.ttl
        ├── graph.ttl
        ├── graph.jsonld
        ├── schema.org JSON-LD
        ├── shapes.ttl
        └── validation_report.txt

</pre>

</div>
"""