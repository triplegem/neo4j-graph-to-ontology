# Semantic Graph Toolkit

A Python toolkit for discovering the schema of a Neo4j property graph and transforming it into reusable Semantic Web artifacts.

The Semantic Graph Toolkit bridges labeled property graphs (LPGs) and Semantic Web technologies through a database-independent semantic graph model that separates graph extraction from serialization and downstream processing. This architecture enables multiple exporters, validators, reasoning pipelines, and reporting tools to operate on a shared semantic representation.

The toolkit currently supports schema discovery, OWL ontology generation, RDF and JSON-LD serialization, SHACL shape generation and validation, PROV-O provenance generation, OWL RL reasoning, inference cleanup, and interactive HTML reporting.

---

# Overview

Rather than serializing directly from Neo4j, the toolkit first loads graph data into a reusable `SemanticGraph` object model. This architectural separation allows semantic processing components to operate independently of the underlying database while sharing a common representation of the graph.

Current capabilities include:

- Discovering graph schema from Neo4j
- Analyzing node and relationship properties
- Discovering semantic graph topology (source → target label pairs)
- Building a reusable semantic graph model
- Generating binary OWL ontologies
- Generating n-ary OWL ontologies
- Exporting graph instances as binary RDF/Turtle
- Exporting graph instances as n-ary RDF/Turtle
- Exporting generic JSON-LD
- Exporting schema.org JSON-LD
- Generating SHACL validation shapes
- Validating RDF with pySHACL
- Generating PROV-O provenance
- Applying OWL RL reasoning
- Producing cleaned inferred RDF graphs
- Generating interactive HTML reports with embedded RDF viewers

Because every downstream component operates on the shared `SemanticGraph` model, new serializers, validators, reasoning engines, and graph-processing pipelines can be added without changing the Neo4j extraction layer.

---

# Workflow

The toolkit provides three primary entry points.

## `discover.py`

Discovers the semantic schema from Neo4j and generates the project's semantic contract.

Outputs:

- `ontology.ttl`
- `ontology_nary.ttl`
- `shapes.ttl`

This workflow should be run whenever the graph schema changes or the ontology definitions are intentionally updated.

---

## `validate.py`

Reads graph instance data into the `SemanticGraph` model and executes the semantic processing pipeline.

Outputs:

- `graph.ttl`
- `graph_nary.ttl`
- `graph.jsonld`
- `schema_org/*.json`
- `provenance.ttl`
- `graph_inferred.ttl`
- `graph_inferred_clean.ttl`
- `validation_report.txt`
- `report.html`

Unlike discovery, this workflow does **not** regenerate the ontology or SHACL shapes. Instead, it validates graph instances against the previously established semantic contract, generates provenance, materializes inferred triples using OWL RL reasoning, cleans the inferred graph for readability, and produces an interactive HTML report summarizing the results.

---

## `main.py`

A convenience workflow that executes the complete semantic processing pipeline.

```text
Discover schema
        ↓
Generate ontology.ttl
Generate ontology_nary.ttl
Generate shapes.ttl
        ↓
Read graph
        ↓
Build SemanticGraph
        ↓
Export RDF / RDF (n-ary) / JSON-LD / schema.org
        ↓
Generate PROV-O provenance
        ↓
Validate with SHACL
        ↓
Apply OWL RL reasoning
        ↓
Clean inferred graph
        ↓
Generate HTML report
```

This workflow is useful during development because it regenerates every semantic artifact from a single command. In production workflows, discovery and validation can be executed independently as needed.

---

# Design Principles

The Semantic Graph Toolkit is organized around four independent architectural layers:

1. **Schema discovery** – learns the semantic structure of a Neo4j property graph.
2. **Semantic graph representation** – provides a reusable, database-independent model of graph instances.
3. **Semantic processing** – generates ontologies, semantic serializations, validation artifacts, provenance, reasoning results, and reports.
4. **Workflow orchestration** – coordinates discovery, validation, and reporting pipelines.

