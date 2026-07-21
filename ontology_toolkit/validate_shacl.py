"""
Validate an RDF graph against SHACL shapes.
"""

from rdflib import Graph
from pyshacl import validate


def validate_graph(
    rdf_file="graph.ttl",
    shacl_file="shapes.ttl",
    report_file="validation_report.txt",
):
    """
    Validate an RDF graph against a SHACL shapes graph.

    Parameters
    ----------
    rdf_file : str
        Path to the RDF graph (Turtle).

    shacl_file : str
        Path to the SHACL shapes graph.

    report_file : str
        Path where the validation report will be written.
    """

    data_graph = Graph()
    data_graph.parse(rdf_file, format="turtle")

    shapes_graph = Graph()
    shapes_graph.parse(shacl_file, format="turtle")

    conforms, results_graph, results_text = validate(
        data_graph=data_graph,
        shacl_graph=shapes_graph,
        inference="rdfs",
        abort_on_first=False,
        allow_infos=True,
        allow_warnings=True,
    )

    print("=" * 60)

    if conforms:
        print("✓ SHACL validation PASSED")
    else:
        print("✗ SHACL validation FAILED")

    print("=" * 60)
    print(results_text)

    #
    # Save report to disk
    #

    with open(report_file, "w", encoding="utf-8") as f:
        f.write(results_text)

    print(f"Validation report written to {report_file}")

    return conforms