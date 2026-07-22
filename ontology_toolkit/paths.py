from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

REPORT = OUTPUT_DIR / "report.html"

ONTOLOGY = OUTPUT_DIR / "ontology.ttl"
ONTOLOGY_NARY = OUTPUT_DIR / "ontology_nary.ttl"

GRAPH = OUTPUT_DIR / "graph.ttl"
GRAPH_JSONLD = OUTPUT_DIR / "graph.jsonld"

SHAPES = OUTPUT_DIR / "shapes.ttl"

VALIDATION_REPORT = OUTPUT_DIR / "validation_report.txt"

SCHEMA_ORG_DIR = OUTPUT_DIR / "schema_org"

DOCS_DIR = PROJECT_ROOT / "docs"