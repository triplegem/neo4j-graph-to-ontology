from dataclasses import dataclass, field

from ontology_toolkit.alignments import (
    ClassAlignment,
    PropertyAlignment,
)


@dataclass
class OntologyProfile:
    name: str

    class_alignments: dict[str, list[ClassAlignment]] = field(
        default_factory=dict,
    )

    property_alignments: dict[str, list[PropertyAlignment]] = field(
        default_factory=dict,
    )

    design_rules: dict = field(
        default_factory=dict,
    )