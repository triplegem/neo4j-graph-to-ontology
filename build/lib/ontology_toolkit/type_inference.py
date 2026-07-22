"""
Ontology Toolkit

Property type inference.

Analyzes Python values returned by the Neo4j driver and infers
their semantic datatype.
"""

from datetime import date, datetime
from urllib.parse import urlparse
import re

from neo4j.time import Date, DateTime, Time, Duration


# ----------------------------------------------------------
# Regular Expressions
# ----------------------------------------------------------

EMAIL_PATTERN = re.compile(
    r"^[^@]+@[^@]+\.[^@]+$"
)

ORCID_PATTERN = re.compile(
    r"^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$"
)

DOI_PATTERN = re.compile(
    r"^10\.\d{4,9}/.+$"
)

WIKIDATA_PATTERN = re.compile(
    r"^Q\d+$"
)


# ----------------------------------------------------------
# Property Type Inference
# ----------------------------------------------------------

def infer_property_type(value):
    """
    Infer the semantic datatype of a Neo4j property.
    """

    #
    # Null
    #

    if value is None:
        return "unknown"

    #
    # ----------------------------------------------------------
    # Neo4j temporal types
    # ----------------------------------------------------------
    #

    if isinstance(value, Date):
        return "date"

    if isinstance(value, DateTime):
        return "datetime"

    if isinstance(value, Time):
        return "time"

    if isinstance(value, Duration):
        return "duration"

    #
    # ----------------------------------------------------------
    # Standard Python temporal types
    # ----------------------------------------------------------
    #

    if isinstance(value, datetime):
        return "datetime"

    if isinstance(value, date):
        return "date"

    #
    # ----------------------------------------------------------
    # Primitive Python types
    # ----------------------------------------------------------
    #

    if isinstance(value, bool):
        return "boolean"

    if isinstance(value, int):
        return "integer"

    if isinstance(value, float):
        return "float"

    if isinstance(value, list):
        return "list"

    #
    # ----------------------------------------------------------
    # Strings
    # ----------------------------------------------------------
    #

    if isinstance(value, str):

        #
        # URI
        #

        parsed = urlparse(value)

        if parsed.scheme in ("http", "https"):
            return "uri"

        #
        # Email
        #

        if EMAIL_PATTERN.match(value):
            return "email"

        #
        # ORCID identifier
        #

        if ORCID_PATTERN.match(value):
            return "orcid"

        #
        # DOI
        #

        if DOI_PATTERN.match(value):
            return "doi"

        #
        # Wikidata identifier
        #

        if WIKIDATA_PATTERN.match(value):
            return "wikidata_identifier"

        #
        # Default string
        #

        return "string"

    #
    # ----------------------------------------------------------
    # Fallback
    # ----------------------------------------------------------
    #

    return type(value).__name__.lower()