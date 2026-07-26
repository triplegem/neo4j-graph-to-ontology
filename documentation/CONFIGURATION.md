# Semantic Graph Toolkit Configuration Guide

The Semantic Graph Toolkit automatically discovers the schema of a Neo4j property graph and generates Semantic Web artifacts including OWL ontologies, RDF graphs, JSON-LD, SHACL shapes, provenance, and reasoned RDF.

The generated artifacts are intended to serve as a high-quality starting point rather than a complete ontology. While the toolkit automates structural modeling, semantic design decisions remain under the control of the user.

---

# Ontology Design

The generated ontology intentionally avoids making strong semantic assumptions whenever possible.

The toolkit automatically generates:

- Classes
- Object properties
- Datatype properties
- Labels
- Comments
- Datatype inference
- Basic domain and range declarations (optional)

The following ontology features should generally be added manually because they require domain knowledge:

- Inverse properties
- Disjoint classes
- Equivalent classes
- Property chains
- Cardinality restrictions
- Property characteristics (functional, inverse functional, symmetric, transitive, etc.)
- Additional domain and range constraints
- Custom annotations

The generated ontology should be viewed as the foundation for a domain ontology rather than the finished product.

---

# Relationship Mapping

Neo4j relationship names describe the local property graph.

They should **not** be chosen simply because they resemble OWL or Schema.org predicates.

For example, rather than naming a relationship:

```text
SAME_AS
```

the toolkit uses:

```text
HAS_ORCID
```

which clearly represents the relationship in the source graph.

The ontology then maps this relationship to an appropriate RDF property.

This avoids unintentionally asserting strong Semantic Web semantics.

For example:

```text
Neo4j

HAS_ORCID

↓

Ontology

kgo:hasOrcid

↓

Optional profile alignments

schema:identifier
vivo:orcidId
```

Likewise,

```text
WORKS_IN
```

should not automatically become

```text
schema:worksFor
```

unless that mapping is intentionally configured.

Relationship names should describe the graph, while ontology mappings describe the semantics.

---

# Ontology Profiles

Ontology Profiles provide interoperability with existing vocabularies while preserving the project's local ontology.

Current profiles include:

- Schema.org
- VIVO

Profiles add additional superclass relationships.

Example:

```text
kgo:Faculty

rdfs:subClassOf

schema:Person
vivo:FacultyMember
```

The local ontology remains authoritative.

Profiles simply align the ontology with external vocabularies.

Profiles can be enabled or disabled by editing:

```python
ACTIVE_PROFILES = [
    SCHEMA_ORG_PROFILE,
    VIVO_PROFILE,
]
```

Additional profiles can easily be created for vocabularies such as:

- FOAF
- Dublin Core
- CIDOC CRM
- BIBO
- GeoSPARQL
- SOSA/SSN

---

# Namespace Configuration

Namespace bindings are managed centrally through:

```python
bind_namespaces()
```

All generated RDF artifacts should use the same namespace configuration.

Typical namespaces include:

- rdf
- rdfs
- owl
- xsd
- schema
- skos
- prov
- vivo
- kgo

Additional namespaces may be added as required by the project.

---

# SHACL Validation

The toolkit automatically generates structural SHACL shapes based on the discovered graph schema.

Automatically generated constraints include:

- Property datatypes
- Property classes
- Cardinality (where appropriate)
- Required properties inferred from the graph

However, business rules should generally be implemented manually.

Examples include:

- Every Faculty must have an email address.
- Every Publication must have a title.
- Every Grant must have an award number.
- Every Department must belong to exactly one College.

These constraints depend on project requirements rather than graph structure.

Manual SHACL files can therefore be added alongside the generated shapes.

---

# Provenance

The toolkit can generate provenance metadata using the W3C PROV ontology.

Typical provenance information includes:

- Generation time
- Source datasets
- Activities
- Software agents
- Data derivation

Projects may extend provenance by modeling additional entities such as:

- prov:Activity
- prov:Agent
- prov:SoftwareAgent
- prov:Organization
- prov:Person

This provides traceability for generated RDF artifacts.

---

# OWL Reasoning

The toolkit supports OWL RL reasoning using `owlrl`.

Reasoning can infer additional knowledge such as:

- Subclass membership
- Subproperty relationships
- Equivalent classes
- Equivalent properties
- Inverse properties
- Transitive relationships

Reasoning expands the RDF graph while preserving asserted triples.

Because OWL RL is intentionally limited for tractability, some OWL constructs are not supported.

---

# Manual Ontology Enhancements

Many ontology features require human expertise and should be added after generation.

Examples include:

- Inverse properties
- Equivalent properties
- Equivalent classes
- Disjoint classes
- Property chains
- Functional properties
- Inverse functional properties
- Symmetric properties
- Transitive properties
- Rich class restrictions

These enhancements improve reasoning quality while reflecting domain-specific knowledge.

---

# Best Practices

- Treat Neo4j relationship names as local graph terminology rather than Semantic Web vocabulary.
- Keep the generated ontology as the authoritative model for the project.
- Use ontology profiles to improve interoperability without changing local semantics.
- Add manual SHACL shapes for business rules that cannot be inferred from the graph.
- Add manual OWL axioms where domain expertise is required.
- Use reasoning to enrich RDF graphs after ontology generation.
- Manage namespace bindings centrally so all generated artifacts use consistent prefixes.
- Review generated ontologies before publication to ensure semantic accuracy.

---

# Philosophy

The Semantic Graph Toolkit is designed to bridge the gap between labeled property graphs and Semantic Web technologies.

Rather than attempting to infer every semantic decision automatically, the toolkit generates a solid semantic foundation while leaving ontology engineering decisions under the control of the user.

This approach combines automation with expert knowledge, producing RDF that is both interoperable and faithful to the original property graph.