from rdflib import Namespace
from rdflib.namespace import RDFS

from ontology_toolkit.alignments import ClassAlignment
from ontology_toolkit.ontology_profile import OntologyProfile

VIVO = Namespace("http://vivoweb.org/ontology/core#")


VIVO_PROFILE = OntologyProfile(
    name="VIVO",
    class_alignments={
        "Faculty": [
            ClassAlignment(
                target=VIVO.FacultyMember,
                relation=RDFS.subClassOf,
            ),
        ],
        "Department": [
            ClassAlignment(
                target=VIVO.Department,
                relation=RDFS.subClassOf,
            ),
        ],
        "College": [
            ClassAlignment(
                target=VIVO.College,
                relation=RDFS.subClassOf,
            ),
        ],
        "University": [
            ClassAlignment(
                target=VIVO.University,
                relation=RDFS.subClassOf,
            ),
        ],
        "Publication": [
            ClassAlignment(
                target=VIVO.InformationResource,
                relation=RDFS.subClassOf,
            ),
        ],
        "Grant": [
            ClassAlignment(
                target=VIVO.Grant,
                relation=RDFS.subClassOf,
            ),
        ],
    },
    property_alignments={},
    design_rules={},
)