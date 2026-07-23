from dataclasses import dataclass

from rdflib.term import URIRef


@dataclass(frozen=True)
class ClassAlignment:
    target: URIRef
    relation: URIRef


@dataclass(frozen=True)
class PropertyAlignment:
    target: URIRef
    relation: URIRef