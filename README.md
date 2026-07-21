# Semantic Graph Toolkit

A Python toolkit for discovering the schema of a Neo4j property graph and generating Semantic Web artifacts including OWL ontologies, RDF exports, JSON-LD exports, schema.org JSON-LD, SHACL shapes, and validation reports.

The toolkit provides a database-independent semantic graph model that separates instance data from serialization, enabling multiple serialization formats while serving as a foundation for future extensions such as RDF-star and additional graph-processing pipelines.

---

# Overview

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

# Workflow

The toolkit provides three entry points.

## `discover.py`

Discovers the semantic schema from Neo4j and generates the semantic contract.

Outputs:

- `ontology.ttl`
- `shapes.ttl`

This workflow should be run whenever the ontology changes or the graph schema is intentionally updated.

---

## `validate.py`

Reads graph instance data, exports semantic representations, and validates the graph against the existing SHACL shapes.

Outputs:

- `graph.ttl`
- `graph.jsonld`
- `schema_org/*.json`
- `validation_report.txt`

Unlike discovery, this workflow does **not** regenerate the ontology or SHACL shapes. Instead, it validates the current graph against the previously established semantic contract.

---

## `main.py`

A convenience workflow that performs both discovery and validation.

```text
Discover schema
        ↓
Generate ontology.ttl
Generate shapes.ttl
        ↓
Read graph
        ↓
Export RDF / JSON-LD / schema.org
        ↓
Validate against SHACL
```

This is useful during development but is not required for routine validation.

---

# Design Principles

The toolkit is organized around four independent layers:

1. Schema discovery
2. Database-independent semantic graph representation
3. Serialization and validation
4. Workflow orchestration

This separation allows serialization formats, validators, and graph-processing components to evolve independently.

---

# Current Capabilities

## Schema Discovery

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

## Property Analysis

Analyzes discovered properties to identify:

- Datatypes
- Required vs. optional properties
- Identifier candidates
- Enumerated values
- Example values

---

## Semantic Graph Model

Provides a reusable semantic representation of Neo4j instance data through:

- `EntityInstance`
- `RelationshipInstance`
- `SemanticGraph`

This layer decouples Neo4j data extraction from serialization, allowing multiple exporters and graph-processing components to reuse the same semantic graph.

---

## OWL Ontology Generation

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

## RDF and JSON-LD Export

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

Relationship metadata is preserved in the semantic graph model but is not currently represented in RDF or JSON-LD.

---

## Schema.org JSON-LD Export

Generates web-oriented schema.org JSON-LD from the same `SemanticGraph` model used for RDF serialization.

Current support includes:

- `Person`
- `affiliation`
- `knowsAbout`
- `sameAs`

The exporter generates one schema.org JSON-LD document per supported entity.

Additional serializers (such as `Organization`, `ScholarlyArticle`, and `Grant`) can be added without changing the graph extraction process.

---

## SHACL Generation

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

## Validation

Validates exported RDF against the existing SHACL shapes using pySHACL.

Validation verifies:

- Datatype properties
- Object property relationships
- Target class constraints
- Cardinality constraints
- Enumerated values

Because validation uses previously generated SHACL shapes, semantic regressions can be detected without rediscovering the ontology.

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
                    │         │
                    ▼         ▼
             ontology.ttl  shapes.ttl


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
                   │      │      │
                   ▼      ▼      ▼
              RDF     JSON-LD  schema.org
                   │
                   ▼
             SHACL Validation


                      main.py
                          │
                          ▼
            Discovery → Validation
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

    generate_ontology.py
    generate_shacl.py

    export_rdf.py
    export_jsonld.py
    export_schema_org.py

    validate_shacl.py
    printer.py
```

---

# Generated Outputs

Discovery generates:

```text
ontology.ttl
shapes.ttl
```

Validation generates:

```text
graph.ttl
graph.jsonld

schema_org/
    *.json

validation_report.txt
```

---

# Current Limitations

- Relationship metadata is preserved in the semantic graph model but is not yet represented in RDF or JSON-LD and therefore is not yet validated.
- Schema.org serialization currently supports `Person` entities only.
- Schema discovery is based on the contents of an existing Neo4j property graph.
- OWL reasoning is not currently performed during ontology generation or validation.
- RDF-star serialization is not yet supported.

---

# Future Enhancements

Potential future enhancements include:

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

# License

MIT License