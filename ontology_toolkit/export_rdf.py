"""
Ontology Toolkit

Export a Neo4j property graph as RDF/Turtle.
"""

from urllib.parse import quote

from rdflib import Graph, Literal
from rdflib.namespace import RDF, RDFS, OWL, SKOS, XSD

from ontology_toolkit.vocab import (
    KGO,
    KGR,
    SCHEMA,
    CLASS_ALIGNMENT,
    STANDARD_PREDICATES,
    relationship_to_predicate,
)

#
# Stable URI generation
#

IDENTIFIER_PROPERTIES = [
    "identifier",
    "netid",
    "uri",
    "awardNumber",
    "name",
]


def make_uri(label: str, properties: dict):
    """
    Create a stable URI for an instance resource.
    """

    for key in IDENTIFIER_PROPERTIES:

        if key in properties and properties[key]:

            value = quote(
                str(properties[key])
                .lower()
                .replace(" ", "-")
            )

            return KGR[f"{label.lower()}/{value}"]

    #
    # Fallback
    #

    return KGR[f"{label.lower()}/{id(properties)}"]


def add_literal(graph, subject, predicate, value):
    """
    Add a literal using the most appropriate XSD datatype.
    """

    if value is None:
        return

    if isinstance(value, bool):

        graph.add((
            subject,
            predicate,
            Literal(value, datatype=XSD.boolean)
        ))
        return

    if isinstance(value, int):

        graph.add((
            subject,
            predicate,
            Literal(value, datatype=XSD.integer)
        ))
        return

    if isinstance(value, float):

        graph.add((
            subject,
            predicate,
            Literal(value, datatype=XSD.decimal)
        ))
        return

    text = str(value)

    #
    # ISO date
    #

    if (
        len(text) == 10
        and text[4] == "-"
        and text[7] == "-"
    ):

        graph.add((
            subject,
            predicate,
            Literal(text, datatype=XSD.date)
        ))
        return

    #
    # URI
    #

    if text.startswith("http://") or text.startswith("https://"):

        graph.add((
            subject,
            predicate,
            Literal(text, datatype=XSD.anyURI)
        ))
        return

    #
    # Default string
    #

    graph.add((
        subject,
        predicate,
        Literal(text)
    ))


def export_rdf(driver, filename="graph.ttl"):

    graph = Graph()

    #
    # Register namespaces
    #

    graph.bind("kgo", KGO)
    graph.bind("kgr", KGR)
    graph.bind("schema", SCHEMA)
    graph.bind("rdf", RDF)
    graph.bind("rdfs", RDFS)
    graph.bind("owl", OWL)
    graph.bind("skos", SKOS)
    graph.bind("xsd", XSD)

    #
    # Cache Neo4j element IDs -> RDF URIs
    #

    uri_map = {}

    with driver.session() as session:

        #
        # Export nodes
        #

        result = session.run("""
            MATCH (n)

            RETURN
                elementId(n) AS id,
                labels(n)[0] AS label,
                properties(n) AS props
        """)

        for record in result:

            node_id = record["id"]
            label = record["label"]
            props = record["props"]

            subject = make_uri(label, props)

            uri_map[node_id] = subject

            #
            # Local ontology class
            #

            graph.add((
                subject,
                RDF.type,
                KGO[label]
            ))

            #
            # Standard vocabulary alignment
            #

            if label in CLASS_ALIGNMENT:

                graph.add((
                    subject,
                    RDF.type,
                    CLASS_ALIGNMENT[label]
                ))

            #
            # Datatype properties
            #

            for key, value in props.items():

                predicate = STANDARD_PREDICATES.get(
                    key,
                    KGO[key]
                )

                add_literal(
                    graph,
                    subject,
                    predicate,
                    value
                )

        #
        # Export relationships
        #

        result = session.run("""
            MATCH (a)-[r]->(b)

            RETURN
                elementId(a) AS source,
                type(r) AS rel,
                elementId(b) AS target
        """)

        for record in result:

            source = uri_map[record["source"]]
            target = uri_map[record["target"]]

            predicate_name = relationship_to_predicate(
                record["rel"]
            )

            predicate = STANDARD_PREDICATES.get(
                predicate_name,
                KGO[predicate_name]
            )

            graph.add((
                source,
                predicate,
                target
            ))

    graph.serialize(
        destination=filename,
        format="turtle"
    )

    return filename