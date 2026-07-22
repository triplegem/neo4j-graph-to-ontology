from rdflib import Graph, Namespace

EX = Namespace("http://example.org/")

g = Graph()

# TODO:
# Find RDFLib's API for creating a quoted triple.

print(g.serialize(format="turtle"))