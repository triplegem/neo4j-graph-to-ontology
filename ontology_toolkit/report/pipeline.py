def render_pipeline():

    return """
<h2 id="pipeline">Semantic Pipeline</h2>

<div class="card">

<div class="report-text">
<p>
This toolkit transforms a Neo4j property graph into a
database-independent semantic graph model that serves as the
foundation for multiple Semantic Web serializations. Generated
RDF can be enriched with provenance metadata and OWL RL reasoning
to produce inferred knowledge while preserving traceability to
the original property graph.
</p>
</div>

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
        ├── graph_nary.ttl
        ├── graph.jsonld
        ├── schema.org JSON-LD
        ├── shapes.ttl
        └── validation_report.txt
        │
        ▼
RDF Export with Provenance
        │
        ▼
OWL RL Reasoning
        │
        ▼
graph_inferred.ttl
        │
        ▼
Inference Cleanup
        │
        ▼
graph_inferred_clean.ttl

</pre>

</div>
"""