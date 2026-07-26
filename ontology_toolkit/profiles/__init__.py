from .schema_org import SCHEMA_ORG_PROFILE
from .vivo import VIVO_PROFILE, VIVO

ACTIVE_PROFILES = [
    SCHEMA_ORG_PROFILE,
    VIVO_PROFILE,
]

__all__ = [
    "ACTIVE_PROFILES",
    "VIVO",
]