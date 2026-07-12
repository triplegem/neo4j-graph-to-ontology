from dataclasses import dataclass, field


# ------------------------------------------------------------
# Property Definition
# ------------------------------------------------------------

@dataclass
class PropertyDefinition:
    """
    Describes a discovered property on a node or relationship.
    """

    # Property name
    name: str

    # Inferred semantic datatype
    data_type: str = "unknown"

    # Analysis
    nullable: bool = True
    unique: bool = False
    inferred_identifier: bool = False
    inferred_enum: bool = False

    # Statistics
    distinct_values: int = 0
    examples: list = field(default_factory=list)


# ------------------------------------------------------------
# Node Type
# ------------------------------------------------------------

@dataclass
class NodeType:
    """
    Describes a Neo4j node label.
    """

    label: str
    count: int = 0
    properties: dict[str, PropertyDefinition] = field(default_factory=dict)


# ------------------------------------------------------------
# Relationship Type
# ------------------------------------------------------------

@dataclass
class RelationshipType:
    """
    Describes a Neo4j relationship type.
    """

    name: str
    count: int = 0
    source_labels: set[str] = field(default_factory=set)
    target_labels: set[str] = field(default_factory=set)
    properties: dict[str, PropertyDefinition] = field(default_factory=dict)


# ------------------------------------------------------------
# Graph Schema
# ------------------------------------------------------------

@dataclass
class GraphSchema:
    """
    Represents the discovered schema of a Neo4j graph.
    """
    node_types: dict[str, NodeType] = field(default_factory=dict)
    relationship_types: dict[str, RelationshipType] = field(default_factory=dict)