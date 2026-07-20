# Ontology Toolkit

A Python toolkit for discovering the schema of a Neo4j property graph and generating Semantic Web artifacts including OWL ontologies, RDF exports, JSON-LD exports, SHACL shapes, and validation reports.

The toolkit also provides a database-independent semantic graph model that separates instance data from serialization, enabling multiple serialization formats while serving as a foundation for future extensions such as RDF-star.

---

## Overview

The Ontology Toolkit bridges Neo4j property graphs and Semantic Web technologies by:

- Discovering graph schema from Neo4j
- Analyzing node and relationship properties
- Generating an OWL ontology
- Exporting graph instances as RDF/Turtle and JSON-LD
- Generating SHACL validation shapes
- Validating exported RDF with pySHACL

Internally, Neo4j instance data is first loaded into a reusable `SemanticGraph` object model before serialization. This separation allows multiple serializers and future graph processors to operate independently of Neo4j.

---

## Current Capabilities

### Schema Discovery

Automatically discovers:

- Node labels
- Relationship types
- Node properties
- Relationship properties
- Graph topology

Relationship properties are preserved in the semantic graph model for future processing but are not currently represented in exported RDF or JSON-LD.

### Property Analysis

Analyzes discovered properties to identify:

- Datatypes
- Required vs. optional properties
- Identifier candidates
- Enumerated values
- Example values

### Semantic Graph Model

Provides a reusable semantic representation of Neo4j instance data through:

- `EntityInstance`
- `RelationshipInstance`
- `SemanticGraph`

This layer decouples graph reading from serialization and serves as the foundation for current and future exporters and graph-processing components.

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

### RDF and JSON-LD Export

Exports graph instances as RDF/Turtle and JSON-LD.

Resources receive stable URIs derived from identifier properties whenever available.

Current serialization includes:

- RDF
- RDFS
- OWL
- SKOS
- Schema.org
- Dublin Core

Relationships are exported as RDF object properties, while literal values become datatype properties.

Relationship metadata (properties attached to Neo4j relationships) is preserved in the semantic graph model but is not currently represented in RDF or JSON-LD.

### SHACL Generation

Automatically generates SHACL NodeShapes including:

- Datatype constraints
- Required property constraints
- Cardinality constraints
- Enumeration constraints

Generated shapes validate node properties and graph structure derived from the discovered schema.

### Validation

Validates the generated RDF graph against the generated SHACL shapes using pySHACL and produces a validation report identifying constraint violations.

Validation currently focuses on node properties and graph structure. Relationship metadata is not yet validated.

---

## Architecture

```text
Neo4j Property Graph
          │
          ├──────────────┐
          │              │
          ▼              ▼
 Schema Discovery   Neo4j Reader
          │              │
          ▼              ▼
     GraphSchema   SemanticGraph
          │              │
          └──────┬───────┘
                 ▼
          RDF Graph Builder
                 │
      ┌──────────┼──────────┐
      ▼          ▼          ▼
 OWL Ontology  RDF/Turtle  JSON-LD
                                │
                                ▼
                         SHACL Validation
```

---

## Project Structure

```text
ontology_toolkit/

├── connection.py
├── discover_schema.py
├── export_jsonld.py
├── export_rdf.py
├── generate_ontology.py
├── generate_shacl.py
├── models.py
├── neo4j_reader.py
├── printer.py
├── property_analysis.py
├── semantic_model.py
├── type_inference.py
├── uri.py
├── validate_shacl.py
├── vocab.py
└── serializers/
    ├── __init__.py
    ├── rdf.py
    └── jsonld.py
```

---

## Generated Outputs

Running the toolkit produces:

```text
ontology.ttl
graph.ttl
graph.jsonld
shapes.ttl
validation_report.txt
```

These artifacts include:

- OWL ontology
- RDF knowledge graph (Turtle)
- JSON-LD knowledge graph
- SHACL validation shapes
- SHACL validation report

---

## Example Workflow

```text
Neo4j Property Graph
          │
          ▼
Schema Discovery
          │
          ▼
GraphSchema
          │
          ▼
Neo4j Reader
          │
          ▼
SemanticGraph
          │
          ▼
RDF Graph Builder
      ┌───┴────┐
      ▼        ▼
 RDF/Turtle  JSON-LD
      │
      ▼
SHACL Validation
```

---

## Requirements

Python 3.11+

### Packages

- neo4j
- rdflib
- pyshacl
- python-dotenv

Install with:

```bash
pip install neo4j rdflib pyshacl python-dotenv
```

---

## Running

Configure your Neo4j connection in a `.env` file.

Example:

```text
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password
```

Run:

```bash
python main.py
```

---

## Technologies

- Python
- Neo4j
- RDF
- RDFS
- OWL
- SHACL
- SKOS
- Schema.org
- Dublin Core
- JSON-LD
- rdflib
- pySHACL

---

## Current Limitations

The toolkit currently has the following limitations:

- Relationship metadata (properties attached to Neo4j relationships) is preserved in the semantic graph model but is not yet represented in RDF or JSON-LD exports.
- SHACL generation currently validates node properties and graph structure, but does not validate relationship metadata.
- Schema discovery is based on the contents of an existing Neo4j property graph; the toolkit does not infer ontologies from unstructured text or use LLMs.
- OWL reasoning is not currently performed as part of ontology generation or validation.
- RDF-star serialization is not yet supported.

---

## Future Enhancements

Planned or potential future enhancements include:

- RDF-star serialization
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