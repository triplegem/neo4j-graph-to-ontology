# Ontology Toolkit

A Python toolkit for discovering the schema of a Neo4j property graph and generating Semantic Web artifacts including OWL ontologies, RDF exports, SHACL shapes, and validation reports.

The toolkit also provides a database-independent semantic graph model that separates instance data from serialization, enabling future support for additional formats such as JSON-LD and RDF-star.

---

## Overview

The Ontology Toolkit bridges Neo4j property graphs and Semantic Web technologies by:

- Discovering graph schema from Neo4j
- Analyzing node and relationship properties
- Generating an OWL ontology
- Exporting graph instances as RDF/Turtle
- Generating SHACL validation shapes
- Validating exported RDF with pySHACL

Internally, Neo4j instance data is first loaded into a reusable `SemanticGraph` object model before serialization. This separation allows future exporters and processors to operate independently of Neo4j.

---

## Current Capabilities

### Schema Discovery

Automatically discovers:

- Node labels
- Relationship types
- Node properties
- Relationship properties
- Graph topology

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

This layer decouples graph reading from RDF serialization and serves as the foundation for future exporters and graph processing.

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

### RDF Export

Exports graph instances as RDF/Turtle.

Resources receive stable URIs derived from identifier properties whenever available.

Current serialization includes:

- RDF
- RDFS
- OWL
- SKOS
- Schema.org
- Dublin Core

### SHACL Generation

Automatically generates SHACL NodeShapes including:

- Datatype constraints
- Required property constraints
- Cardinality constraints
- Enumeration constraints

### Validation

Validates exported RDF against generated SHACL shapes using pySHACL and produces a validation report identifying any constraint violations.

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
        Semantic Web Outputs
                 │
     ┌───────────┼───────────┐
     ▼           ▼           ▼
 OWL Ontology  RDF Export  SHACL Shapes
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
└── vocab.py
```

---

## Generated Outputs

Running the toolkit produces:

```text
ontology.ttl
graph.ttl
shapes.ttl
validation_report.txt
```

These artifacts include:

- OWL ontology
- RDF knowledge graph
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
RDF Serialization
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
- rdflib
- pySHACL

---

## Future Enhancements

Planned or potential future enhancements include:

- JSON-LD serialization
- RDF-star serialization
- SPARQL endpoint support
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