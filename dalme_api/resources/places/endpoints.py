"""API endpoint for managing places."""
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

from dalme_api.access_policies import BaseAccessPolicy
from dalme_api.base_viewset import DALMEBaseViewSet
from ida.models import Place

from .serializers import PlaceSerializer


class PlaceAccessPolicy(BaseAccessPolicy):
    """Access policies for Places endpoint."""

    id = 'places-policy'  # noqa: A003


class Places(DALMEBaseViewSet):
    """API endpoint for managing places."""

    permission_classes = [PlaceAccessPolicy]
    oauth_permission_classes = [TokenHasReadWriteScope]

    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    filterset_fields = ['id']
    search_fields = ['id', 'name']
    ordering_fields = ['id', 'name']
    ordering = ['name']