By separating these concerns, serialization formats, ontology profiles, validators, reasoning engines, and future graph-processing components can evolve independently while sharing the same semantic graph representation.

---

# Current Capabilities

## Schema Discovery

Automatically discovers the semantic structure of a Neo4j property graph, including:

- Node labels
- Relationship types
- Node properties
- Relationship properties
- Relationship topology (source → target label pairs)
- Property datatypes
- Required and optional properties
- Identifier candidates
- Enumerated values
- Example values

Relationship topology is preserved within the discovered schema, allowing ontology generation and SHACL validation to accurately model valid source-to-target relationships without producing invalid combinations.

Relationship properties are also preserved for downstream serializers and semantic processing components.

---

## Semantic Graph Model

The toolkit introduces a reusable semantic representation of graph instance data through:

- `EntityInstance`
- `RelationshipInstance`
- `SemanticGraph`

This layer decouples Neo4j data extraction from every downstream component. Ontology generation, RDF serialization, JSON-LD export, SHACL validation, provenance generation, reasoning, and reporting all operate on the same shared semantic graph.

---

## OWL Ontology Generation

The toolkit generates two complementary ontology variants from the discovered schema.

### Binary Ontology (`ontology.ttl`)

Represents graph relationships as OWL object properties.

Generates:

- OWL classes
- Object properties
- Datatype properties
- Domains
- Ranges
- Dublin Core metadata
- Ontology profile alignments
- SKOS concept relationships

### N-ary Ontology (`ontology_nary.ttl`)

Represents relationships as first-class semantic resources.

Generates:

- `Entity` base class
- `Relationship` base class
- Relationship subclasses
- Shared `source` and `target` object properties
- Datatype properties
- Dublin Core metadata

The n-ary ontology mirrors the toolkit's semantic graph model, enabling relationship metadata to be represented directly while providing a foundation for richer semantic modeling.

### Ontology Profiles

Ontology profiles separate the toolkit's internal semantic model from external vocabularies, allowing the same semantic graph to align with multiple ontology ecosystems without modifying the core model.

Current profiles include:

- **Schema.org**
- **VIVO**

Additional profiles can be added independently to support other vocabularies and domain ontologies.

---

## RDF and JSON-LD Serialization

Graph instances can be serialized into multiple Semantic Web formats from the shared `SemanticGraph` model.

Current serializers include:

- Binary RDF/Turtle
- N-ary RDF/Turtle
- Generic JSON-LD

Resources receive stable URIs derived from identifier properties whenever available.

Generated RDF incorporates vocabulary from:

- RDF
- RDFS
- OWL
- SKOS
- Schema.org
- VIVO
- Dublin Core

The binary serializer represents relationships as RDF object properties, while the n-ary serializer models relationships as first-class resources, preserving relationship metadata and supporting richer semantic representations.

Because serialization operates on the shared semantic graph, additional RDF vocabularies can be incorporated through ontology profiles without changing the serialization architecture.

---

## Schema.org JSON-LD Export

The toolkit generates web-oriented schema.org JSON-LD from the same `SemanticGraph` model used for RDF serialization.

Current support includes:

- `Person`
- `affiliation`
- `knowsAbout`
- `sameAs`

The exporter generates one schema.org JSON-LD document per supported entity.

Because serialization is independent of graph extraction, additional schema.org serializers—such as `Organization`, `ScholarlyArticle`, `Grant`, or `Dataset`—can be added without modifying the underlying semantic graph model.

---

## SHACL Generation

The toolkit automatically generates SHACL NodeShapes from the discovered schema, including:

- Datatype constraints
- Object property constraints
- Target class constraints (`sh:class`)
- IRI node constraints (`sh:nodeKind sh:IRI`)
- Required property constraints
- Cardinality constraints
- Enumeration constraints

Object property constraints are generated directly from the discovered relationship topology, preserving valid source-to-target label combinations rather than producing the Cartesian product of all possible source and target classes.

---

## Validation

Exported RDF is validated against the generated SHACL shapes using **pySHACL**.

Validation verifies:

