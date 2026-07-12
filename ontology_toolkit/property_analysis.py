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
            enum_values=[],
            examples=[]
        )

    #
    # Infer datatype from the first non-null value
    #

    datatype = infer_property_type(non_null[0])

    #
    # Collect distinct values
    #

    distinct_list = []

    for value in non_null:

        if value not in distinct_list:
            distinct_list.append(value)

    distinct = len(distinct_list)

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
        and 1 < distinct <= 10
        and len(non_null) > distinct
    )

    #
    # Enumeration values
    #

    enum_values = []

    if inferred_enum:

        enum_values = sorted(
            str(v)
            for v in distinct_list
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

    examples = distinct_list[:5]

    return PropertyDefinition(
        name=name,
        data_type=datatype,
        nullable=nullable,
        unique=unique,
        inferred_identifier=inferred_identifier,
        inferred_enum=inferred_enum,
        distinct_values=distinct,
        enum_values=enum_values,
        examples=examples
    )