"""
Ontology Toolkit

Property analysis.

Analyzes all observed values for a property and produces a
PropertyDefinition containing inferred metadata.
"""

from ontology_toolkit.models import PropertyDefinition
from ontology_toolkit.type_inference import infer_property_type


def analyze_property(name: str, values: list) -> PropertyDefinition:
    """
    Analyze all observed values for a property.
    """

    #
    # Remove null values
    #

    non_null = [v for v in values if v is not None]

    #
    # Empty property
    #

    if not non_null:
        return PropertyDefinition(
            name=name,
            data_type="unknown",
            nullable=True,
            unique=False,
            inferred_identifier=False,
            inferred_enum=False,
            distinct_values=0,
            examples=[]
        )

    #
    # Infer datatype from the first non-null value
    #

    datatype = infer_property_type(non_null[0])

    #
    # Count distinct values
    #

    try:
        distinct = len(set(non_null))
    except TypeError:
        distinct = len({str(v) for v in non_null})

    #
    # Determine uniqueness
    #

    unique = distinct == len(non_null)

    #
    # Determine nullability
    #

    nullable = len(non_null) != len(values)

    #
    # Candidate enumeration
    #

    inferred_enum = (
        datatype == "string"
        and distinct <= 10
        and len(non_null) > distinct
    )

    #
    # Candidate identifier
    #

    IDENTIFIER_PROPERTIES = {
        "identifier",
        "id",
        "uri",
        "netid",
        "awardNumber",
    }

    inferred_identifier = (
        unique
        and name in IDENTIFIER_PROPERTIES
    )

    #
    # Example values
    #

    examples = []

    for value in non_null:

        if value not in examples:
            examples.append(value)

        if len(examples) >= 5:
            break

    return PropertyDefinition(
        name=name,
        data_type=datatype,
        nullable=nullable,
        unique=unique,
        inferred_identifier=inferred_identifier,
        inferred_enum=inferred_enum,
        distinct_values=distinct,
        examples=examples
    )