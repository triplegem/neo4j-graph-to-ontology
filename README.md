# Ontology Toolkit

A Python toolkit for automatically discovering the schema of a Neo4j knowledge graph and generating semantic web artifacts including OWL ontologies, RDF exports, SHACL validation shapes, and validation reports.

## Overview

The Ontology Toolkit bridges Neo4j property graphs and Semantic Web technologies by automatically analyzing an existing graph and producing standards-compliant semantic representations.

The toolkit performs:

- Schema discovery
- Datatype inference
- Identifier detection
- Cardinality inference
- Enumeration inference
- OWL ontology generation
- RDF/Turtle export
- SHACL shape generation
- SHACL validation

## Features

### Schema Discovery

Automatically discovers:

- Node labels
- Relationship types
- Node properties
- Relationship properties
- Graph topology

### Property Analysis

Infers:

- Datatypes
- Required properties
- Nullable properties
- Identifier candidates
- Enumerated values
- Example values

### OWL Ontology Generation

Generates:

- OWL classes
- Object properties
- Datatype properties
- Domains
- Ranges
- Inverse properties
- Functional properties
- Dublin Core metadata
- Schema.org alignment
- SKOS alignment

### RDF Export

Exports the Neo4j graph as RDF/Turtle using:

- RDF
- OWL
- SKOS
- Schema.org

Resources receive stable URIs using discovered identifiers whenever possible.

### SHACL Generation

Automatically generates SHACL NodeShapes including:

- Datatype constraints
- Required properties
- Cardinality constraints
- Enumeration constraints
- Identifier constraints

### Validation

Validates exported RDF against generated SHACL shapes using pySHACL.

Produces a validation report identifying any constraint violations.

---

## Project Structure

```
ontology-toolkit/

├── main.py
├── ontology_toolkit/
│   ├── connection.py
│   ├── discover_schema.py
│   ├── property_analysis.py
│   ├── type_inference.py
│   ├── export_rdf.py
│   ├── generate_ontology.py
│   ├── generate_shacl.py
│   ├── validate_shacl.py
│   ├── printer.py
│   ├── models.py
│   └── vocab.py
```

---

## Generated Outputs

Running the toolkit produces:

```
ontology.ttl
graph.ttl
shapes.ttl
validation_report.txt
```

These artifacts include:

- OWL ontology
- RDF knowledge graph
- SHACL validation shapes
- Validation report

---

## Example Workflow

```
Neo4j Property Graph
          │
          ▼
Schema Discovery
          │
          ▼
Property Analysis
          │
          ▼
Ontology Generation
          │
          ▼
RDF Export
          │
          ▼
SHACL Generation
          │
          ▼
SHACL Validation
          │
          ▼
Validation Report
```

---

## Requirements

Python 3.11+

### Packages

```
neo4j
rdflib
pyshacl
python-dotenv
```

Install with:

```bash
pip install neo4j rdflib pyshacl python-dotenv
```

---

## Running

Configure your Neo4j connection in a `.env` file.

Example:

```
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
- OWL
- SHACL
- SKOS
- Schema.org
- Dublin Core
- pySHACL
- rdflib

---

## Future Enhancements

Potential future improvements include:

- SPARQL endpoint generation
- Reasoning with OWL reasoners
- SHACL-AF rules
- Competency question testing
- Ontology visualization
- JSON-LD export
- VoID metadata generation
- DCAT dataset descriptions

---

## License

MIT License