"""Interface for the dalme_api.resources.locales module."""
from .endpoints import Locales
from .serializers import LocaleReferenceSerializer

__all__ = [
    'Locales',
    'LocaleReferenceSerializer',
]
