# Comprehensive Architecture Review: Ontology Toolkit Repository

**Review Date:** 2026-07-26
**Reviewer:** Claude Sonnet 4.5
**Repository:** ontology-toolkitI read the generated artifacts, the generators, and the reasoning pipeline, and ran a few checks against the actual outputs. Overall assessment first,
  then the specific problems.

  Overall

  The architecture (discover → SemanticGraph → N serializers) is sound, and several decisions are genuinely good: reusing SKOS/schema.org classes instead
  of minting parallel ones, preserving relationship topology instead of taking the Cartesian product, separating the "semantic contract" (discover.py) from
  instance validation (validate.py), and shipping both a binary and reified relationship view.

  The problems are almost all in one family: axioms and identity statements are being derived from observed data or from string names, then emitted as 
  global logical commitments. In OWL that isn't a heuristic — it's a claim about all possible worlds, and a reasoner will act on it. Below, ranked by how
  much damage they do.

  ---
  1. SAME_AS → owl:sameAs is corrupting the graph today

  vocab.py:31-41 maps LPG edge names to standard predicates by string match, so a Neo4j edge named SAME_AS becomes owl:sameAs — the strongest identity
  assertion in OWL. Combined with §2, this is already producing wrong inferences. From your own output/graph_inferred_clean.ttl:107-118:

  turtle
  <...resource#orcid/0000-0003-2310-6687> a owl:Thing, kgo:Faculty, kgo:ORCID, schema:Person ;
      kgo:email "jd732@cornell.edu" ;
      kgo:netid "jd732" ;
      kgo:rank "Associate Professor" .

  An ORCID identifier is now a professor with an email and an academic rank. And in the other direction (graph_inferred_clean.ttl:71-78), Julia
  Dshemuchadse's kgo:identifier is now her ORCID string, colliding with any other identifier she has. Worse, at graph_inferred_clean.ttl:86-87 and
  :126-127:

  turtle
  <...grant/2016522> kgo:hasInvestigator <...faculty/de54>, <...orcid/0000-0002-1624-9711> .

  Every grant and publication now has twice as many investigators/authors as it really has. Any downstream count, dedup, or aggregation is wrong.

  The same name-based mapping applies skos:exactMatch (symmetric and transitive, per SKOS S43) to EXACT_MATCH edges. Because skos:exactMatch ⊑ … ⊑
  skos:semanticRelation, which has rdfs:domain/rdfs:range skos:Concept, any consumer who loads SKOS will infer your kgo:Wikidata instances are
  skos:Concepts. You don't see it locally only because export_reasoned_rdf.py never imports SKOS.

  In an LPG, SAME_AS almost always means "linked record," not owl:sameAs. Mapping identity predicates by edge-name string is unsafe by construction — this
  should be an explicit, per-edge opt-in in the profile, not a lookup table.

  2. External identifiers modeled as classes, with the real IRI trapped in a literal

  kgo:ORCID and kgo:Wikidata are OWL classes whose instances are locally-minted URIs (kgr:orcid/0000-0002-...), and the actual global IRI is a string:
  kgo:uri "https://orcid.org/..."^^xsd:anyURI (graph.ttl:160-178). This is the literal-encoded-link anti-pattern, and it's the root of §1.

  assertion in OWL. Combined with §2, this is already producing wrong inferences. From your own output/graph_inferred_clean.ttl:107-118:

  turtle
  <...resource#orcid/0000-0003-2310-6687> a owl:Thing, kgo:Faculty, kgo:ORCID, schema:Person ;
      kgo:email "jd732@cornell.edu" ;
      kgo:netid "jd732" ;
      kgo:rank "Associate Professor" .

  An ORCID identifier is now a professor with an email and an academic rank. And in the other direction (graph_inferred_clean.ttl:71-78), Julia
  Dshemuchadse's kgo:identifier is now her ORCID string, colliding with any other identifier she has. Worse, at graph_inferred_clean.ttl:86-87 and
  :126-127:

  turtle
  <...grant/2016522> kgo:hasInvestigator <...faculty/de54>, <...orcid/0000-0002-1624-9711> .

  Every grant and publication now has twice as many investigators/authors as it really has. Any downstream count, dedup, or aggregation is wrong.

  The same name-based mapping applies skos:exactMatch (symmetric and transitive, per SKOS S43) to EXACT_MATCH edges. Because skos:exactMatch ⊑ … ⊑
  skos:semanticRelation, which has rdfs:domain/rdfs:range skos:Concept, any consumer who loads SKOS will infer your kgo:Wikidata instances are
  skos:Concepts. You don't see it locally only because export_reasoned_rdf.py never imports SKOS.

  In an LPG, SAME_AS almost always means "linked record," not owl:sameAs. Mapping identity predicates by edge-name string is unsafe by construction — this
  should be an explicit, per-edge opt-in in the profile, not a lookup table.

  2. External identifiers modeled as classes, with the real IRI trapped in a literal

  kgo:ORCID and kgo:Wikidata are OWL classes whose instances are locally-minted URIs (kgr:orcid/0000-0002-...), and the actual global IRI is a string:
  kgo:uri "https://orcid.org/..."^^xsd:anyURI (graph.ttl:160-178). This is the literal-encoded-link anti-pattern, and it's the root of §1.

  Two independent costs:
  - No linked data. Nothing in the graph points at https://orcid.org/0000-0002-1624-9711 or http://www.wikidata.org/entity/Q11468 as a resource. A consumer
  cannot follow the link, and cannot join your graph to ORCID or Wikidata without string-parsing a literal.
  - Your Wikidata URIs point at https://www.wikidata.org/wiki/Q11468 — the human-readable web page, not the entity IRI
  http://www.wikidata.org/entity/Q11468. Even after string extraction, the join fails.

  Either mint the external IRI directly (kgr:faculty/de54 owl:sameAs <https://orcid.org/0000-0002-1624-9711>, kgo:Concept skos:exactMatch 
  <http://www.wikidata.org/entity/Q11468>) or, if you want to keep identifier provenance, use the schema:PropertyValue/vivo:orcidId pattern. What you must
  not do is keep both the class-per-identifier-scheme model and owl:sameAs.

  3. rdfs:domain/rdfs:range inferred from a data snapshot

  ontology_common.py:322-330 emits rdfs:domain when exactly one class currently uses a property. The comment says this determines "whether a domain can
  safely be emitted" — it's the opposite of safe. kgo:description rdfs:domain kgo:ConceptScheme (ontology.ttl:54-59) means anything with a description is a
  ConceptScheme. Add a description to a Department and a reasoner will type it as a skos:ConceptScheme. Same for kgo:email → Faculty, kgo:venue → 
  Publication, kgo:awardNumber → Grant.

  The concrete failure mode is worse than hypothetical, because of a namespace collision with the n-ary model:

  - rdf_nary.py:82-89 emits relationship properties as KGO[key] — the same namespace as node properties.
  - So a relationship carrying startDate (very plausible for AFFILIATED_WITH) emits kgo:startDate, whose rdfs:domain is kgo:Grant.
  - OWL RL then infers your kgo:AffiliatedWithRelationship instance is a Grant.

  The inverse problem also bites: when 2+ classes share a property the domain is dropped entirely rather than expressed as owl:unionOf, so information is
  silently lost. And because domains flip on and off as data changes while owl:versionInfo stays "1.0" (ontology_common.py:198-202), the logical meaning of
  your terms changes between builds with no version signal.

  Recommendation: don't derive domain/range from instance data at all. Put them in the profile (profiles/faculty.py), where a human commits to them; or
  emit them as SHACL only, where closed-world constraint semantics is what you actually want.

  4. owl:FunctionalProperty is derived from the wrong statistic

  property_analysis.py:65 computes unique = distinct == len(non_null) — i.e. values are distinct across all instances of the label. That is
  inverse-functionality (a key). But ontology_common.py:285-296 uses it to emit owl:FunctionalProperty, which means at most one value per subject.
  Different axiom entirely.
  turtle
  <...grant/2016522> kgo:hasInvestigator <...faculty/de54>, <...orcid/0000-0002-1624-9711> .

  Every grant and publication now has twice as many investigators/authors as it really has. Any downstream count, dedup, or aggregation is wrong.

  The same name-based mapping applies skos:exactMatch (symmetric and transitive, per SKOS S43) to EXACT_MATCH edges. Because skos:exactMatch ⊑ … ⊑
  skos:semanticRelation, which has rdfs:domain/rdfs:range skos:Concept, any consumer who loads SKOS will infer your kgo:Wikidata instances are
  skos:Concepts. You don't see it locally only because export_reasoned_rdf.py never imports SKOS.

  In an LPG, SAME_AS almost always means "linked record," not owl:sameAs. Mapping identity predicates by edge-name string is unsafe by construction — this
  should be an explicit, per-edge opt-in in the profile, not a lookup table.

  2. External identifiers modeled as classes, with the real IRI trapped in a literal

  kgo:ORCID and kgo:Wikidata are OWL classes whose instances are locally-minted URIs (kgr:orcid/0000-0002-...), and the actual global IRI is a string:
  kgo:uri "https://orcid.org/..."^^xsd:anyURI (graph.ttl:160-178). This is the literal-encoded-link anti-pattern, and it's the root of §1.

  Two independent costs:
  - No linked data. Nothing in the graph points at https://orcid.org/0000-0002-1624-9711 or http://www.wikidata.org/entity/Q11468 as a resource. A consumer
  cannot follow the link, and cannot join your graph to ORCID or Wikidata without string-parsing a literal.
  - Your Wikidata URIs point at https://www.wikidata.org/wiki/Q11468 — the human-readable web page, not the entity IRI
  http://www.wikidata.org/entity/Q11468. Even after string extraction, the join fails.

  Either mint the external IRI directly (kgr:faculty/de54 owl:sameAs <https://orcid.org/0000-0002-1624-9711>, kgo:Concept skos:exactMatch
  <http://www.wikidata.org/entity/Q11468>) or, if you want to keep identifier provenance, use the schema:PropertyValue/vivo:orcidId pattern. What you must
  not do is keep both the class-per-identifier-scheme model and owl:sameAs.

  3. rdfs:domain/rdfs:range inferred from a data snapshot

  ontology_common.py:322-330 emits rdfs:domain when exactly one class currently uses a property. The comment says this determines "whether a domain can
  safely be emitted" — it's the opposite of safe. kgo:description rdfs:domain kgo:ConceptScheme (ontology.ttl:54-59) means anything with a description is a
  ConceptScheme. Add a description to a Department and a reasoner will type it as a skos:ConceptScheme. Same for kgo:email → Faculty, kgo:venue →
  Publication, kgo:awardNumber → Grant.

  Also: nothing validates graph_nary.ttl, graph.jsonld, or the inferred graph — generate_shacl.py only iterates node_types, so the n-ary relationship
  classes and their properties have neither ontology declarations nor shapes. Relationship metadata is the entire justification for the n-ary model, and it
  is the one thing left undeclared and unchecked.

  6. PROV-O integration is a single misused triple

  The README claims a provenance.ttl artifact and "PROV-O provenance generation." There is no generate_provenance.py, no provenance.ttl in output/, and
  grep -r prov finds only a namespace binding. The entire PROV footprint is rdf_nary.py:76-80:

  turtle
  <...relationship/about/5%3A...> prov:wasDerivedFrom "5:ec3be6f8-...:1152931400211496986" .

  Two problems. First, prov:wasDerivedFrom is declared owl:ObjectProperty in PROV-O with rdfs:range prov:Entity; giving it a string literal makes the graph
  invalid OWL DL (object property used as data property) and will be flagged by any store with PROV-O loaded. Second, a Neo4j elementId is not an entity —
  and it isn't even durable (Neo4j explicitly documents elementIds as unstable across restarts and re-imports), so this both breaks DL and rots.

  Real PROV-O for this pipeline needs prov:Activity per pipeline step, prov:SoftwareAgent for the toolkit version, prov:used on the source graph, and
  prov:wasGeneratedBy/prov:generatedAtTime on each artifact — which is exactly the traceability the README promises. Until then I'd soften the README
  turtle
  <...grant/2016522> kgo:hasInvestigator <...faculty/de54>, <...orcid/0000-0002-1624-9711> .

  Every grant and publication now has twice as many investigators/authors as it really has. Any downstream count, dedup, or aggregation is wrong.

  The same name-based mapping applies skos:exactMatch (symmetric and transitive, per SKOS S43) to EXACT_MATCH edges. Because skos:exactMatch ⊑ … ⊑
  skos:semanticRelation, which has rdfs:domain/rdfs:range skos:Concept, any consumer who loads SKOS will infer your kgo:Wikidata instances are
  skos:Concepts. You don't see it locally only because export_reasoned_rdf.py never imports SKOS.

  In an LPG, SAME_AS almost always means "linked record," not owl:sameAs. Mapping identity predicates by edge-name string is unsafe by construction — this
  should be an explicit, per-edge opt-in in the profile, not a lookup table.

  2. External identifiers modeled as classes, with the real IRI trapped in a literal

  kgo:ORCID and kgo:Wikidata are OWL classes whose instances are locally-minted URIs (kgr:orcid/0000-0002-...), and the actual global IRI is a string:
  kgo:uri "https://orcid.org/..."^^xsd:anyURI (graph.ttl:160-178). This is the literal-encoded-link anti-pattern, and it's the root of §1.

  Two independent costs:
  - No linked data. Nothing in the graph points at https://orcid.org/0000-0002-1624-9711 or http://www.wikidata.org/entity/Q11468 as a resource. A consumer
  cannot follow the link, and cannot join your graph to ORCID or Wikidata without string-parsing a literal.
  - Your Wikidata URIs point at https://www.wikidata.org/wiki/Q11468 — the human-readable web page, not the entity IRI
  http://www.wikidata.org/entity/Q11468. Even after string extraction, the join fails.

  Either mint the external IRI directly (kgr:faculty/de54 owl:sameAs <https://orcid.org/0000-0002-1624-9711>, kgo:Concept skos:exactMatch
  <http://www.wikidata.org/entity/Q11468>) or, if you want to keep identifier provenance, use the schema:PropertyValue/vivo:orcidId pattern. What you must
  not do is keep both the class-per-identifier-scheme model and owl:sameAs.

  3. rdfs:domain/rdfs:range inferred from a data snapshot

  ontology_common.py:322-330 emits rdfs:domain when exactly one class currently uses a property. The comment says this determines "whether a domain can
  safely be emitted" — it's the opposite of safe. kgo:description rdfs:domain kgo:ConceptScheme (ontology.ttl:54-59) means anything with a description is a
  ConceptScheme. Add a description to a Department and a reasoner will type it as a skos:ConceptScheme. Same for kgo:email → Faculty, kgo:venue →
  Publication, kgo:awardNumber → Grant.

  Class name baked into the URI + labels(n)[0]. neo4j_reader.py:52 takes only the first Neo4j label, whose order Neo4j does not guarantee. So for
  multi-label nodes the URI is nondeterministic and all secondary types are lost. Worse, discover_schema.py keys node_types on labels(n)[0] but discovers
  properties with UNWIND labels(n) — so a node labeled [Faculty, Person] will KeyError on schema.node_types["Person"]. The toolkit works only on
  single-label graphs, and multi-label handling is the central problem in LPG→RDF mapping. This is the highest-value thing to fix in the reader.

  turtle
  <...grant/2016522> kgo:hasInvestigator <...faculty/de54>, <...orcid/0000-0002-1624-9711> .

  Every grant and publication now has twice as many investigators/authors as it really has. Any downstream count, dedup, or aggregation is wrong.

  The same name-based mapping applies skos:exactMatch (symmetric and transitive, per SKOS S43) to EXACT_MATCH edges. Because skos:exactMatch ⊑ … ⊑
  skos:semanticRelation, which has rdfs:domain/rdfs:range skos:Concept, any consumer who loads SKOS will infer your kgo:Wikidata instances are
  skos:Concepts. You don't see it locally only because export_reasoned_rdf.py never imports SKOS.

  In an LPG, SAME_AS almost always means "linked record," not owl:sameAs. Mapping identity predicates by edge-name string is unsafe by construction — this
  should be an explicit, per-edge opt-in in the profile, not a lookup table.

  2. External identifiers modeled as classes, with the real IRI trapped in a literal

  kgo:ORCID and kgo:Wikidata are OWL classes whose instances are locally-minted URIs (kgr:orcid/0000-0002-...), and the actual global IRI is a string:
  kgo:uri "https://orcid.org/..."^^xsd:anyURI (graph.ttl:160-178). This is the literal-encoded-link anti-pattern, and it's the root of §1.

  Two independent costs:
  - No linked data. Nothing in the graph points at https://orcid.org/0000-0002-1624-9711 or http://www.wikidata.org/entity/Q11468 as a resource. A consumer
  cannot follow the link, and cannot join your graph to ORCID or Wikidata without string-parsing a literal.
  - Your Wikidata URIs point at https://www.wikidata.org/wiki/Q11468 — the human-readable web page, not the entity IRI
  http://www.wikidata.org/entity/Q11468. Even after string extraction, the join fails.

  Either mint the external IRI directly (kgr:faculty/de54 owl:sameAs <https://orcid.org/0000-0002-1624-9711>, kgo:Concept skos:exactMatch
  <http://www.wikidata.org/entity/Q11468>) or, if you want to keep identifier provenance, use the schema:PropertyValue/vivo:orcidId pattern. What you must
  not do is keep both the class-per-identifier-scheme model and owl:sameAs.

  3. rdfs:domain/rdfs:range inferred from a data snapshot

  ontology_common.py:322-330 emits rdfs:domain when exactly one class currently uses a property. The comment says this determines "whether a domain can
  safely be emitted" — it's the opposite of safe. kgo:description rdfs:domain kgo:ConceptScheme (ontology.ttl:54-59) means anything with a description is a
  ConceptScheme. Add a description to a Department and a reasoner will type it as a skos:ConceptScheme. Same for kgo:email → Faculty, kgo:venue →
  Publication, kgo:awardNumber → Grant.

  The reified model is competently built but semantically stranded:

  - No bridge to the binary form. Nothing connects kgo:AuthorOfRelationship + kgo:source/kgo:target to kgo:authorOf. A consumer of graph_nary.ttl cannot
  derive authorOf, and a consumer who merges both graphs gets every fact twice with no way to recognize the duplication. OWL 2 RL does support the fix:
  <...grant/2016522> kgo:hasInvestigator <...faculty/de54>, <...orcid/0000-0002-1624-9711> .

  Every grant and publication now has twice as many investigators/authors as it really has. Any downstream count, dedup, or aggregation is wrong.

  The same name-based mapping applies skos:exactMatch (symmetric and transitive, per SKOS S43) to EXACT_MATCH edges. Because skos:exactMatch ⊑ … ⊑
  skos:semanticRelation, which has rdfs:domain/rdfs:range skos:Concept, any consumer who loads SKOS will infer your kgo:Wikidata instances are
  skos:Concepts. You don't see it locally only because export_reasoned_rdf.py never imports SKOS.

  In an LPG, SAME_AS almost always means "linked record," not owl:sameAs. Mapping identity predicates by edge-name string is unsafe by construction — this
  should be an explicit, per-edge opt-in in the profile, not a lookup table.

  2. External identifiers modeled as classes, with the real IRI trapped in a literal

  kgo:ORCID and kgo:Wikidata are OWL classes whose instances are locally-minted URIs (kgr:orcid/0000-0002-...), and the actual global IRI is a string:
  kgo:uri "https://orcid.org/..."^^xsd:anyURI (graph.ttl:160-178). This is the literal-encoded-link anti-pattern, and it's the root of §1.

  Two independent costs:
  - No linked data. Nothing in the graph points at https://orcid.org/0000-0002-1624-9711 or http://www.wikidata.org/entity/Q11468 as a resource. A consumer
  cannot follow the link, and cannot join your graph to ORCID or Wikidata without string-parsing a literal.
  - Your Wikidata URIs point at https://www.wikidata.org/wiki/Q11468 — the human-readable web page, not the entity IRI
  http://www.wikidata.org/entity/Q11468. Even after string extraction, the join fails.

  Either mint the external IRI directly (kgr:faculty/de54 owl:sameAs <https://orcid.org/0000-0002-1624-9711>, kgo:Concept skos:exactMatch
  <http://www.wikidata.org/entity/Q11468>) or, if you want to keep identifier provenance, use the schema:PropertyValue/vivo:orcidId pattern. What you must
  not do is keep both the class-per-identifier-scheme model and owl:sameAs.

  3. rdfs:domain/rdfs:range inferred from a data snapshot

  ontology_common.py:322-330 emits rdfs:domain when exactly one class currently uses a property. The comment says this determines "whether a domain can
  safely be emitted" — it's the opposite of safe. kgo:description rdfs:domain kgo:ConceptScheme (ontology.ttl:54-59) means anything with a description is a
  ConceptScheme. Add a description to a Department and a reasoner will type it as a skos:ConceptScheme. Same for kgo:email → Faculty, kgo:venue →
  Publication, kgo:awardNumber → Grant.

  The concrete failure mode is worse than hypothetical, because of a namespace collision with the n-ary model:

  - rdf_nary.py:82-89 emits relationship properties as KGO[key] — the same namespace as node properties.
  - So a relationship carrying startDate (very plausible for AFFILIATED_WITH) emits kgo:startDate, whose rdfs:domain is kgo:Grant.
  - OWL RL then infers your kgo:AffiliatedWithRelationship instance is a Grant.

  The inverse problem also bites: when 2+ classes share a property the domain is dropped entirely rather than expressed as owl:unionOf, so information is
  silently lost. And because domains flip on and off as data changes while owl:versionInfo stays "1.0" (ontology_common.py:198-202), the logical meaning of
  your terms changes between builds with no version signal.

  Recommendation: don't derive domain/range from instance data at all. Put them in the profile (profiles/faculty.py), where a human commits to them; or
  emit them as SHACL only, where closed-world constraint semantics is what you actually want.

  4. owl:FunctionalProperty is derived from the wrong statistic

  property_analysis.py:65 computes unique = distinct == len(non_null) — i.e. values are distinct across all instances of the label. That is
  inverse-functionality (a key). But ontology_common.py:285-296 uses it to emit owl:FunctionalProperty, which means at most one value per subject.
  Different axiom entirely.
  
  The result is a set of axioms that is close to noise:
  - kgo:email a owl:FunctionalProperty — emitted because all emails happen to be distinct.
  - kgo:sponsor not functional — because two grants share "National Science Foundation," even though sponsor obviously is single-valued per grant.
  - kgo:rank not functional, for the same accidental reason.
  
  Consequence: the day a faculty member has two email addresses, OWL RL asserts the two literals are owl:sameAs, which owlrl reports as an inconsistency.
  You've bought a fragile axiom that also doesn't say what you meant. If you want key semantics, use owl:hasKey or owl:InverseFunctionalProperty (carefully
  — kgo:identifier as IFP would merge a grant and a publication sharing an identifier string). If you want cardinality, SHACL sh:maxCount already does it,
  safely.

  Note also that OWL and SHACL disagree on the same facts: kgo:name gets sh:maxCount 1 from DESIGN_RULES (generate_shacl.py:72-75) but no
  owl:FunctionalProperty, because the two artifacts derive cardinality from different sources.

  5. SHACL: multiple sh:property shapes on one path are conjunctive

  generate_shacl.py:231-268 emits one property shape per discovered (source, target) pair. When a relationship has two target types from the same source,
  you get two shapes on the same path with different sh:class — and SHACL conjoins them, so every value violates one of them. I confirmed this with
  pySHACL:

  CONFORMS: False
  Source Shape: [ sh:class kgo:College ; sh:nodeKind sh:IRI ; sh:path kgo:affiliatedWith ]
  Focus Node: kgr:f1   Value Node: kgr:d1   Message: Value does not have class kgo:College

  Your current dataset happens to have no such relationship, so it's latent — but the moment AFFILIATED_WITH reaches both a Department and a College, or
  ABOUT reaches Concepts and Datasets, validation fails on correct data. The correct construction is one property shape per path with sh:or ( [sh:class A]
  [sh:class B] ).

  Two more SHACL issues:
  - Language tags are forbidden. sh:datatype is emitted unconditionally (generate_shacl.py:175-177), so skos:prefLabel gets sh:datatype xsd:string
  (shapes.ttl:52-57). That rejects "Engineering"@en — the SKOS best practice. Labels should be sh:or ( [sh:datatype xsd:string] [sh:datatype
  rdf:langString] ) plus sh:uniqueLang true, and instance labels should carry @en.
  - Enums from small samples. sh:in ( "Assistant Professor" "Associate Professor" "Professor" ) (shapes.ttl:139) comes from ≤10 distinct observed values
  (property_analysis.py:77-81). The first "Emeritus Professor" or "Senior Lecturer" is a validation failure on legitimate data. Emit these as sh:severity
  sh:Warning, or as commented-out suggestions.

  Also: nothing validates graph_nary.ttl, graph.jsonld, or the inferred graph — generate_shacl.py only iterates node_types, so the n-ary relationship
  classes and their properties have neither ontology declarations nor shapes. Relationship metadata is the entire justification for the n-ary model, and it
  is the one thing left undeclared and unchecked.

  6. PROV-O integration is a single misused triple

  The README claims a provenance.ttl artifact and "PROV-O provenance generation." There is no generate_provenance.py, no provenance.ttl in output/, and
  grep -r prov finds only a namespace binding. The entire PROV footprint is rdf_nary.py:76-80:

  turtle
  <...relationship/about/5%3A...> prov:wasDerivedFrom "5:ec3be6f8-...:1152931400211496986" .

  Two problems. First, prov:wasDerivedFrom is declared owl:ObjectProperty in PROV-O with rdfs:range prov:Entity; giving it a string literal makes the graph
  invalid OWL DL (object property used as data property) and will be flagged by any store with PROV-O loaded. Second, a Neo4j elementId is not an entity —
  and it isn't even durable (Neo4j explicitly documents elementIds as unstable across restarts and re-imports), so this both breaks DL and rots.

  Real PROV-O for this pipeline needs prov:Activity per pipeline step, prov:SoftwareAgent for the toolkit version, prov:used on the source graph, and
  prov:wasGeneratedBy/prov:generatedAtTime on each artifact — which is exactly the traceability the README promises. Until then I'd soften the README
  claim; right now it overstates what ships.

  7. schema.org export silently drops everything

  serializers/schema_org.py looks up relationships with graph.outgoing(person.uri, "AFFILIATED_WITH"), but SemanticGraph.outgoing() matches
  relationship.predicate (semantic_model.py:127-145), which is camelCase affiliatedWith (neo4j_reader.py:113). No lookup ever matches. Confirmed in the
  output — every file is:

  {"@context":"https://schema.org","@type":"Person",
   "@id":"https://id.duffield.cornell.edu/resource#faculty/de54","name":"David Erickson"}

  affiliation, knowsAbout, sameAs, worksFor — all of the README's advertised support — emit nothing. Beyond the bug, three modeling notes for when it's
  fixed:
  - A Department is typed CollegeOrUniversity (schema_org.py:94). It should be Organization or EducationalOrganization.
  - @id becomes {url}#person when a url exists (schema_org.py:32-36), which is a different identifier from the kgr: URI used in graph.ttl, with no
  owl:sameAs bridging them. The two serializations of the same person can't be joined.
  - knowsAbout emits bare label strings, discarding the SKOS concept URIs. schema:DefinedTerm with inDefinedTermSet preserves the link and is still valid
  schema.org.

  8. URI strategy

  Several distinct issues, in order of severity:

  Hash namespace for instance data. RESOURCE_NAMESPACE = f"{BASE_URI}/resource#" (config.py:16). Everything after # is never sent to the server, so every
  resource in the KG dereferences to one document at https://id.duffield.cornell.edu/resource. That's fine for a small vocabulary; for instance data it
  makes HTTP dereferencing and content negotiation impossible at any scale. Instances want slash URIs:
  https://id.duffield.cornell.edu/resource/faculty/de54.

  The fallback URI is a memory address. uri.py:50: KGR[f"{class_name.lower()}/{id(properties)}"]. id() is not stable across runs, and CPython reuses
  addresses after GC — two different entities in one run can collide into one URI, silently merging them. Use a content hash or fail loudly.

  Label-derived slugs. #department/school-of-electrical-and-computer-engineering comes from name (uri.py:16-22). Renaming a department changes its
  identity; two same-named entities of one class silently merge. Also quote() leaves / unescaped and escapes parens, producing
  #campus/weill-cornell-%28nyc%29 and #publication/arxiv%3A2101.08134 — percent-encoding in URIs is a classic source of silent non-matching terms, since
  %28 and ( are distinct RDF terms and different encoders disagree.

  Class name baked into the URI + labels(n)[0]. neo4j_reader.py:52 takes only the first Neo4j label, whose order Neo4j does not guarantee. So for
  multi-label nodes the URI is nondeterministic and all secondary types are lost. Worse, discover_schema.py keys node_types on labels(n)[0] but discovers
  properties with UNWIND labels(n) — so a node labeled [Faculty, Person] will KeyError on schema.node_types["Person"]. The toolkit works only on
  single-label graphs, and multi-label handling is the central problem in LPG→RDF mapping. This is the highest-value thing to fix in the reader.

  Ontology IRI ends in #. KGO[""] = https://id.duffield.cornell.edu/ontology# is used as the owl:Ontology IRI (ontology_common.py:162). Convention is the
  ontology IRI without the separator (.../ontology), with terms at .../ontology#Term.

  9. Two ontologies share one IRI, and neither imports what it extends

  ontology.ttl and ontology_nary.ttl both declare <https://id.duffield.cornell.edu/ontology#> a owl:Ontology with identical owl:versionInfo "1.0", but
  different axioms (the n-ary version adds ⊑ kgo:Entity everywhere, and defines relationship classes where the other defines object properties). Any tool
  that resolves both — a catalog, a triplestore, owl:imports — sees one ontology with merged, partly-contradictory content. Give them distinct IRIs
  (.../ontology/nary#) or make one an extension that imports the other.

  Also: the ontology asserts kgo:Faculty ⊑ schema:Person and kgo:Concept ⊑ skos:Concept but declares no owl:imports for schema.org or SKOS. A reasoner has
  no way to load the vocabularies you're aligning to, which is why export_reasoned_rdf.py produces no schema.org or SKOS inferences at all. And
  dcterms:created is set to date.today() on every regeneration (ontology_common.py:186-190) — that's dcterms:modified. There's no owl:versionIRI, so
  consumers cannot distinguish builds even as axioms change (see §3).

  Separately, there is not a single disjointness axiom in the ontology. No owl:disjointWith, no owl:AllDisjointClasses, no owl:propertyDisjointWith. An OWL
  ontology with no disjointness can essentially never be found inconsistent, so the OWL RL step can only ever materialize subsumptions and inverses — it
  can never catch an error. Adding kgo:Entity owl:disjointWith kgo:Relationship, and disjointness among Person/Organization/Place/Concept, is what would
  make the reasoning step earn its place. (It would also immediately surface the §1 ORCID/Faculty conflation as a hard inconsistency, which is the point.)

  10. Reasoning pipeline ordering and configuration

  Three things undercut the pipeline:

  - Validation runs before reasoning, and without the ontology. validate_shacl.py:37-51 parses only graph.ttl and passes inference="rdfs" with no
  ont_graph. Since graph.ttl contains no schema axioms, RDFS inference over it is a near no-op — the flag reads as ontology-aware validation but isn't.
  sh:class constraints therefore pass only because export_common.py:168-174 pre-materializes exactly the types the shapes expect. Any real-world graph
  typed only schema:Person would fail. Pass ont_graph=ONTOLOGY, or validate the inferred graph — either would have caught the ORCID contamination in §1.
  - No consistency check. reasoning.py calls DeductiveClosure(OWLRL_Semantics).expand(graph) and returns. Nothing inspects the result for owl:Nothing
  memberships or reports owlrl's clash detection. Reasoning that cannot fail is materialization, not reasoning.
  - The inferred graph loses its prefixes. export_reasoned_rdf.py:12 builds a bare Graph() without bind_namespaces(), which is why graph_inferred_clean.ttl
  is full of ns1: — it makes the HTML report's RDF viewer much harder to read for no reason.

  clean_inferred.py is a reasonable idea, but be explicit that its output is a display artifact, not a reusable graph: it strips
  rdfs:subClassOf/domain/range for all kgo: subjects, including genuinely inferred subsumptions, so it can't stand alone.

  11. N-ary modeling

  The reified model is competently built but semantically stranded:

  - No bridge to the binary form. Nothing connects kgo:AuthorOfRelationship + kgo:source/kgo:target to kgo:authorOf. A consumer of graph_nary.ttl cannot
  derive authorOf, and a consumer who merges both graphs gets every fact twice with no way to recognize the duplication. OWL 2 RL does support the fix:
  give each relationship class its own subproperties of source/target and add kgo:authorOf owl:propertyChainAxiom ( [owl:inverseOf kgo:authorOfSource]
  kgo:authorOfTarget ). Type-specific subproperties are essential — a generic chain over source/target would collapse all relationship types into one
  another.
  - source/target are LPG vocabulary, not domain vocabulary. The W3C n-ary relations note recommends domain-meaningful role properties. kgo:Affiliation
  with kgo:affiliatedPerson/kgo:affiliatedOrganization/kgo:duringInterval is what makes reification pay for itself; source/target just relabels the LPG
  edge. As it stands this is closer to RDF reification than to an n-ary pattern — if the goal is edge annotation with minimal ceremony, RDF-star is the
  more interoperable target now that SPARQL 1.2/RDF 1.2 is landing.
  - Relationship properties are emitted into the node-property namespace (see §3) and have no ontology declaration or shape.

  12. Literal and datatype handling

  - Datatype inference happens twice, independently, by different rules. type_inference.py drives the ontology's rdfs:range and the SHACL sh:datatype;
  export_common.py:38-138 re-derives the literal's datatype from the value's string form at serialization time. These can disagree — a numeric awardNumber
  in Neo4j serializes as xsd:integer while the ontology declares xsd:string, producing a sh:datatype violation and an OWL range violation on correct data.
  There should be one inference path, and the serializer should consult the discovered schema.
  - Range from a single value. property_analysis.py:46 infers the datatype from non_null[0] only. One heterogeneous property mistypes the whole class.
  - List properties become Python reprs. Neo4j array properties (common — keywords, alternate names) reach add_literal, fall through to text = str(value),
  and serialize as "['a', 'b']". That's silent data corruption; arrays should become multiple triples.
  - float → xsd:decimal in both paths (vocab.py:52, export_common.py:83-90). Neo4j floats are IEEE doubles; xsd:double is correct. xsd:decimal and
  xsd:double are distinct value spaces to a reasoner, so numeric joins against other datasets fail.
  - datetime is in XSD_TYPES but not DATATYPE_MAPPING, so datetime properties get sh:datatype xsd:dateTime in SHACL and no rdfs:range in the ontology. time
  and duration are in neither and silently become xsd:string.
  - The date heuristic is positional: len(text) == 10 and text[4] == "-" and text[7] == "-" (export_common.py:99-103) will type any 10-char dashed
  identifier as xsd:date.
  - No rdfs:label anywhere in the instance data, and no language tags. Every instance uses kgo:name, which has no rdfs:subPropertyOf rdfs:label or
  schema:name. Generic RDF tooling — Protégé, GraphDB's autocomplete, LodView, most SPARQL UIs — will show your resources as bare URIs.
  profiles/faculty.py:59 has property_alignments={}, so despite the README's "Schema.org mappings," only classes are aligned — not one property. Adding
  kgo:name ⊑ rdfs:label, schema:name, kgo:title ⊑ dcterms:title, kgo:identifier ⊑ dcterms:identifier, kgo:affiliatedWith ⊑ schema:affiliation is cheap and
  is probably the single highest interoperability return in the whole toolkit.

  13. kgo:subOrganization inverts the organizational hierarchy

  vocab.py:67-80 mechanically camelCases edge names, so SUB_ORGANIZATION becomes subOrganization and ontology_common.py:122-123 documents it as "Relates an
  organization to one of its sub-organizations" — matching schema:subOrganization ("the first includes the second"). But the data reads the other way
  (graph.ttl:11-13, 126):

  turtle
  <...department/department-of-earth-and-atmospheric-sciences> kgo:subOrganization
      <...college/cornell-bowers-college-of-computing-and-information-science>, … ;
  <...college/cornell-duffield-college-of-engineering> kgo:subOrganization <...university/cornell-university> .

  As published, Cornell University is a sub-organization of a college, and a department contains three colleges. The Neo4j edge clearly means "is a
  sub-organization of." There's no formal contradiction yet only because the property isn't aligned to schema:subOrganization — the moment you add the
  property alignments recommended above, the org tree inverts for every consumer. Rename to kgo:partOf (aligned to schema:parentOrganization) or reverse
  the triple. This is the cheapest fix on the list and a good illustration of why name-based mapping needs a human in the loop.

  14. SKOS details

  - Four concepts (fpga, machine-learning, artificial-intelligence, neural-architecture-search) assert skos:broader but no skos:inScheme, while their
  parents have it — scheme-scoped queries will return partial hierarchies.
  - No skos:hasTopConcept/skos:topConceptOf anywhere, so the scheme has no entry points for a browsing client.
  - kgo:name duplicates skos:prefLabel with identical values on every concept — pick one, and make kgo:name a subproperty of rdfs:label so both are
  discoverable.

  ---
  Suggested order of work

  1. SAME_AS/EXACT_MATCH → real external IRIs (§1, §2). This is actively producing wrong query results in shipped artifacts.
  2. Property alignments in the profile (rdfs:label, dcterms:*, schema:*) and fix subOrganization's direction (§12, §13). Cheapest interoperability wins
  available.
  3. Stop deriving OWL axioms from data — move rdfs:domain/range into the profile, drop owl:FunctionalProperty entirely, keep cardinality in SHACL (§3,
  §4). Namespace n-ary relationship properties separately (kgo:rel/).
  4. Fix the schema.org predicate bug and the SHACL sh:or construction (§7, §5). Both are small and both are latent-to-active correctness failures.
  5. Instance URIs: slash namespace, hash-based fallback, all labels not labels(n)[0] (§8). This is the one that determines whether the KG can grow.
  6. Make reasoning able to fail: add disjointness axioms and owl:imports, validate after reasoning with ont_graph set, and report inconsistency (§9, §10).
  7. Then the n-ary bridge (§11), datatype unification (§12), and real PROV-O (§6).

  One README note worth making regardless: provenance.ttl, generate_provenance.py, and the reports/ layout are documented but don't exist, and the
  schema.org section describes fields that never emit. Those claims should come down or the features should go in — right now the docs are the least
  reliable artifact in the repo.