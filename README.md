# Semantic Graph Toolkit

A Python toolkit for discovering the schema of a Neo4j property graph and generating Semantic Web artifacts including OWL ontologies, RDF exports, JSON-LD exports, schema.org JSON-LD, SHACL shapes, and validation reports.

The toolkit provides a database-independent semantic graph model that separates instance data from serialization, enabling multiple serialization formats while serving as a foundation for future extensions such as RDF-star and additional graph-processing pipelines.

---

## Overview

The Semantic Graph Toolkit bridges Neo4j property graphs and Semantic Web technologies by:

- Discovering graph schema from Neo4j
- Analyzing node and relationship properties
- Discovering semantic graph topology (source→target label pairs)
- Building a reusable semantic graph model
- Generating an OWL ontology
- Exporting graph instances as RDF/Turtle
- Exporting generic JSON-LD
- Exporting schema.org JSON-LD
- Generating SHACL validation shapes
- Validating exported RDF with pySHACL

Rather than serializing directly from Neo4j, the toolkit first loads instance data into a reusable `SemanticGraph` object model. This architectural separation allows multiple serializers and graph-processing components to operate independently of Neo4j.

---

## Design Principles

The toolkit is organized around three independent layers:

1. **Schema discovery** from Neo4j
2. **Database-independent semantic graph representation**
3. **Serialization and validation**

This separation allows new serialization formats and graph-processing components to be added without changing how graph data is extracted from Neo4j.

---

## Current Capabilities

### Schema Discovery

Automatically discovers:

- Node labels
- Relationship types
- Node properties
- Relationship properties
- Graph topology
- Relationship source→target label pairs

Relationship topology is preserved in the discovered schema, allowing semantic relationship constraints to be generated without creating invalid source/target combinations.

Relationship properties are preserved in the semantic graph model for future processing but are not currently represented in exported RDF or JSON-LD.

---

### Property Analysis

Analyzes discovered properties to identify:

- Datatypes
- Required vs. optional properties
- Identifier candidates
- Enumerated values
- Example values

---

### Semantic Graph Model

Provides a reusable semantic representation of Neo4j instance data through:

- `EntityInstance`
- `RelationshipInstance`
- `SemanticGraph`

This layer decouples Neo4j data extraction from serialization, allowing multiple exporters and graph-processing components to reuse the same semantic graph.

---

### OWL Ontology Generation

Generates:

- OWL classes
- Object properties
- Datatype properties
- Domains
- Ranges
- Inverse properties (where applicable)
- Functional properties (where applicable)
- Dublin Core metadata
- Schema.org mappings
- SKOS concept relationships

---

### RDF and JSON-LD Export

Exports graph instances as RDF/Turtle and generic JSON-LD.

Resources receive stable URIs derived from identifier properties whenever available.

Serialization includes:

- RDF
- RDFS
- OWL
- SKOS
- Schema.org
- Dublin Core

Relationships are exported as RDF object properties, while literal values become datatype properties.

Relationship metadata (properties attached to Neo4j relationships) is preserved in the semantic graph model but is not currently represented in RDF or JSON-LD.

---

### Schema.org JSON-LD Export

Generates web-oriented schema.org JSON-LD from the same `SemanticGraph` model used for RDF serialization.

Current support includes:

- `Person` serialization for Faculty entities
- `affiliation`
- `knowsAbout`
- `sameAs`

The exporter generates one schema.org JSON-LD document per supported entity, allowing the toolkit to produce structured data suitable for search engines and other schema.org consumers.

Because schema.org serialization operates on the semantic graph rather than directly on Neo4j, additional serializers (such as `Organization`, `ScholarlyArticle`, and `Grant`) can be added without changing the graph extraction process.

---

### SHACL Generation

Automatically generates SHACL NodeShapes including:

- Datatype constraints
- Object property constraints
- Target class constraints (`sh:class`)
- IRI node constraints (`sh:nodeKind sh:IRI`)
- Required property constraints
- Cardinality constraints
- Enumeration constraints

Object property constraints are generated from the discovered relationship topology, preserving valid source→target label combinations rather than generating the Cartesian product of source and target labels.

---

### Validation

Validates the generated RDF graph against the generated SHACL shapes using pySHACL and produces a validation report identifying constraint violations.

Validation verifies:

- Datatype properties
- Object property relationships
- Target class constraints
- Cardinality constraints
- Enumerated values

Relationship metadata is preserved in the semantic graph model but is not yet validated.

---

## Architecture

```text
                  Neo4j Property Graph
                           │
               ┌───────────┴───────────┐
               │                       │
               ▼                       ▼
      Schema Discovery           Neo4j Reader
               │                       │
               ▼                       ▼
        GraphSchema             SemanticGraph
               │                       │
               │              ┌────────┴────────┐
               │              │                 │
               ▼              ▼                 ▼
       OWL Generator     RDF Graph Builder   schema.org
               │              │              Serializer
               │              │                 │
               ▼              ▼                 ▼
        ontology.ttl      graph.ttl      schema_org/*.json
               │              │
               │              ▼
               │         graph.jsonld
               │              │
               └──────────────┴──────────────┐
                                             ▼
                                      SHACL Validation
```

---

## Generated Outputs

Running the toolkit produces:

```text
ontology.ttl
graph.ttl
graph.jsonld
schema_org/
    *.json
shapes.ttl
validation_report.txt
```

Artifacts generated include:

- OWL ontology
- RDF knowledge graph (Turtle)
- Generic JSON-LD knowledge graph
- schema.org JSON-LD documents
- SHACL validation shapes
- SHACL validation report

---

## Current Limitations

The toolkit currently has the following limitations:

- Relationship metadata (properties attached to Neo4j relationships) is preserved in the semantic graph model but is not yet represented in RDF or JSON-LD and is therefore not yet validated by SHACL.
- Schema.org serialization currently supports `Person` entities only.
- Schema discovery is based on the contents of an existing Neo4j property graph.
- The current workflow regenerates the discovered ontology and SHACL shapes each time the toolkit is run. A future validation-only mode will validate graph updates against a previously generated semantic contract.
- OWL reasoning is not currently performed as part of ontology generation or validation.
- RDF-star serialization is not yet supported.

---

## Future Enhancements

Potential future enhancements include:

- Separate ontology discovery and validation workflows
- Relationship property serialization
- RDF-star serialization
- Additional schema.org serializers (`Organization`, `ScholarlyArticle`, `Grant`, `Dataset`)
- SPARQL query support
- OWL reasoning integration
- SHACL-AF rules
- Competency question testing
- VoID metadata generation
- DCAT dataset descriptions
- Graph visualization
- Additional import/export formats

---

## License

MIT License