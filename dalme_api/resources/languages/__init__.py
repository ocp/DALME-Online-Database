"""Interface for the dalme_api.resources.languages module."""
from .endpoints import Languages
from .serializers import LanguageReferenceSerializer

__all__ = [
    'Languages',
    'LanguageReferenceSerializer',
]
