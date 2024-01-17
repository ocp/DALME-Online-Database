"""API endpoint for managing locations."""
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

from dalme_api.access_policies import GeneralAccessPolicy
from dalme_api.base_viewset import DALMEBaseViewSet
from ida.models import Location

from .serializers import LocationSerializer


class Locations(DALMEBaseViewSet):
    """API endpoint for managing places."""

    permission_classes = [GeneralAccessPolicy]
    oauth_permission_classes = [TokenHasReadWriteScope]

    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filterset_fields = ['id', 'location_type']
    search_fields = ['id', 'location_type']
    ordering_fields = ['id', 'location_type']
    ordering = ['id']
