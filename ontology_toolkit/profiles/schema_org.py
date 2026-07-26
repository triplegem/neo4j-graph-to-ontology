from rdflib.namespace import RDFS, SKOS

from ontology_toolkit.alignments import ClassAlignment
from ontology_toolkit.ontology_profile import OntologyProfile
from ontology_toolkit.vocab import SCHEMA


SCHEMA_ORG_PROFILE = OntologyProfile(
    name="schema.org",
    class_alignments={
        "Faculty": [
            ClassAlignment(
                target=SCHEMA.Person,
                relation=RDFS.subClassOf,
            ),
        ],
        "Publication": [
            ClassAlignment(
                target=SCHEMA.ScholarlyArticle,
                relation=RDFS.subClassOf,
            ),
        ],
        "Department": [
            ClassAlignment(
                target=SCHEMA.Organization,
                relation=RDFS.subClassOf,
            ),
        ],
        "College": [
            ClassAlignment(
                target=SCHEMA.CollegeOrUniversity,
                relation=RDFS.subClassOf,
            ),
        ],
        "University": [
            ClassAlignment(
                target=SCHEMA.CollegeOrUniversity,
                relation=RDFS.subClassOf,
            ),
        ],
        "Campus": [
            ClassAlignment(
                target=SCHEMA.Place,
                relation=RDFS.subClassOf,
            ),
        ],
        "Concept": [
            ClassAlignment(
                target=SKOS.Concept,
                relation=RDFS.subClassOf,
            ),
        ],
        "ConceptScheme": [
            ClassAlignment(
                target=SKOS.ConceptScheme,
                relation=RDFS.subClassOf,
            ),
        ],
    },
    property_alignments={},
    design_rules={},
)