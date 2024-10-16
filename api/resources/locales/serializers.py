"""Serializers for locale data."""

from api.dynamic_serializer import DynamicSerializer
from api.resources.countries import CountryReferenceSerializer
from ida.models import LocaleReference


class LocaleReferenceSerializer(DynamicSerializer):
    """Serializer for locales."""

    country = CountryReferenceSerializer(field_set='attribute')

    class Meta:
        model = LocaleReference
        fields = [
            'id',
            'name',
            'administrative_region',
            'country',
            'latitude',
            'longitude',
        ]
        field_sets = {
            'option': [
                'id',
                'name',
                'country',
            ],
            'attribute': [
                'id',
                'name',
                'administrative_region',
                'country',
            ],
        }