- Datatype constraints
- Object property relationships
- Target class constraints
- Cardinality constraints
- Enumerated values

Because validation uses previously generated SHACL shapes rather than rediscovering the ontology, semantic regressions can be detected as the underlying graph evolves.

---

## Provenance

The toolkit generates provenance metadata using the W3C PROV Ontology (PROV-O).

Provenance captures the semantic processing workflow, documenting how generated RDF artifacts were produced and establishing traceability between the source graph, generated semantic artifacts, validation, and reasoning steps.

---

## Reasoning

The toolkit supports OWL RL reasoning over exported RDF graphs.

Reasoning materializes inferred triples that are logically implied by the ontology, making implicit knowledge explicit for downstream consumers. A subsequent cleanup step removes redundant axiomatic statements to produce a concise inferred graph suitable for inspection and reuse.

---

## Interactive HTML Reports

The toolkit generates an interactive HTML report that summarizes the complete semantic processing pipeline.

The report includes:

- Executive summary
- Schema overview
- Validation results
- Generated artifacts
- Embedded syntax-highlighted RDF viewers
- Provenance outputs
- Reasoning outputs
- Interactive navigation

This report provides a convenient, self-contained overview of the generated semantic artifacts without requiring external RDF tooling.

---

# Architecture

```text
                    discover.py
                         │
                         ▼
                DiscoveryService
                         │
                         ▼
                Schema Discovery
                         │
                         ▼
                   GraphSchema
                  ┌──────┼──────┐
                  ▼      ▼      ▼
        ontology.ttl  ontology_nary.ttl
                  │
                  ▼
             shapes.ttl


                    validate.py
                         │
                         ▼
               ValidationService
                         │
                         ▼
                  Neo4j Reader
                         │
                         ▼
                  SemanticGraph
      ┌────────────┼─────────────┬─────────────┐
      ▼            ▼             ▼             ▼
 Binary RDF   N-ary RDF      JSON-LD     schema.org
      │
      ▼
 PROV-O Provenance
      │
      ▼
 SHACL Validation
      │
      ▼
 OWL RL Reasoning
      │
      ▼
 Inference Cleanup
      │
      ▼
 Interactive HTML Report
```

---

# Project Structure

```text
discover.py
validate.py
main.py

ontology_toolkit/

    services/
        discovery.py
        validation.py

    connection.py

    discover_schema.py
    neo4j_reader.py

    schema_model.py
    semantic_model.py

    ontology_common.py

    generate_ontology.py
    generate_ontology_nary.py
    generate_shacl.py

    export_rdf.py
    export_rdf_nary.py
    export_jsonld.py
    export_schema_org.py

    generate_provenance.py
    reasoning.py

    validate_shacl.py

    reports/
        layout.py
        sections.py
        report.py

    printer.py
```

---

# Generated Outputs

Discovery generates:

```text
ontology.ttl
ontology_nary.ttl
shapes.ttl
```

Validation generates:

```text
graph.ttl
graph_nary.ttl
graph.jsonld

schema_org/
    *.json

provenance.ttl

graph_inferred.ttl
graph_inferred_clean.ttl

validation_report.txt

report.html
```

---

# Current Limitations

- Generic JSON-LD currently follows the binary RDF model and does not yet represent relationship resources using the n-ary model.
- schema.org serialization currently supports `Person` entities only.
- Schema discovery operates on the contents of an existing Neo4j property graph.

---

# Future Enhancements

Potential future enhancements include:

- Generic JSON-LD n-ary serialization
- Additional schema.org serializers (`Organization`, `ScholarlyArticle`, `Grant`, `Dataset`)
- SPARQL query support
- SHACL Rules / SHACL-AF
- Competency question testing
- VoID metadata generation
- DCAT dataset descriptions
- Graph visualization
- Additional ontology profiles
- Additional import and export formats
- Optional RDF-star serialization

---

# AI Reviews and Responses

- `CLAUDE_REVIEW.md`
- `CHATGPT_CLAUDE_REVIEW_RESPONSE.md`

---

# License

MIT License